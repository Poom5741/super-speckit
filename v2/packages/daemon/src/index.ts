import { timingSafeEqual } from "node:crypto";
import { chmod, lstat, unlink } from "node:fs/promises";
import { createServer, type IncomingMessage, type Server, type ServerResponse } from "node:http";
import { createConnection } from "node:net";
import { CardId } from "@super-speckit/protocol";
import { Coordinator } from "@super-speckit/coordinator";

export class CoordinatorDaemon {
  readonly #server: Server;
  readonly #coordinator: Coordinator;
  readonly #token: Buffer;
  readonly #socketPath: string;

  constructor(input: Readonly<{ coordinator: Coordinator; token: string; socketPath: string }>) {
    if (input.token.length < 32) throw new Error("daemon token must contain at least 32 characters");
    this.#coordinator = input.coordinator;
    this.#token = Buffer.from(input.token);
    this.#socketPath = input.socketPath;
    this.#server = createServer((request, response) => void this.#handle(request, response));
  }

  async start(): Promise<void> {
    await removeStaleSocket(this.#socketPath, false);
    await new Promise<void>((resolve, reject) => {
      this.#server.once("error", reject);
      this.#server.listen(this.#socketPath, () => {
        this.#server.off("error", reject);
        resolve();
      });
    });
    await chmod(this.#socketPath, 0o600);
  }

  async stop(): Promise<void> {
    await new Promise<void>((resolve, reject) => this.#server.close((error) => error === undefined ? resolve() : reject(error)));
    await removeStaleSocket(this.#socketPath, true);
  }

  async #handle(request: IncomingMessage, response: ServerResponse): Promise<void> {
    try {
      if (!this.#authorized(request.headers.authorization)) return send(response, 401, { error: { code: "unauthorized", message: "valid bearer token required" } });
      if (request.method !== "POST" || request.url !== "/rpc") return send(response, 404, { error: { code: "not_found", message: "RPC endpoint not found" } });
      const body = await readBody(request);
      const rpc = recordOf(JSON.parse(body), "RPC request");
      const method = rpc["method"];
      const params = rpc["params"];
      const id = rpc["id"];
      if (typeof method !== "string" || typeof id !== "string") return send(response, 400, { error: { code: "invalid_request", message: "method and string ID are required" } });
      if (method === "execute") return send(response, 200, { jsonrpc: "2.0", id, result: this.#coordinator.execute(params) });
      const input = recordOf(params, "RPC parameters");
      if (method === "query.card") {
        const card = input["cardId"];
        if (typeof card !== "string") return send(response, 400, { error: { code: "invalid_params", message: "cardId is required" } });
        const snapshot = this.#coordinator.queryCard(new CardId(card));
        return send(response, 200, { jsonrpc: "2.0", id, result: snapshot === null ? null : snapshotWire(snapshot) });
      }
      if (method === "query.events") {
        const after = input["after"];
        const limit = input["limit"];
        if (typeof after !== "number" || typeof limit !== "number") return send(response, 400, { error: { code: "invalid_params", message: "after and limit are required" } });
        return send(response, 200, { jsonrpc: "2.0", id, result: this.#coordinator.eventsAfter(after, limit) });
      }
      return send(response, 404, { error: { code: "method_not_found", message: `unknown method ${method}` } });
    } catch (error) {
      return send(response, 400, { error: { code: "request_failed", message: error instanceof Error ? error.message : "request failed" } });
    }
  }

  #authorized(header: string | undefined): boolean {
    if (header === undefined || !header.startsWith("Bearer ")) return false;
    const supplied = Buffer.from(header.slice("Bearer ".length));
    return supplied.length === this.#token.length && timingSafeEqual(supplied, this.#token);
  }
}

function snapshotWire(snapshot: NonNullable<ReturnType<Coordinator["queryCard"]>>): Readonly<Record<string, unknown>> {
  return {
    cardId: snapshot.cardId.value,
    revision: snapshot.revision.value,
    version: snapshot.version,
    observedAt: snapshot.observedAt,
    attempts: snapshot.attempts.map((attempt) => ({
      attemptId: attempt.attemptId.value,
      revision: attempt.revision.value,
      workspaceId: attempt.workspaceId,
      providerId: attempt.providerId,
      runnerId: attempt.runnerId,
      principal: attempt.principal,
      state: attempt.state,
      fence: attempt.fence,
      leaseExpiresAt: attempt.leaseExpiresAt,
    })),
    handoffs: snapshot.handoffs.map((handoff) => ({
      handoffId: handoff.handoffId.value,
      sourceAttemptId: handoff.sourceAttemptId.value,
      capsuleDigest: handoff.capsuleDigest,
      state: handoff.state,
    })),
  };
}

async function readBody(request: IncomingMessage): Promise<string> {
  const chunks: Buffer[] = [];
  let length = 0;
  for await (const chunk of request) {
    const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    length += bytes.byteLength;
    if (length > 1_048_576) throw new Error("RPC request exceeds 1 MiB");
    chunks.push(bytes);
  }
  return Buffer.concat(chunks).toString("utf8");
}

function recordOf(value: unknown, name: string): Readonly<Record<string, unknown>> {
  if (value === null || Array.isArray(value) || typeof value !== "object") throw new Error(`${name} is not an object`);
  return Object.fromEntries(Object.entries(value));
}

function send(response: ServerResponse, status: number, payload: unknown): void {
  response.writeHead(status, { "content-type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(payload));
}

async function removeStaleSocket(path: string, serverWasClosed: boolean): Promise<void> {
  try {
    const status = await lstat(path);
    if (!status.isSocket()) throw new Error(`refusing to remove non-socket coordinator path: ${path}`);
    if (!serverWasClosed && await socketAcceptsConnections(path)) {
      throw new Error(`coordinator is already listening at ${path}`);
    }
    await unlink(path);
  } catch (error) {
    if (!(error instanceof Error && "code" in error && error.code === "ENOENT")) throw error;
  }
}

function socketAcceptsConnections(path: string): Promise<boolean> {
  return new Promise((resolve) => {
    const socket = createConnection(path);
    socket.once("connect", () => {
      socket.destroy();
      resolve(true);
    });
    socket.once("error", () => resolve(false));
  });
}
