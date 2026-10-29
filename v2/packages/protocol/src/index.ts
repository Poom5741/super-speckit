import { createHash } from "node:crypto";
import { Type, type Static, type StaticDecode, type TSchema } from "@sinclair/typebox";
import { Value } from "@sinclair/typebox/value";

export const PROTOCOL_VERSION = 1 as const;
export const OPENCODE_TARGET_COMMIT = "1eea2d4d606b3688d243033446d6ab83113431c8" as const;

abstract class Identifier<Name extends string> {
  abstract readonly kind: Name;
  constructor(readonly value: string) {}
}

export class CardId extends Identifier<"CardId"> { readonly kind = "CardId" as const; }
export class CardRevision extends Identifier<"CardRevision"> { readonly kind = "CardRevision" as const; }
export class AttemptId extends Identifier<"AttemptId"> { readonly kind = "AttemptId" as const; }
export class WorkspaceId extends Identifier<"WorkspaceId"> { readonly kind = "WorkspaceId" as const; }
export class RequestId extends Identifier<"RequestId"> { readonly kind = "RequestId" as const; }
export class OperationId extends Identifier<"OperationId"> { readonly kind = "OperationId" as const; }
export class HandoffId extends Identifier<"HandoffId"> { readonly kind = "HandoffId" as const; }
export class EvidenceId extends Identifier<"EvidenceId"> { readonly kind = "EvidenceId" as const; }
export class ArtifactId extends Identifier<"ArtifactId"> { readonly kind = "ArtifactId" as const; }
export class ProviderId extends Identifier<"ProviderId"> { readonly kind = "ProviderId" as const; }
export class RunnerId extends Identifier<"RunnerId"> { readonly kind = "RunnerId" as const; }
export class CommitId extends Identifier<"CommitId"> { readonly kind = "CommitId" as const; }

const identifier = <T extends Identifier<string>>(construct: (value: string) => T) =>
  Type.Transform(Type.String({ minLength: 1 }))
    .Decode(construct)
    .Encode((value) => value.value);

export const CardIdSchema = identifier((value) => new CardId(value));
export const CardRevisionSchema = identifier((value) => new CardRevision(value));
export const AttemptIdSchema = identifier((value) => new AttemptId(value));
export const WorkspaceIdSchema = identifier((value) => new WorkspaceId(value));
export const RequestIdSchema = identifier((value) => new RequestId(value));
export const OperationIdSchema = identifier((value) => new OperationId(value));
export const HandoffIdSchema = identifier((value) => new HandoffId(value));
export const EvidenceIdSchema = identifier((value) => new EvidenceId(value));
export const ArtifactIdSchema = identifier((value) => new ArtifactId(value));
export const ProviderIdSchema = identifier((value) => new ProviderId(value));
export const RunnerIdSchema = identifier((value) => new RunnerId(value));
export const CommitIdSchema = Type.Transform(Type.String({ pattern: "^[0-9a-f]{40,64}$" }))
  .Decode((value) => new CommitId(value))
  .Encode((value) => value.value);

export const CardKindSchema = Type.Union([Type.Literal("foundation"), Type.Literal("feature")]);
export type CardKind = Static<typeof CardKindSchema>;

export const CardContractWireSchema = Type.Object({
  schemaVersion: Type.Literal(PROTOCOL_VERSION),
  repository: Type.String({ minLength: 1 }),
  issueNodeId: Type.String({ minLength: 1 }),
  issueNumber: Type.Integer({ minimum: 1 }),
  title: Type.String({ minLength: 1 }),
  kind: CardKindSchema,
  outcome: Type.String({ minLength: 1 }),
  nonGoals: Type.Array(Type.String()),
  acceptance: Type.Array(Type.String({ minLength: 1 }), { minItems: 1 }),
  dependencies: Type.Array(Type.String({ minLength: 1 })),
  baseRef: Type.String({ minLength: 1 }),
  capability: Type.String({ minLength: 1 }),
  risk: Type.Union([Type.Literal("low"), Type.Literal("medium"), Type.Literal("high")]),
}, { additionalProperties: false });
export type CardContractWire = Static<typeof CardContractWireSchema>;

