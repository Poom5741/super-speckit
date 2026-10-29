# Unattended runtime research: ADE, Herdr, and Cloudflare

Research snapshot: 2026-10-30, Asia/Bangkok. This note uses first-party documentation and source repositories only. Product behavior and prices can change. Version observations use the public releases available on the research date: ADE `v1.2.126`, Herdr `v0.9.5`, and OpenCode stable `v1.19.5`. OpenCode v2 is documented on its official v2 site and developed on the repository's `dev` branch, so its plugin API must be treated as a moving target until a stable v2 release is pinned.

## Recommendation

Super-SpecKit should own the work contract and coordinate interchangeable execution providers. It should not make Herdr, ADE, or Cloudflare the source of truth.

Use this composition:

1. **Super-SpecKit control plane.** GitHub Issues and Projects own card intent, revision, dependencies, status, and assignment. `.super-speckit/` is the repository-safe projection of architecture, run checkpoints, verification requirements, and redacted evidence descriptors. A local or hosted coordinator owns leases, attempts, cancellation, budgets, and provider-neutral handoff capsules.
2. **OpenCode v2 product adapter.** The plugin supplies the agents, tools, hooks, card UI, live status, and typed RPC. Run the OpenCode server as a background service so closing the TUI or desktop window does not end the run.
3. **Local execution provider.** Support both Herdr and ADE, rather than choosing one as the core. Herdr is the lighter terminal process host. ADE is the richer optional desktop, mobile, lane, automation, proof, and cross-machine provider.
4. **Remote browser provider.** Use Cloudflare Browser Run for headless web verification, recordings, screenshots, PDFs, network evidence, and live observation. Do not describe it as desktop computer use or as a durable coding-agent host.
5. **Optional hosted coordinator and worker.** Cloudflare Workflows plus Durable Objects can coordinate durable events and live clients. Cloudflare Containers can run an optional remote worker later. They should not be required for the first local release.

The card survives every provider switch. A Herdr pane, ADE chat, OpenCode session, Cloudflare browser session, or container instance is one attempt attached to a specific card revision.

## What "Herdr" means

