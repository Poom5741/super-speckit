import { execFile } from "node:child_process";
import { promisify } from "node:util";
import {
  OperationId,
  ProviderId,
  type CapabilityReport,
  type ProviderObservation,
  type ProviderOperation,
} from "@super-speckit/protocol";
import { IdempotentProvider } from "@super-speckit/provider-sdk";

const executeFile = promisify(execFile);

export class ExternalBridgeProvider extends IdempotentProvider {
  readonly id: ProviderId;
  readonly #executable: string | null;
  readonly #versionArguments: readonly string[];
  readonly #bridgeArguments: readonly string[];
  readonly #name: string;

  constructor(input: Readonly<{ id: string; name: string; executable: string | null; versionArguments?: readonly string[]; bridgeArguments?: readonly string[] }>) {
    super();
    this.id = new ProviderId(input.id);
    this.#name = input.name;
    this.#executable = input.executable;
    this.#versionArguments = input.versionArguments ?? ["--version"];
    this.#bridgeArguments = input.bridgeArguments ?? ["super-speckit", "bridge"];
  }

  async probeCapabilities(): Promise<CapabilityReport> {
    if (this.#executable === null) {
      return {
        providerId: this.id,
        version: "unavailable",
        observedAt: new Date().toISOString(),
        capabilities: { writer: { kind: "unavailable", reason: `${this.#name} bridge executable is not configured` } },
      };
    }
    try {
      const { stdout, stderr } = await executeFile(this.#executable, [...this.#versionArguments]);
      const version = `${stdout}${stderr}`.trim() || "observed";
      return {
        providerId: this.id,
        version,
        observedAt: new Date().toISOString(),
        capabilities: {
          observation: { kind: "supported", evidence: `${this.#name} process responded to its version probe` },
          writer: { kind: "degraded", limits: ["writer support requires the reviewed Super-SpecKit JSON bridge"], evidence: this.#executable },
        },
      };
    } catch (error) {
      return {
        providerId: this.id,
        version: "unavailable",
        observedAt: new Date().toISOString(),
        capabilities: { writer: { kind: "unavailable", reason: error instanceof Error ? error.message : `${this.#name} probe failed` } },
      };
    }
  }

  protected async perform(operation: ProviderOperation): Promise<ProviderObservation> {
    if (this.#executable === null) return { kind: "failed", operationId: operation.operationId, message: `${this.#name} bridge executable is not configured` };
    try {
      const payload = JSON.stringify(serializeOperation(operation));
      const { stdout } = await executeFile(this.#executable, [...this.#bridgeArguments, payload]);
      const response = parseBridgeResponse(stdout, operation.operationId);
      return response;
    } catch (error) {
      return { kind: "unknown", operationId: operation.operationId, reason: error instanceof Error ? error.message : `${this.#name} bridge acknowledgement failed` };
    }
  }
}

export function createHerdrProvider(executable: string | null): ExternalBridgeProvider {
  return new ExternalBridgeProvider({ id: "herdr", name: "Herdr", executable });
}

export function createAdeProvider(executable: string | null): ExternalBridgeProvider {
  return new ExternalBridgeProvider({ id: "ade", name: "ADE", executable });
}

export type BrowserSession = Readonly<{ sessionId: string; liveViewUrl: string | null; recordingRef: string | null }>;

export class CloudflareBrowserProvider extends IdempotentProvider {
  readonly id = new ProviderId("cloudflare-browser-run");
  readonly #endpoint: URL | null;
  readonly #token: string | null;
  readonly #allowedHosts: ReadonlySet<string>;
  readonly #fetch: typeof fetch;

  constructor(input: Readonly<{ endpoint: string | null; token: string | null; allowedHosts: readonly string[]; fetch?: typeof fetch }>) {
    super();
    this.#endpoint = input.endpoint === null ? null : new URL(input.endpoint);
    this.#token = input.token;
    this.#allowedHosts = new Set(input.allowedHosts);
    this.#fetch = input.fetch ?? fetch;
  }

  async probeCapabilities(): Promise<CapabilityReport> {
    if (this.#endpoint === null || this.#token === null) {
      return { providerId: this.id, version: "unavailable", observedAt: new Date().toISOString(), capabilities: { browser: { kind: "unavailable", reason: "Browser Run endpoint or token is not configured" } } };
    }
    return {
      providerId: this.id,
      version: "configured-endpoint",
      observedAt: new Date().toISOString(),
      capabilities: {
        browser: { kind: "supported", evidence: this.#endpoint.origin },
        writer: { kind: "unavailable", reason: "Browser Run never receives repository writer authority" },
      },
    };
  }

  assertAllowedTarget(target: string): URL {
    const url = new URL(target);
    if (url.protocol !== "https:" || !this.#allowedHosts.has(url.hostname)) throw new Error(`browser target is not allowlisted: ${url.hostname}`);
    return url;
  }

  protected async perform(operation: ProviderOperation): Promise<ProviderObservation> {
    if (this.#endpoint === null || this.#token === null) return { kind: "failed", operationId: operation.operationId, message: "Browser Run is not configured" };
    const response = await this.#fetch(new URL("operations", this.#endpoint), {
      method: "POST",
      headers: { authorization: `Bearer ${this.#token}`, "content-type": "application/json" },
      body: JSON.stringify(serializeOperation(operation)),
    });
    if (!response.ok) return { kind: "unknown", operationId: operation.operationId, reason: `Browser Run returned HTTP ${response.status}` };
    const body: unknown = await response.json();
    if (body === null || Array.isArray(body) || typeof body !== "object") return { kind: "unknown", operationId: operation.operationId, reason: "Browser Run returned an invalid observation" };
    return { kind: "completed", operationId: operation.operationId, result: Object.fromEntries(Object.entries(body)) };
  }
}

function serializeOperation(operation: ProviderOperation): Readonly<Record<string, unknown>> {
  const base = { kind: operation.kind, operationId: operation.operationId.value };
  switch (operation.kind) {
    case "start": return { ...base, attemptId: operation.attemptId.value, workspaceId: operation.workspaceId.value };
    case "send": return { ...base, instruction: operation.instruction };
    case "observe":
    case "checkpoint":
    case "interrupt":
    case "collectEvidence":
    case "release": return base;
  }
}

function parseBridgeResponse(raw: string, operationId: OperationId): ProviderObservation {
  const value: unknown = JSON.parse(raw);
  if (value === null || Array.isArray(value) || typeof value !== "object") return { kind: "unknown", operationId, reason: "bridge returned a non-object response" };
  const record = Object.fromEntries(Object.entries(value));
  if (record["kind"] === "completed" && record["result"] !== null && !Array.isArray(record["result"]) && typeof record["result"] === "object") {
    return { kind: "completed", operationId, result: Object.fromEntries(Object.entries(record["result"])) };
  }
  if (record["kind"] === "failed" && typeof record["message"] === "string") return { kind: "failed", operationId, message: record["message"] };
  return { kind: "unknown", operationId, reason: typeof record["reason"] === "string" ? record["reason"] : "bridge did not return a recognized observation" };
}