export const ConsumedCardSchema = Type.Object({
  cardId: CardIdSchema,
  revision: CardRevisionSchema,
});
export type ConsumedCard = StaticDecode<typeof ConsumedCardSchema>;

const budgetSchema = Type.Object({
  wallTimeSeconds: Type.Integer({ minimum: 1 }),
  paidUsdCents: Type.Integer({ minimum: 0 }),
});

const instantSchema = Type.String({ pattern: "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{3})?Z$" });

const claimCardCommandSchema = Type.Object({
  kind: Type.Literal("claimCard"),
  card: ConsumedCardSchema,
  attemptId: AttemptIdSchema,
  workspaceId: WorkspaceIdSchema,
  providerId: ProviderIdSchema,
  runnerId: RunnerIdSchema,
  leaseSeconds: Type.Integer({ minimum: 30, maximum: 86400 }),
  budget: budgetSchema,
});

const observeCardCommandSchema = Type.Object({
  kind: Type.Literal("observeCard"),
  cardId: CardIdSchema,
  revision: CardRevisionSchema,
  observedAt: instantSchema,
});

const recordProviderStartedSchema = Type.Object({
  kind: Type.Literal("recordProviderStarted"),
  attemptId: AttemptIdSchema,
  operationId: OperationIdSchema,
  sessionRef: Type.String({ minLength: 1 }),
});

const saveCheckpointSchema = Type.Object({
  kind: Type.Literal("saveCheckpoint"),
  attemptId: AttemptIdSchema,
  dirtyDigest: Type.Union([Type.String({ pattern: "^[0-9a-f]{64}$" }), Type.Null()]),
  completedCriteria: Type.Array(Type.String({ minLength: 1 })),
  nextAction: Type.String({ minLength: 1 }),
});

const heartbeatAttemptSchema = Type.Object({
  kind: Type.Literal("heartbeatAttempt"),
  attemptId: AttemptIdSchema,
  fence: Type.Integer({ minimum: 1 }),
  leaseSeconds: Type.Integer({ minimum: 30, maximum: 86400 }),
});

const requestCancellationSchema = Type.Object({
  kind: Type.Literal("requestCancellation"),
  attemptId: AttemptIdSchema,
  operationId: OperationIdSchema,
  reason: Type.String({ minLength: 1 }),
});

const recordStoppedSchema = Type.Object({
  kind: Type.Literal("recordStopped"),
  attemptId: AttemptIdSchema,
  operationId: OperationIdSchema,
  receiptDigest: Type.String({ pattern: "^[0-9a-f]{64}$" }),
});

const recordStopUnknownSchema = Type.Object({
  kind: Type.Literal("recordStopUnknown"),
  attemptId: AttemptIdSchema,
  operationId: OperationIdSchema,
  reason: Type.String({ minLength: 1 }),
});

const prepareHandoffSchema = Type.Object({
  kind: Type.Literal("prepareHandoff"),
  handoffId: HandoffIdSchema,
  sourceAttemptId: AttemptIdSchema,
  destinationProviderId: ProviderIdSchema,
  destinationRunnerId: RunnerIdSchema,
  capsuleDigest: Type.String({ pattern: "^[0-9a-f]{64}$" }),
});

const approveHandoffSchema = Type.Object({
  kind: Type.Literal("approveHandoff"),
  handoffId: HandoffIdSchema,
  capsuleDigest: Type.String({ pattern: "^[0-9a-f]{64}$" }),
  approvedBy: Type.String({ minLength: 1 }),
  approvedAt: instantSchema,
  expiresAt: instantSchema,
});

const activateHandoffSchema = Type.Object({
  kind: Type.Literal("activateHandoff"),
  handoffId: HandoffIdSchema,
  destinationAttemptId: AttemptIdSchema,
  destinationWorkspaceId: WorkspaceIdSchema,
});

const acknowledgeHandoffSchema = Type.Object({
  kind: Type.Literal("acknowledgeHandoff"),
  handoffId: HandoffIdSchema,
  destinationAttemptId: AttemptIdSchema,
  revision: CardRevisionSchema,
  capsuleDigest: Type.String({ pattern: "^[0-9a-f]{64}$" }),
});

