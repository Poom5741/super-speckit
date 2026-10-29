import { Plugin } from "@opencode/plugin/tui";
import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { SocketCoordinatorClient } from "@super-speckit/client";
import type { RuntimeEvent } from "@super-speckit/protocol";
import { MissionControlRpc, probeOpenCodeCompatibility } from "./rpc.ts";

type ViewName = "Home" | "Card" | "Agent lanes" | "Environment" | "Evidence" | "Release";
type MissionState = {
  connected: boolean;
  cursor: number;
  lastEvent: RuntimeEvent | null;
  message: string;
};

const views: readonly ViewName[] = ["Home", "Card", "Agent lanes", "Environment", "Evidence", "Release"];

export default Plugin.define({
  id: "super-speckit",
  async setup(context) {
    const compatibility = probeOpenCodeCompatibility(context.app.version);
    const defaults = defaultRuntimePaths();
    const socketPath = stringOption(context.options, "socketPath") ?? defaults.socketPath;
    const tokenFile = stringOption(context.options, "tokenFile") ?? defaults.tokenFile;
    let token: string | null = null;
    try { token = (await readFile(tokenFile, "utf8")).trim(); } catch { token = null; }
    const [state, updateState] = context.storage.memory<MissionState>("mission-control", {
      initial: { connected: false, cursor: 0, lastEvent: null, message: token === null ? `Run ssk2 daemon install; token file not found at ${tokenFile}` : "Connecting…" },
    });
    const cleanups: Array<() => void> = [];
    const abort = new AbortController();

    if (token !== null) {
      const rpc = new MissionControlRpc(new SocketCoordinatorClient({ socketPath, token }));
      void rpc.snapshot({ after: state.cursor }).then((snapshot) => {
        updateState((draft) => {
          draft.connected = true;
          draft.cursor = snapshot.cursor;
          draft.lastEvent = snapshot.latestEvent;
          draft.message = compatibility.status === "verified" ? "Coordinator connected" : compatibility.limitations.join(" ");
        });
        return watchEvents(rpc, snapshot.cursor, abort.signal, updateState);
      }).catch((error: unknown) => updateState((draft) => {
        draft.connected = false;
        draft.message = error instanceof Error ? error.message : "Coordinator connection failed";
      }));
    }

    for (const view of views) {
      cleanups.push(context.ui.router.register({ name: `Super-SpecKit · ${view}`, render: () => <MissionControlPage view={view} state={state} compatibility={compatibility.status} /> }));
    }
    context.keymap.layer(() => ({
      mode: "global",
      commands: [{
        id: "ssk.mission-control",
        title: "Open Super-SpecKit Mission Control",
        description: "Open card, agent, environment, evidence, and release state",
        group: "Super-SpecKit",
        bind: "ctrl+shift+s",
        palette: true,
        slash: { name: "ssk", aliases: ["mission-control"] },
        run: () => context.ui.router.navigate({ type: "plugin", name: "Super-SpecKit · Home" }),
      }],
    }));
    return () => {
      abort.abort();
      for (const cleanup of cleanups) cleanup();
    };
  },
});

function MissionControlPage(props: Readonly<{ view: ViewName; state: MissionState; compatibility: "verified" | "degraded" }>) {
  const eventText = () => props.state.lastEvent === null ? "No runtime events yet" : `${props.state.lastEvent.kind} · card ${props.state.lastEvent.aggregateId} · v${props.state.lastEvent.aggregateVersion}`;
  return <box flexDirection="column" padding={1} gap={1}>
    <box flexDirection="row" justifyContent="space-between">
      <text><strong>SUPER-SPECKIT MISSION CONTROL</strong></text>
      <text>{props.state.connected ? "● CONNECTED" : "○ OFFLINE"} · {props.compatibility.toUpperCase()}</text>
    </box>
    <text>{views.map((view) => view === props.view ? `[${view}]` : view).join("  ")}</text>
    <box border borderStyle="rounded" flexDirection="column" padding={1}>
      <text><strong>{props.view}</strong></text>
      <text>{viewDescription(props.view)}</text>
      <text>{eventText()}</text>
      <text>{props.state.message}</text>
    </box>
    <text>Ctrl+Shift+S Mission Control · keyboard-first · no writer handoff without approval</text>
  </box>;
}

function viewDescription(view: ViewName): string {
  switch (view) {
    case "Home": return "Dependency-ready cards and quiet attention signals.";
    case "Card": return "Canonical revision, writer lease, checkpoints, and handoff state.";
    case "Agent lanes": return "Permanent role identities; sessions exist only while useful.";
    case "Environment": return "Owned runners, warm environments, ports, and cleanup receipts.";
    case "Evidence": return "Candidate-bound evidence descriptors; raw artifacts stay outside Git.";
    case "Release": return "Feature Delivery Ready and Production Release Ready are separate gates.";
  }
}

async function watchEvents(rpc: MissionControlRpc, after: number, signal: AbortSignal, updateState: (mutation: (draft: MissionState) => void) => void): Promise<void> {
  for await (const event of rpc.watch(after, signal)) {
    updateState((draft) => {
      draft.connected = true;
      draft.cursor = event.cursor;
      draft.lastEvent = event;
      draft.message = "Live event stream active";
    });
  }
}

function stringOption(options: Readonly<Record<string, unknown>>, name: string): string | null {
  const value = options[name];
  return typeof value === "string" && value.length > 0 ? value : null;
}

function defaultRuntimePaths(): Readonly<{ socketPath: string; tokenFile: string }> {
  const base = process.env["XDG_STATE_HOME"] ?? (process.platform === "win32" ? process.env["LOCALAPPDATA"] : undefined) ?? join(homedir(), ".local", "state");
  const root = join(base, "super-speckit", "v2");
  return { socketPath: join(root, "coordinator.sock"), tokenFile: join(root, "daemon.token") };
}
