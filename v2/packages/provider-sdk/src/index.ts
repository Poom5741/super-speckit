import {
  OperationId,
  ProviderId,
  type CapabilityReport,
  type CapabilityStatus,
  type ProviderObservation,
  type ProviderOperation,
  assertNever,
} from "@super-speckit/protocol";

export interface ProviderAdapter {
  readonly id: ProviderId;
  probeCapabilities(): Promise<CapabilityReport>;
  start(operation: Extract<ProviderOperation, { kind: "start" }>): Promise<ProviderObservation>;
  observe(operation: Extract<ProviderOperation, { kind: "observe" }>): Promise<ProviderObservation>;
  checkpoint(operation: Extract<ProviderOperation, { kind: "checkpoint" }>): Promise<ProviderObservation>;
  send(operation: Extract<ProviderOperation, { kind: "send" }>): Promise<ProviderObservation>;
  interrupt(operation: Extract<ProviderOperation, { kind: "interrupt" }>): Promise<ProviderObservation>;
  collectEvidence(operation: Extract<ProviderOperation, { kind: "collectEvidence" }>): Promise<ProviderObservation>;
  release(operation: Extract<ProviderOperation, { kind: "release" }>): Promise<ProviderObservation>;
}

export type ProviderRequirement = Readonly<{ name: string; required: boolean; weight: number }>;
export type ProviderScore = Readonly<{ providerId: ProviderId; eligible: boolean; score: number; reasons: readonly string[] }>;

export function scoreProvider(report: CapabilityReport, requirements: readonly ProviderRequirement[]): ProviderScore {
  let score = 0;
  const reasons: string[] = [];
  for (const requirement of requirements) {
    const status = report.capabilities[requirement.name];
    if (status === undefined || status.kind === "unavailable") {
      reasons.push(`${requirement.name} is unavailable`);
      if (requirement.required) return { providerId: report.providerId, eligible: false, score: 0, reasons };
      continue;
    }
    if (status.kind === "supported") score += requirement.weight;
    if (status.kind === "degraded") {
      score += requirement.weight / 2;
      reasons.push(`${requirement.name} is degraded: ${status.limits.join(", ")}`);
    }
  }
  return { providerId: report.providerId, eligible: true, score, reasons };
}

export async function applyProviderOperation(adapter: ProviderAdapter, operation: ProviderOperation): Promise<ProviderObservation> {
  switch (operation.kind) {
    case "start": return adapter.start(operation);
    case "observe": return adapter.observe(operation);
    case "checkpoint": return adapter.checkpoint(operation);
    case "send": return adapter.send(operation);
    case "interrupt": return adapter.interrupt(operation);
    case "collectEvidence": return adapter.collectEvidence(operation);
    case "release": return adapter.release(operation);
    default: return assertNever(operation);
  }
}

export abstract class IdempotentProvider implements ProviderAdapter {
  readonly #observations = new Map<string, ProviderObservation>();
  abstract readonly id: ProviderId;
  abstract probeCapabilities(): Promise<CapabilityReport>;

  protected abstract perform(operation: ProviderOperation): Promise<ProviderObservation>;

  async start(operation: Extract<ProviderOperation, { kind: "start" }>): Promise<ProviderObservation> { return this.#once(operation); }
  async observe(operation: Extract<ProviderOperation, { kind: "observe" }>): Promise<ProviderObservation> {
    return this.#observations.get(operation.operationId.value) ?? { kind: "unknown", operationId: operation.operationId, reason: "operation has not been observed" };
  }
  async checkpoint(operation: Extract<ProviderOperation, { kind: "checkpoint" }>): Promise<ProviderObservation> { return this.#once(operation); }
  async send(operation: Extract<ProviderOperation, { kind: "send" }>): Promise<ProviderObservation> { return this.#once(operation); }
  async interrupt(operation: Extract<ProviderOperation, { kind: "interrupt" }>): Promise<ProviderObservation> { return this.#once(operation); }
  async collectEvidence(operation: Extract<ProviderOperation, { kind: "collectEvidence" }>): Promise<ProviderObservation> { return this.#once(operation); }
  async release(operation: Extract<ProviderOperation, { kind: "release" }>): Promise<ProviderObservation> { return this.#once(operation); }

  protected remember(operationId: OperationId, observation: ProviderObservation): ProviderObservation {
    this.#observations.set(operationId.value, observation);
    return observation;
  }

  async #once(operation: ProviderOperation): Promise<ProviderObservation> {
    const prior = this.#observations.get(operation.operationId.value);
    if (prior !== undefined) return prior;
    const observation = await this.perform(operation);
    return this.remember(operation.operationId, observation);
  }
}

export class FakeProvider extends IdempotentProvider {
  readonly id = new ProviderId("fake");
  readonly #mode: "succeed" | "unknown" | "fail";

  constructor(mode: "succeed" | "unknown" | "fail" = "succeed") {
    super();
    this.#mode = mode;
  }

  async probeCapabilities(): Promise<CapabilityReport> {
    const supported: CapabilityStatus = { kind: "supported", evidence: "deterministic fake provider" };
    return { providerId: this.id, version: "fixture-1", observedAt: new Date(0).toISOString(), capabilities: { writer: supported, checkpoint: supported, evidence: supported } };
  }

  protected async perform(operation: ProviderOperation): Promise<ProviderObservation> {
    if (this.#mode === "unknown") return { kind: "unknown", operationId: operation.operationId, reason: "fixture acknowledgement loss" };
    if (this.#mode === "fail") return { kind: "failed", operationId: operation.operationId, message: "fixture failure" };
    return { kind: "completed", operationId: operation.operationId, result: { operation: operation.kind } };
  }
}