The spelling and requested behavior match [Herdr, `herdrdev/herdr`](https://github.com/herdrdev/herdr), whose official description is "the runtime your coding agents live on." Its README explicitly names OpenCode, Codex, Claude Code, and other agent CLIs, and says it owns their terminals rather than wrapping the agents ([Herdr README](https://github.com/herdrdev/herdr#readme)). No assumption is needed after this match. The similarly named `herdr.ink` result was not used because the official repository links to `herdr.dev`.

Herdr is a background terminal server and multiplexer. Detaching a client leaves the original pane processes alive. Reattaching returns to those processes. A full Herdr server restart is different: arbitrary processes die, the layout returns, and only agents with a supported native resume reference can restart their conversation ([session state and restore](https://herdr.dev/docs/session-state/)). A machine reboot therefore does not preserve a Docker process, test watcher, or shell in memory. Super-SpecKit must checkpoint durable work before relying on session resume.

Herdr provides useful execution mechanics:

- The CLI and socket API can create worktrees, start and prompt agents, wait for lifecycle states, read pane output, send keys deliberately, and emit lifecycle events. `worktree.remove` removes the checkout but not its branch ([socket API](https://herdr.dev/docs/socket-api/), [agent automation](https://herdr.dev/docs/agent-automation/)).
- The server classifies supported agents as working, blocked, idle, done, or unknown. Screen-based detection can be wrong, and the docs warn that idle is not authorization to type into a possible approval dialog ([agents](https://herdr.dev/docs/agents/)). Super-SpecKit must use its own run completion protocol rather than equating Herdr's `idle` or `done` label with card acceptance.
- Saved SSH machines allow one TUI to observe and control several hosts. Remote commands use structured JSON over non-interactive SSH, and remote pane processes keep running when the bridge disconnects ([connecting machines](https://herdr.dev/docs/connecting-machines/), [CLI reference](https://herdr.dev/docs/cli-reference/)).
- Herdr publishes Linux, macOS, and Windows builds. Native Windows support is labeled beta, and its docs say not every native terminal and ConPTY combination has been verified. Running it through WSL is an exercised path ([install](https://herdr.dev/docs/install/), [Windows support](https://herdr.dev/docs/windows-beta/)).
- Plugins can declare commands, event hooks, panes, and link handlers. They are ordinary host executables with CLI or socket access, not a restricted plugin sandbox ([plugins](https://herdr.dev/docs/plugins/)). A Super-SpecKit Herdr plugin can render card state and launch provider-neutral commands, while the coordinator retains authority.

Herdr should not own credentials or durable product state. It inherits the host process environment and SSH setup. Saved machine profiles do not store passwords, private keys, agent tickets, or SSH control sockets. Pane history is off by default because terminal output may contain secrets, and the documentation tells users to treat saved history as private ([connecting machines](https://herdr.dev/tui/docs/connecting-machines/), [session state and restore](https://herdr.dev/docs/session-state/)). Super-SpecKit should ingest only selected, redacted outputs.

## What ADE provides

The referenced site belongs to [ADE by `arul28/ADE`](https://github.com/arul28/ADE). The website bundle names that repository, and the repository links back to `ade-app.dev`. ADE describes itself as a free, local-first environment that runs coding agents on the user's machines. Its AGPL-3.0 repository includes an MIT SDK and a documented runtime-embedding exception ([ADE README](https://github.com/arul28/ADE#readme)). This is a materially stronger integration candidate than a visual reference alone.

### Background and cross-machine execution

ADE's Brain is a per-user, always-on process. It owns projects, lanes, chats, terminals, Git operations, proof, provider sessions, and synchronization. The installer can register it with launchd on macOS, a systemd user service on Linux, or a per-user startup entry on Windows. Closing a desktop, web, phone, or terminal client does not end Brain-owned work ([architecture](https://github.com/arul28/ADE/blob/main/architecture.mdx), [machines and clients](https://github.com/arul28/ADE/blob/main/concepts/machines-and-clients.mdx)). If the machine sleeps or powers off, local execution stops; another online Brain or hosted worker is required for true off-machine continuation.

Machines can join one account and be controlled by desktop, web, iOS, or terminal clients. ADE also offers a no-account SSH path. A Linux server can run only the Brain and execute agents, builds, and tests with its own filesystem and credentials ([connect a machine](https://github.com/arul28/ADE/blob/main/getting-started/connect-machine.mdx)). This is a good fit for a future always-on Mac mini or Linux build box.

ADE documents an explicit cross-machine chat handoff. The source prepares a portable capsule, validates branch, commit, working tree, origin, model, and recent activity, records checkpoints, and uses an idempotent handoff ID. Ambiguous delivery becomes `unknown` and blocks a duplicate move until the user retries or dismisses it. The destination creates or safely reuses a lane and reconstructs a handoff chat. Source sessions remain as history ([cross-machine handoff contract](https://github.com/arul28/ADE/blob/main/docs/features/sync-and-multi-device/cross-machine-session-handoff.md)). This is the closest existing implementation to the requested provider handoff, but it still moves an ADE chat. Super-SpecKit's capsule must sit one level higher so it can target ADE, Herdr, OpenCode, or another provider.

### Workspaces, lifecycle, and automation

An ADE lane is one Git worktree and branch. It owns its chats, terminals, diff, tests, artifacts, and pull request. Lane environment initialization can allocate ports, assign a `.localhost` hostname, copy or template environment files, start Docker Compose, install dependencies from an allowlist, and run platform-specific setup ([lanes](https://github.com/arul28/ADE/blob/main/concepts/lanes.mdx), [lane runtime](https://github.com/arul28/ADE/blob/main/lanes/environment.mdx)). This directly addresses repeated Docker setup and parallel environment collisions.

ADE work sessions include agent chats, terminals, and tracked provider CLIs. Chats can run in the background and schedule wakes or cron work. Stopping a turn interrupts it but retains the transcript for resumption ([work sessions](https://github.com/arul28/ADE/blob/main/concepts/work-sessions.mdx)).

ADE's automation engine runs in the Brain, not the desktop renderer. It supports schedules, file changes, lane events, webhooks, GitHub and Linear ingress, durable cleanup, run history, verification gates, and external publishing. Its guardrails include optional agent time and idle limits, command timeouts, project and per-run budget caps, human review, path checks, secret references, and an audit trail ([automation architecture](https://github.com/arul28/ADE/blob/main/docs/features/automations/README.md), [automation guardrails](https://github.com/arul28/ADE/blob/main/docs/features/automations/guardrails.md)). These are valuable provider capabilities. Super-SpecKit should still define the common policy because other providers will not implement ADE's rule schema.

### Computer use, proof, and credentials

ADE includes browser and platform computer-use code and proof artifacts. The repository has separate capability paths for browser automation, macOS, iOS Simulator, and Windows. Its Windows port document still lists clean-machine proof gates and platform gaps, so support should be capability-probed rather than inferred from the app being installed ([computer use overview](https://github.com/arul28/ADE/blob/main/computer-use/overview.mdx), [Windows port evaluation](https://github.com/arul28/ADE/blob/main/WINDOWS_PORT.md)).

ADE stores project runtime state under `.ade/`, including the database, worktrees, artifacts, and encrypted project credentials. Machine-wide provider credentials live outside the repository in ADE's home directory ([architecture](https://github.com/arul28/ADE/blob/main/architecture.mdx)). Super-SpecKit must never copy either secret material or raw private proof into `.super-speckit/`. The repository should contain only a redacted descriptor, content hash, producer, card revision, verification result, and an access-controlled locator.

ADE's README says it is free, and the repository is AGPL-3.0. No separate paid ADE plan or service limit was found in its first-party docs on the research date. Account-backed multi-machine access still creates an external service dependency, so local and SSH operation must remain a supported fallback.

## What Cloudflare Browser Run provides

The referenced URL is a real Cloudflare product, now named Browser Run and formerly Browser Rendering. It provides headless Chrome through Quick Actions or browser sessions controlled with Playwright, Puppeteer, Chrome DevTools Protocol, or Stagehand. CDP can connect from a local host, CI runner, ADE Brain, Herdr pane, or OpenCode service ([Browser Run overview](https://developers.cloudflare.com/browser-run/), [examples](https://developers.cloudflare.com/browser-run/examples/)).

It is well suited to browser verification:

- Browser sessions have typed acquire, connect, target, Live View, close, recording, network-routing, and hostname-guardrail APIs ([binding API](https://developers.cloudflare.com/browser-run/reference/browser-binding-api/)).
- Session recording can be replayed in the Cloudflare dashboard or retrieved by session ID after close. Recordings contain per-tab event streams. Screenshots, PDFs, DOM snapshots, and network data can become Super-SpecKit evidence descriptors ([session recording](https://developers.cloudflare.com/browser-run/features/session-recording/)).
- Incognito browser contexts isolate cookies, local storage, and cache while several tasks reuse one browser process ([FAQ](https://developers.cloudflare.com/browser-run/faq/)).
- Session guardrails restrict HTTP and HTTPS destinations to allowed hostnames. They are fixed when the session starts. If no guardrail is supplied, browser network access is unrestricted ([guardrails](https://developers.cloudflare.com/browser-run/features/guardrails/)).
- An outbound Worker can route a selected hostname to a private service or add authentication without putting the credential in the browser. This path is currently limited to HTTP and Browser Run bindings, not REST-created sessions ([outbound Workers](https://developers.cloudflare.com/browser-run/features/outbound-workers/)).

Browser Run is not a persistent agent process. The default inactivity timeout is 60 seconds and can be raised to 20 minutes. An active session can last longer if commands keep arriving, but Cloudflare warns that sessions can close because of crashes, connection failures, maintenance, or deployments. Controllers must reconnect or recreate state ([limits](https://developers.cloudflare.com/browser-run/limits/), [close reasons](https://developers.cloudflare.com/browser-run/reference/browser-close-reasons/)). The session is also not a general desktop. It cannot control native IDEs, Docker Desktop, a local browser profile, or an operating-system permission dialog.

Browser Run can test a public or routed preview. It cannot reach `localhost` on a developer's Mac or WSL instance by magic. Super-SpecKit needs an authenticated preview tunnel, an ADE/Herdr local browser provider, or a Cloudflare internal/outbound routing adapter.

Current official pricing on 2026-10-30 is 10 browser minutes per day and 3 concurrent browsers on Workers Free. Workers Paid includes 10 browser hours per month and 10 average concurrent browsers, then charges $0.09 per extra browser hour and $2.00 per extra average concurrent browser ([Browser Run pricing](https://developers.cloudflare.com/browser-run/pricing/)). These figures belong in live configuration help, not hard-coded scheduler logic.

## Cloudflare as an optional hosted coordinator

Browser Run alone does not keep a coding agent alive. A hosted design can combine other Cloudflare services:

- **Workflows** persist step state, retry failed steps, sleep, wait for events or human approval, and expose pause, resume, restart, and terminate lifecycle operations. A Workflow instance may span hours or weeks. Each step has unlimited wall time but remains subject to CPU and step-count limits ([Workflows overview](https://developers.cloudflare.com/workflows/), [limits](https://developers.cloudflare.com/workflows/reference/limits/)). Workflows fit card-attempt orchestration and notification, not Git checkout execution.
- **Durable Objects** fit one live coordinator per card or run. They offer durable storage, alarms, and hibernating WebSockets, which lets mission-control clients disconnect without losing the logical coordinator ([Durable Objects overview](https://developers.cloudflare.com/durable-objects/concepts/what-are-durable-objects/), [WebSocket hibernation](https://developers.cloudflare.com/durable-objects/best-practices/websockets/)). They should project state from GitHub and the Super-SpecKit run ledger, not replace either.
- **Containers** can host an OpenCode or Super-SpecKit worker. They have lifecycle hooks, cancellation through signals or destroy, optional internet access, hostname egress policy, and secret-injecting outbound handlers. They do not guarantee a process will run for a fixed period, and their disk is ephemeral after sleep unless the design creates and restores snapshots ([container lifecycle](https://developers.cloudflare.com/containers/concepts/architecture/), [FAQ](https://developers.cloudflare.com/containers/faq/), [outbound traffic](https://developers.cloudflare.com/containers/configuration/outbound-traffic/)). Git commits and uploaded artifacts must remain the recovery path.

Cloudflare Containers require Workers Paid. On 2026-10-30, the $5 monthly plan included 25 GiB-hours of memory, 375 vCPU-minutes, and 200 GB-hours of disk; extra usage and regional egress are metered ([Containers pricing](https://developers.cloudflare.com/containers/platform/pricing/)). Workflows were available on Free and Paid plans with request, CPU, storage, and step quotas and charges ([Workflows pricing](https://developers.cloudflare.com/workflows/reference/pricing/)). Hosted execution should remain optional until local dogfooding proves the state model.

## Comparison with OpenCode v2

| Need | OpenCode v2 | Herdr | ADE | Cloudflare |
| --- | --- | --- | --- | --- |
| Work continues after UI closes | Yes, while the background or supervised server runs | Yes, while the Herdr server and pane process run | Yes, while the Brain runs | Yes, if a Workflow, Durable Object, or Container owns it; Browser Run alone does not |
| Survives host reboot | Sessions can resume, but host processes stop | Layout returns; supported agents can resume; arbitrary processes stop | Brain restarts and state remains; active processes may need recovery | Hosted state remains; container/browser processes can still be replaced |
| Isolated work | Built-in worktree APIs and workspace adapters | Worktree CLI/socket APIs | Lanes with branch, worktree, ports, Docker, and setup | Containers isolate compute; Browser contexts isolate browser storage |
| Cross-machine | Remote background service and web client; provider-specific session | SSH machine catalog and remote control | Account or SSH machines plus explicit portable handoff | Globally reachable APIs; caller supplies the work capsule |
| Browser or computer use | Plugin tools or external MCP/provider | Whatever CLI runs in a pane | Built-in browser and platform-dependent computer use | Headless Chrome only |
| Evidence | Plugin captures events, diffs, tool output | Selected terminal output and lifecycle | Proof artifacts, transcripts, diffs, test history | Recordings, screenshots, PDFs, DOM and network output |
| Cancellation | Session interrupt and tool abort signals | Agent keys, pane process control, server stop | Stop turn, automation cancellation, process ownership | Workflow terminate, container signal/destroy, browser close |
| Budgets | Plugin must add common policy | Super-SpecKit must add it | ADE has automation and usage caps | Provider quotas plus Super-SpecKit policy |
| Credentials | Host/server environment and provider auth | Host environment and SSH agent | ADE credential stores and destination-machine credentials | Worker Secrets or Secrets Store; outbound handlers can hide tokens from containers |
| Windows/WSL/macOS | Official v2 web docs recommend WSL on Windows; native clients exist | Linux, macOS, Windows beta; WSL exercised | macOS and Windows desktop, Linux Brain; Windows has documented proof gaps | Remote service, independent of developer OS |

OpenCode v2 already provides the correct extension point. One package can export server, TUI, experimental GUI, and RPC parts. The server plugin can add tools, hooks, integrations, commands, and agents; TUI and GUI parts can build the mission-control experience; RPC connects those views to shared state ([plugin overview](https://opencode.ai/v2/docs/build/plugins)). Plugins can subscribe to the public event stream, register live hooks, enforce permissions, and manage sessions ([server plugin API](https://opencode.ai/v2/docs/build/plugins/server/)). OpenCode also has background subagents, worktree APIs, and resumable child sessions ([tools](https://opencode.ai/v2/docs/tools), [agents](https://opencode.ai/v2/docs/agents)).

The v2 server can run as a shared background service or as a supervised foreground process. Clients can pair locally, connect over SSH, or use an opt-in encrypted remote tunnel. A dedicated server accepts remote clients through `--server` ([v2 web and server access](https://opencode.ai/v2/docs/cli/web)). This means the first unattended release does not need to invent another process supervisor.

OpenCode's permission rules reduce risk but do not create a sandbox. Its docs state that shell commands run with the host user's filesystem, process, and network authority and that directory inference is best effort ([v2 permissions](https://dev.opencode.ai/v2/docs/permissions/)). Super-SpecKit must apply separate workspace ownership, credential, network, and destructive-action policy.

## Provider-neutral contracts Super-SpecKit must own

### Run record

Every attempt needs a stable record independent of the provider:

```text
card identity and active card revision
attempt identity and parent attempt
provider, host, capability set, and native session reference
repository, base commit, candidate commit, worktree identity, and dirty-state digest
lease owner and expiry
accepted scope, required checks, and evidence policy
time, token, cost, and tool budgets
cancel state and cancellation acknowledgement
checkpoints, blockers, decisions, and next action
artifact descriptors and redaction status
terminal result and reason
```

### Handoff capsule

A handoff should freeze the source card revision and include the exact commit, working-tree patch or explicit refusal to transfer dirty state, verified checks, remaining acceptance criteria, environment recipe, required secrets by logical handle, artifact references, and the intended next action. The destination starts a new attempt and acknowledges the capsule fingerprint. An ambiguous acknowledgement must fence duplicate execution until reconciled. ADE's idempotent handoff and unknown-delivery behavior is a strong model for this contract.

### Credentials and evidence

The repository may contain only secret names and access-controlled locators. Local secrets remain in the OS keychain, provider CLI store, ADE store, or environment. Hosted secrets remain in the cloud secret manager. A worker receives the narrowest credential and network scope needed for its card.

Raw browser recordings, terminal transcripts, production logs, and screenshots may contain customer or credential data. Store them outside Git by default. `.super-speckit/` records the hash, producer, creation time, card revision, retention class, sensitivity, and locator. Only a reviewed, redacted artifact may be committed.

### Cancellation and budget enforcement

Cancellation is a durable state transition, not only Ctrl+C. The coordinator sets `cancel_requested`, adapters interrupt their native session, and the worker writes `cancelled` only after owned child processes have stopped or been transferred. A timeout without acknowledgement becomes `cancel_unknown` and fences destructive cleanup.

Budgets should support elapsed time, active model spend, tool calls, browser minutes, container cost, and external write count. Provider limits are inputs to this policy. They are not the policy itself.

## Deployment modes and fallbacks

1. **OpenCode only.** Run the v2 background service in macOS, Linux, or WSL. The Super-SpecKit plugin handles cards, agents, worktrees, checkpoints, and UI. Local Playwright handles browser tests. This is the minimum supported mode.
2. **OpenCode plus Herdr.** Herdr owns long-lived terminals, warm Docker, test watchers, multiple agent panes, and remote SSH machines. The OpenCode plugin remains the mission-control UI, or a Herdr plugin provides a terminal-native view. This is the lightest way to keep real processes alive after closing OpenCode's client.
3. **OpenCode plus ADE.** ADE Brain owns lanes, environment setup, background automations, proof, mobile access, and cross-machine execution. Super-SpecKit uses ADE through its CLI, RPC, or SDK, but keeps the card ledger outside ADE chat state. This is the richest local-first mode.
4. **Cloudflare browser extension.** Any local mode can send web-only verification to Browser Run when the target is reachable. Local browser testing remains the fallback for private or desktop-dependent flows.
5. **Hosted continuation.** A Workflow and Durable Object coordinate an optional Container worker. This mode continues after a laptop powers off. It requires an explicit autonomous-run action, a pushed or bundled work capsule, remote credentials, and hard cost and network limits.
6. **No runtime integration.** A developer uses the GitHub card, `AGENTS.md`, ordinary Git, tests, and CI. Super-SpecKit imports commits and CI evidence. This remains a first-class path.

## What to build first

1. Define the provider-neutral card, attempt, lease, checkpoint, artifact, budget, cancellation, and handoff schemas.
2. Implement the OpenCode v2 plugin against a pinned v2 commit or release. Add a compatibility probe because the documented v2 API is not the current stable release line.
3. Run OpenCode as a supervised background service and prove that closing and reopening the client preserves an active card attempt.
4. Add a Herdr adapter using its CLI/socket API. Prove warm Docker and agent continuation on macOS and Windows through WSL.
5. Add an ADE adapter behind capability discovery. Reuse lanes and proof, then prove one cross-machine card handoff without treating the ADE chat as canonical.
6. Add Cloudflare Browser Run as a browser specialist. Start with public preview URLs, recording, screenshot, trace, cancellation, guardrails, and budget accounting.
7. Consider Cloudflare Workflows, Durable Objects, and Containers only after local runs prove the handoff and recovery contracts.

## Unresolved questions and required experiments

- OpenCode v2 is documented but not the stable public release observed on 2026-10-30. Which commit or release will Super-SpecKit support first, and what compatibility window will the installer enforce?
- Should ADE be an optional peer product controlled through public CLI/RPC contracts, or should Super-SpecKit embed its MIT SDK? The AGPL runtime and embedding exception need a focused license review before distribution design.
- Can ADE's current packaged Windows Brain, WSL workflow, and computer-use features pass a clean Windows 11 test on the user's actual setup? Repository design documents are not a substitute for that proof.
- Which provider owns warm Docker on a machine where both Herdr and ADE are installed? Super-SpecKit must elect one environment owner per worktree and port namespace.
- What is the first supported remote preview path for Browser Run: a deployment preview, Cloudflare Tunnel, or a Worker-routed internal host?
- Which raw evidence classes may leave the developer machine, and what retention and deletion policy applies to Cloudflare recordings and ADE proof artifacts?
- Does the first hosted worker need arbitrary repository builds, or only browser verification? Browser-only remote work is far smaller and safer.
- How will GitHub card revision activation fence an already-running local pane when the host is offline from the coordinator?

## Bottom line

Herdr and ADE are both worth supporting. Herdr is the process and terminal layer. ADE is the richer development environment and remote control layer. Cloudflare Browser Run is the remote web-verification layer. OpenCode v2 is the primary product host. Super-SpecKit must remain above all four as the owner of card contracts, attempts, budgets, safe evidence, cancellation, and cross-provider handoff.
