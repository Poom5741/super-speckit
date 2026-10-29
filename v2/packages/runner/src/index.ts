import { spawn, type ChildProcess } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { access } from "node:fs/promises";
import { constants } from "node:fs";
import { AttemptId, OperationId, RunnerId, WorkspaceId } from "@super-speckit/protocol";

export type StructuredCommand = Readonly<{
  operationId: OperationId;
  attemptId: AttemptId;
  workspaceId: WorkspaceId;
  fence: number;
  executable: string;
  arguments: readonly string[];
  workingDirectory: string;
  environment: Readonly<Record<string, string>>;
}>;

export type CommandEvent =
  | Readonly<{ kind: "started"; processId: number }>
  | Readonly<{ kind: "stdout"; bytes: Uint8Array }>
  | Readonly<{ kind: "stderr"; bytes: Uint8Array }>
  | Readonly<{ kind: "exited"; code: number | null; signal: NodeJS.Signals | null }>;

export type OwnershipReceipt = Readonly<{
  receiptId: string;
  runnerId: RunnerId;
  workspaceId: WorkspaceId;
  attemptId: AttemptId;
  fence: number;
  processId: number;
  executableDigest: string;
}>;

type OwnedProcess = Readonly<{ process: ChildProcess; receipt: OwnershipReceipt }>;

export class NativeRunner {
  readonly id: RunnerId;
  readonly #owned = new Map<string, OwnedProcess>();

  constructor(id = "native") {
    this.id = new RunnerId(id);
  }

  async *execute(command: StructuredCommand): AsyncIterable<CommandEvent> {
    await access(command.workingDirectory, constants.R_OK | constants.W_OK);
    const child = spawn(command.executable, [...command.arguments], {
      cwd: command.workingDirectory,
      env: { ...process.env, ...command.environment },
      detached: process.platform !== "win32",
      shell: false,
      stdio: ["ignore", "pipe", "pipe"],
    });
    if (child.pid === undefined) throw new Error("runner did not receive a process ID");
    const receipt: OwnershipReceipt = {
      receiptId: randomUUID(),
      runnerId: this.id,
      workspaceId: command.workspaceId,
      attemptId: command.attemptId,
      fence: command.fence,
      processId: child.pid,
      executableDigest: createHash("sha256").update(`${command.executable}\0${command.arguments.join("\0")}`).digest("hex"),
    };
    this.#owned.set(command.operationId.value, { process: child, receipt });
    yield { kind: "started", processId: child.pid };
    const events: CommandEvent[] = [];
    child.stdout?.on("data", (bytes: Buffer) => events.push({ kind: "stdout", bytes }));
    child.stderr?.on("data", (bytes: Buffer) => events.push({ kind: "stderr", bytes }));
    const exit = new Promise<Extract<CommandEvent, { kind: "exited" }>>((resolve) => {
      child.once("exit", (code, signal) => resolve({ kind: "exited", code, signal }));
    });
    while (child.exitCode === null && child.signalCode === null) {
      const event = events.shift();
      if (event !== undefined) yield event;
      else await new Promise((resolve) => setTimeout(resolve, 10));
    }
    while (events.length > 0) {
      const event = events.shift();
      if (event !== undefined) yield event;
    }
    yield await exit;
    this.#owned.delete(command.operationId.value);
  }

  inspect(operationId: OperationId): OwnershipReceipt | null {
    return this.#owned.get(operationId.value)?.receipt ?? null;
  }

  async quiesce(input: Readonly<{ operationId: OperationId; receiptId: string; fence: number }>): Promise<Readonly<{ kind: "stopped"; receiptDigest: string }> | Readonly<{ kind: "unknown"; reason: string }>> {
    const owned = this.#owned.get(input.operationId.value);
    if (owned === undefined) return { kind: "unknown", reason: "runner has no matching owned process" };
    if (owned.receipt.receiptId !== input.receiptId || owned.receipt.fence !== input.fence) return { kind: "unknown", reason: "ownership receipt does not match" };
    const signalTarget = process.platform === "win32" ? owned.receipt.processId : -owned.receipt.processId;
    process.kill(signalTarget, "SIGTERM");
    const stopped = await Promise.race([
      new Promise<boolean>((resolve) => owned.process.once("exit", () => resolve(true))),
      new Promise<boolean>((resolve) => setTimeout(() => resolve(false), 5000)),
    ]);
    if (!stopped) return { kind: "unknown", reason: "owned process did not acknowledge stop" };
    this.#owned.delete(input.operationId.value);
    const receiptDigest = createHash("sha256").update(`${owned.receipt.receiptId}:${owned.receipt.processId}:${owned.receipt.fence}`).digest("hex");
    return { kind: "stopped", receiptDigest };
  }
}

