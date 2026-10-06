---
name: tiktok-work-break
description: Enable TikTok work-break mode when requested, opening TikTok during independent agent work and closing the managed tab before asking for human judgment or input.
---

# TikTok work break

Use when the user asks for TikTok while the agent works or enables this mode. Loading or installing the skill alone does not enable it for unrelated users or chats. Once enabled, keep the preference for the active chat until the user disables it. Continue the user's actual task; opening TikTok is a companion action, not completion of that task.

## Independent work

At the start of a substantial independent work phase, open `https://www.tiktok.com/` visibly using available browser tools. Respect a user-selected browser; otherwise use the host's visible in-app browser when available. Inspect the resulting page state and record the browser ID and tab ID returned by the tools. Keep the tab open across tool calls and turn boundaries with the host's supported tab lifecycle mechanism.

Reuse this mode's existing managed tab instead of creating duplicates. Do not adopt a pre-existing user tab without explicit authorization to close that tab. Do not operate the feed, like posts, or change account settings as part of this skill. Let the user browse while the agent continues working. Keep unrelated research tabs hidden where the browser tools support it.

## Human judgment needed

Immediately before presenting a decision, approval request, missing-information question, or login handoff that needs the user's response, close only the recorded managed tab. Verify its closure and bring the chat into view with available host navigation tools when supported. Then present the concrete question and explain the decision plainly. This applies to asynchronous questions as well as final questions. TikTok remains closed while the question is pending.

After the user answers and independent work resumes, reopen TikTok and record the new tab identity. Do not open and close it for ordinary progress messages or a completion receipt that needs no answer. Keep it open at completion if the user is still watching, using the host's keep-open mechanism.

## Ownership and recovery

Track `enabled`, `browser_id`, `managed_tab_id`, and `pending_user_input` in the chat's runtime state. If durable resumption is needed, use a Git-ignored local QA/session artifact with a chat identifier; do not create a global preference or store browsing history. A stale tab ID requires inspecting current tab inventory. Do not close a tab based only on a matching TikTok URL. If ownership cannot be established, leave it open and report that automatic closure could not be verified.

If the user navigates the managed tab away from TikTok or takes it over for unrelated work, relinquish ownership and avoid closing it. If they close it themselves, do not reopen it until the next independent work phase. On disabling the mode, stop automation and close an owned TikTok tab only when the user's request includes that action.

If browser controls are unavailable, continue the primary work and explain the limitation once. If TikTok requires login, age verification, or another user action, follow the host's normal browser rules; do not force an interruption just to enable entertainment. This is an agent-driven convention, not a background watcher: transitions occur only while the agent is executing and browser tools are available.