const recordHandoffUnknownSchema = Type.Object({
  kind: Type.Literal("recordHandoffUnknown"),
  handoffId: HandoffIdSchema,
  reason: Type.String({ minLength: 1 }),
});

const recordEvidenceSchema = Type.Object({
  kind: Type.Literal("recordEvidence"),
  evidenceId: EvidenceIdSchema,
  attemptId: AttemptIdSchema,
  candidate: CommitIdSchema,
  criterion: Type.String({ minLength: 1 }),
  verifier: Type.String({ minLength: 1 }),
  outcome: Type.Union([
    Type.Literal("passed"),
    Type.Literal("failed"),
    Type.Literal("blocked"),
    Type.Literal("inconclusive"),
  ]),
  artifactIds: Type.Array(ArtifactIdSchema),
});

const completeAttemptSchema = Type.Object({
  kind: Type.Literal("completeAttempt"),
  attemptId: AttemptIdSchema,
  candidate: CommitIdSchema,
  requiredCriteria: Type.Array(Type.String({ minLength: 1 }), { minItems: 1 }),
  summary: Type.String({ minLength: 1 }),
});

export const RuntimeCommandSchema = Type.Union([
  observeCardCommandSchema,
  claimCardCommandSchema,
  recordProviderStartedSchema,
  saveCheckpointSchema,
  heartbeatAttemptSchema,
  requestCancellationSchema,
  recordStoppedSchema,
  recordStopUnknownSchema,
  prepareHandoffSchema,
  approveHandoffSchema,
  activateHandoffSchema,
  acknowledgeHandoffSchema,
  recordHandoffUnknownSchema,
  recordEvidenceSchema,
  completeAttemptSchema,
]);
export type RuntimeCommand = StaticDecode<typeof RuntimeCommandSchema>;

export const CommandEnvelopeSchema = Type.Object({
  protocolVersion: Type.Literal(PROTOCOL_VERSION),
  requestId: RequestIdSchema,
  principal: Type.String({ minLength: 1 }),
  expectedVersion: Type.Integer({ minimum: 0 }),
  command: RuntimeCommandSchema,
});
export type CommandEnvelope = StaticDecode<typeof CommandEnvelopeSchema>;

export const CommandReceiptSchema = Type.Union([
  Type.Object({ kind: Type.Literal("accepted"), version: Type.Integer({ minimum: 0 }), cursor: Type.Integer({ minimum: 0 }), operationId: Type.Union([OperationIdSchema, Type.Null()]) }),
  Type.Object({ kind: Type.Literal("duplicate"), version: Type.Integer({ minimum: 0 }), cursor: Type.Integer({ minimum: 0 }) }),
  Type.Object({
    kind: Type.Literal("rejected"),
    code: Type.Union([
      Type.Literal("version_conflict"),
      Type.Literal("revision_conflict"),
      Type.Literal("policy_violation"),
      Type.Literal("ownership_unresolved"),
      Type.Literal("not_found"),
    ]),
    message: Type.String({ minLength: 1 }),
  }),
]);
export type CommandReceipt = StaticDecode<typeof CommandReceiptSchema>;

export type AttemptState =
  | Readonly<{ kind: "starting"; operationId: OperationId }>
  | Readonly<{ kind: "running"; sessionRef: string }>
  | Readonly<{ kind: "stop_requested"; operationId: OperationId; reason: string }>
  | Readonly<{ kind: "stop_unknown"; operationId: OperationId; reason: string }>
  | Readonly<{ kind: "paused"; quiescenceReceipt: string }>
  | Readonly<{ kind: "failed"; reason: string }>;

export type HandoffState =
  | Readonly<{ kind: "awaiting_approval"; capsuleDigest: string }>
  | Readonly<{ kind: "approved"; capsuleDigest: string; approvedBy: string; expiresAt: string }>
  | Readonly<{ kind: "awaiting_ack"; destinationAttemptId: AttemptId; revision: CardRevision; capsuleDigest: string }>
  | Readonly<{ kind: "active"; destinationAttemptId: AttemptId }>
  | Readonly<{ kind: "handoff_unknown"; reason: string }>;