export class PersistentJsonLineBridge {
  readonly #child: ChildProcess;
  readonly #pending = new Map<string, Readonly<{ resolve: (value: Readonly<Record<string, unknown>>) => void; reject: (error: Error) => void; timeout: NodeJS.Timeout }>>();
  #buffer = "";
  #closed = false;

  constructor(input: Readonly<{ executable: string; arguments: readonly string[] }>) {
    this.#child = spawn(input.executable, [...input.arguments], { shell: false, stdio: ["pipe", "pipe", "inherit"] });
    this.#child.stdout?.setEncoding("utf8");
    this.#child.stdout?.on("data", (chunk: string) => this.#consume(chunk));
    this.#child.once("exit", (code, signal) => this.#failAll(new Error(`persistent bridge exited (code=${String(code)}, signal=${String(signal)})`)));
    this.#child.once("error", (error) => this.#failAll(error));
  }

  request(payload: Readonly<Record<string, unknown>>, timeoutMilliseconds = 30_000): Promise<Readonly<Record<string, unknown>>> {
    if (this.#closed) return Promise.reject(new Error("persistent bridge is closed"));
    const id = randomUUID();
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.#pending.delete(id);
        reject(new Error(`persistent bridge request timed out after ${timeoutMilliseconds}ms`));
      }, timeoutMilliseconds);
      this.#pending.set(id, { resolve, reject, timeout });
      this.#child.stdin?.write(`${JSON.stringify({ id, payload })}\n`, (error) => {
        if (error !== null && error !== undefined) {
          const pending = this.#pending.get(id);
          if (pending !== undefined) clearTimeout(pending.timeout);
          this.#pending.delete(id);
          reject(error);
        }
      });
    });
  }

  close(): void {
    if (this.#closed) return;
    this.#closed = true;
    this.#child.kill("SIGTERM");
    this.#failAll(new Error("persistent bridge closed"));
  }

  #consume(chunk: string): void {
    this.#buffer += chunk;
    while (true) {
      const newline = this.#buffer.indexOf("\n");
      if (newline < 0) return;
      const line = this.#buffer.slice(0, newline);
      this.#buffer = this.#buffer.slice(newline + 1);
      const value: unknown = JSON.parse(line);
      if (value === null || Array.isArray(value) || typeof value !== "object") continue;
      const record = Object.fromEntries(Object.entries(value));
      const id = record["id"];
      const payload = record["payload"];
      if (typeof id !== "string" || payload === null || Array.isArray(payload) || typeof payload !== "object") continue;
      const pending = this.#pending.get(id);
      if (pending === undefined) continue;
      this.#pending.delete(id);
      clearTimeout(pending.timeout);
      pending.resolve(Object.fromEntries(Object.entries(payload)));
    }
  }

  #failAll(error: Error): void {
    for (const pending of this.#pending.values()) {
      clearTimeout(pending.timeout);
      pending.reject(error);
    }
    this.#pending.clear();
  }
}

export interface RunnerBridge {
  request(payload: Readonly<Record<string, unknown>>, timeoutMilliseconds?: number): Promise<Readonly<Record<string, unknown>>>;
  close(): void;
}

export class WslPersistentRunner {
  readonly id: RunnerId;
  readonly #bridge: RunnerBridge;

  constructor(input: Readonly<{ distribution: string; runnerExecutable?: string; bridge?: RunnerBridge }>) {
    if (input.distribution.trim() === "") throw new Error("WSL distribution is required");
    this.id = new RunnerId(`wsl:${input.distribution}`);
    this.#bridge = input.bridge ?? new PersistentJsonLineBridge({
      executable: "wsl.exe",
      arguments: ["--distribution", input.distribution, "--exec", input.runnerExecutable ?? "ssk-runner", "bridge"],
    });
  }

  probe(): Promise<Readonly<Record<string, unknown>>> {
    return this.#bridge.request({ kind: "probe", protocolVersion: 1 });
  }

  execute(command: StructuredCommand): Promise<Readonly<Record<string, unknown>>> {
    return this.#bridge.request({
      kind: "execute",
      protocolVersion: 1,
      command: serializeStructuredCommand(command),
    });
  }

  quiesce(input: Readonly<{ operationId: OperationId; receiptId: string; fence: number }>): Promise<Readonly<Record<string, unknown>>> {
    return this.#bridge.request({ kind: "quiesce", protocolVersion: 1, operationId: input.operationId.value, receiptId: input.receiptId, fence: input.fence });
  }

  close(): void {
    this.#bridge.close();
  }
}

function serializeStructuredCommand(command: StructuredCommand): Readonly<Record<string, unknown>> {
  return {
    operationId: command.operationId.value,
    attemptId: command.attemptId.value,
    workspaceId: command.workspaceId.value,
    fence: command.fence,
    executable: command.executable,
    arguments: command.arguments,
    workingDirectory: command.workingDirectory,
    environment: command.environment,
  };
}
