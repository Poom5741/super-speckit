import { CardId, OPENCODE_TARGET_COMMIT, type CardSnapshotWire, type CommandReceipt, type RuntimeEvent } from "@super-speckit/protocol";
import type { CoordinatorClient } from "@super-speckit/client";

export const MISSION_CONTROL_RPC_VERSION = 1 as const;
export const OPENCODE_PLUGIN_VERSION = "2.2.2" as const;

export type CompatibilityReport = Readonly<{
  status: "verified" | "degraded";
  installedVersion: string;
  verifiedPluginVersion: string;
  targetCommit: string;
  limitations: readonly string[];
}>;

export type MissionControlSnapshot = Readonly<{
  rpcVersion: typeof MISSION_CONTROL_RPC_VERSION;
  connected: boolean;
  cursor: number;
  latestEvent: RuntimeEvent | null;
  card: CardSnapshotWire | null;
}>;

export function probeOpenCodeCompatibility(installedVersion: string): CompatibilityReport {
  const verified = installedVersion === OPENCODE_PLUGIN_VERSION;
  return {
    status: verified ? "verified" : "degraded",
    installedVersion,
    verifiedPluginVersion: OPENCODE_PLUGIN_VERSION,
    targetCommit: OPENCODE_TARGET_COMMIT,
    limitations: verified ? [] : [`OpenCode ${installedVersion} is not the verified ${OPENCODE_PLUGIN_VERSION} API surface; writer controls are disabled.`],
  };
}

export class MissionControlRpc {
  readonly #client: CoordinatorClient;

  constructor(client: CoordinatorClient) {
    this.#client = client;
  }

  execute(command: unknown): Promise<CommandReceipt> {
    return this.#client.execute(command);
  }

  async snapshot(input: Readonly<{ after?: number; cardId?: string }>): Promise<MissionControlSnapshot> {
    const after = input.after ?? 0;
    const events = await this.#client.query({ kind: "events", after, limit: 100 });
    const latestEvent = events.at(-1) ?? null;
    const card = input.cardId === undefined ? null : await this.#client.query({ kind: "card", cardId: new CardId(input.cardId) });
    return { rpcVersion: MISSION_CONTROL_RPC_VERSION, connected: true, cursor: latestEvent?.cursor ?? after, latestEvent, card };
  }

  watch(after: number, signal?: AbortSignal): AsyncIterable<RuntimeEvent> {
    return signal === undefined ? this.#client.watch({ after }) : this.#client.watch({ after, signal });
  }
}