export type RuntimeEvent = Readonly<{
  cursor: number;
  aggregateId: string;
  aggregateVersion: number;
  kind: string;
  payload: Readonly<Record<string, unknown>>;
  occurredAt: string;
}>;

export type CardSnapshotWire = Readonly<{
  cardId: string;
  revision: string;
  version: number;
  observedAt: string;
  attempts: readonly Readonly<{
    attemptId: string;
    revision: string;
    workspaceId: string;
    providerId: string;
    runnerId: string;
    principal: string;
    state: Readonly<{ kind: string; details: Readonly<Record<string, unknown>> }>;
    fence: number;
    leaseExpiresAt: string;
  }>[];
  handoffs: readonly Readonly<{
    handoffId: string;
    sourceAttemptId: string;
    capsuleDigest: string;
    state: Readonly<{ kind: string; details: Readonly<Record<string, unknown>> }>;
  }>[];
}>;

export type CoordinatorQuery =
  | Readonly<{ kind: "card"; cardId: CardId }>
  | Readonly<{ kind: "events"; after: number; limit?: number }>;

export type CapabilityStatus =
  | Readonly<{ kind: "supported"; evidence: string }>
  | Readonly<{ kind: "degraded"; limits: readonly [string, ...string[]]; evidence: string }>
  | Readonly<{ kind: "unavailable"; reason: string }>;

export type CapabilityReport = Readonly<{
  providerId: ProviderId;
  version: string;
  observedAt: string;
  capabilities: Readonly<Record<string, CapabilityStatus>>;
}>;

export type ProviderOperation =
  | Readonly<{ kind: "start"; operationId: OperationId; attemptId: AttemptId; workspaceId: WorkspaceId }>
  | Readonly<{ kind: "observe"; operationId: OperationId }>
  | Readonly<{ kind: "send"; operationId: OperationId; instruction: string }>
  | Readonly<{ kind: "checkpoint"; operationId: OperationId }>
  | Readonly<{ kind: "interrupt"; operationId: OperationId }>
  | Readonly<{ kind: "collectEvidence"; operationId: OperationId }>
  | Readonly<{ kind: "release"; operationId: OperationId }>;

export type ProviderObservation =
  | Readonly<{ kind: "accepted"; operationId: OperationId; nativeRef: string }>
  | Readonly<{ kind: "completed"; operationId: OperationId; result: Readonly<Record<string, unknown>> }>
  | Readonly<{ kind: "failed"; operationId: OperationId; message: string }>
  | Readonly<{ kind: "unknown"; operationId: OperationId; reason: string }>;

export function parse<TSchemaValue extends TSchema>(schema: TSchemaValue, input: unknown): StaticDecode<TSchemaValue> {
  return Value.Decode(schema, input);
}

export function encode<TSchemaValue extends TSchema>(schema: TSchemaValue, input: StaticDecode<TSchemaValue>): Static<TSchemaValue> {
  return Value.Encode(schema, input);
}

export function stableJson(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(stableJson).join(",")}]`;
  const entries = Object.entries(value).sort(([left], [right]) => left.localeCompare(right));
  return `{${entries.map(([key, item]) => `${JSON.stringify(key)}:${stableJson(item)}`).join(",")}}`;
}

export function sha256(value: string | Uint8Array): string {
  return createHash("sha256").update(value).digest("hex");
}

export function fingerprintCard(contract: CardContractWire): CardRevision {
  const normalized: CardContractWire = {
    schemaVersion: contract.schemaVersion,
    repository: contract.repository,
    issueNodeId: contract.issueNodeId,
    issueNumber: contract.issueNumber,
    title: contract.title,
    kind: contract.kind,
    outcome: contract.outcome,
    nonGoals: [...contract.nonGoals].sort(),
    acceptance: [...contract.acceptance],
    dependencies: [...contract.dependencies].sort(),
    baseRef: contract.baseRef,
    capability: contract.capability,
    risk: contract.risk,
  };
  return new CardRevision(sha256(stableJson(normalized)));
}

export function assertNever(value: never): never {
  throw new Error(`unhandled variant: ${String(value)}`);
}
