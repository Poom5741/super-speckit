import { AttemptId, OperationId, WorkspaceId, type CapabilityReport, type ProviderObservation } from "@super-speckit/protocol";
import { applyProviderOperation, type ProviderAdapter } from "@super-speckit/provider-sdk";

export type ConformanceCheck = Readonly<{ name: string; status: "passed" | "failed"; detail: string }>;
export type ProviderConformanceReport = Readonly<{ provider: string; capabilities: CapabilityReport; checks: readonly ConformanceCheck[] }>;

export async function runProviderConformance(adapter: ProviderAdapter): Promise<ProviderConformanceReport> {
  const capabilities = await adapter.probeCapabilities();
  const startOperation = new OperationId("conformance-start");
  const start = await applyProviderOperation(adapter, { kind: "start", operationId: startOperation, attemptId: new AttemptId("conformance-attempt"), workspaceId: new WorkspaceId("conformance-workspace") });
  const duplicate = await applyProviderOperation(adapter, { kind: "start", operationId: startOperation, attemptId: new AttemptId("conformance-attempt"), workspaceId: new WorkspaceId("conformance-workspace") });
  const observe = await adapter.observe({ kind: "observe", operationId: startOperation });
  const checks: ConformanceCheck[] = [
    check("identity", capabilities.providerId.value === adapter.id.value, `adapter=${adapter.id.value}, report=${capabilities.providerId.value}`),
    check("idempotent start", sameObservation(start, duplicate), `${start.kind}/${duplicate.kind}`),
    check("observable operation", sameObservation(start, observe), `${start.kind}/${observe.kind}`),
  ];
  const lifecycle = [
    { name: "checkpoint", operation: { kind: "checkpoint", operationId: new OperationId("conformance-checkpoint") } },
    { name: "send", operation: { kind: "send", operationId: new OperationId("conformance-send"), instruction: "conformance message" } },
    { name: "interrupt", operation: { kind: "interrupt", operationId: new OperationId("conformance-interrupt") } },
    { name: "collectEvidence", operation: { kind: "collectEvidence", operationId: new OperationId("conformance-evidence") } },
    { name: "release", operation: { kind: "release", operationId: new OperationId("conformance-release") } },
  ] as const;
  for (const item of lifecycle) {
    const first = await applyProviderOperation(adapter, item.operation);
    const second = await applyProviderOperation(adapter, item.operation);
    checks.push(check(`idempotent ${item.name}`, sameObservation(first, second), `${first.kind}/${second.kind}`));
  }
  return { provider: adapter.id.value, capabilities, checks };
}

export function assertProviderConformance(report: ProviderConformanceReport): void {
  const failed = report.checks.filter((item) => item.status === "failed");
  if (failed.length > 0) throw new Error(`${report.provider} failed provider conformance: ${failed.map((item) => item.name).join(", ")}`);
}

function sameObservation(left: ProviderObservation, right: ProviderObservation): boolean {
  return JSON.stringify(serializeObservation(left)) === JSON.stringify(serializeObservation(right));
}

function serializeObservation(observation: ProviderObservation): Readonly<Record<string, unknown>> {
  if (observation.kind === "completed") return { kind: observation.kind, operationId: observation.operationId.value, result: observation.result };
  if (observation.kind === "accepted") return { kind: observation.kind, operationId: observation.operationId.value, nativeRef: observation.nativeRef };
  if (observation.kind === "failed") return { kind: observation.kind, operationId: observation.operationId.value, message: observation.message };
  return { kind: observation.kind, operationId: observation.operationId.value, reason: observation.reason };
}

function check(name: string, passed: boolean, detail: string): ConformanceCheck {
  return { name, status: passed ? "passed" : "failed", detail };
}
