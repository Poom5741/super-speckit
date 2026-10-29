import { Plugin } from "@opencode/plugin";
import { probeOpenCodeCompatibility } from "./rpc.ts";

export default Plugin.define({
  id: "super-speckit",
  async setup(context) {
    const compatibility = probeOpenCodeCompatibility(context.app.version);
    const registration = await context.command.transform((commands) => {
      commands.add({
        name: "ssk",
        description: compatibility.status === "verified"
          ? "Open Super-SpecKit Mission Control in the TUI"
          : `Super-SpecKit is in degraded read-only mode: ${compatibility.limitations.join(" ")}`,
        async execute(input) {
          await context.session.synthetic({
            sessionID: input.sessionID,
            text: compatibility.status === "verified" ? "Open Mission Control with the TUI /ssk command." : compatibility.limitations.join(" "),
            resume: false,
          });
        },
      });
    });
    return () => registration.dispose();
  },
});

export { MissionControlRpc, probeOpenCodeCompatibility } from "./rpc.ts";
