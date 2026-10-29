import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { cleanupExpiredArtifacts, inspectRawArtifact, preserveArtifact, writeRetentionState } from "./index.ts";

test("raw evidence stays outside Git while a redacted descriptor is projected", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-evidence-"));
  const repository = join(directory, "repo");
  const stateRoot = join(directory, "state");
  const source = join(directory, "browser-recording.bin");
  await writeFile(source, "private customer-looking payload");
  const descriptor = await preserveArtifact({ stateRoot, repository, sourcePath: source, mediaType: "application/octet-stream", kind: "browser-recording", now: new Date("2026-01-01T00:00:00.000Z") });
  await writeRetentionState(stateRoot, descriptor);
  const projected = await readFile(join(repository, ".super-speckit", "evidence", `${descriptor.artifactId}.json`), "utf8");
  assert.doesNotMatch(projected, /private customer-looking payload/);
  assert.deepEqual(await inspectRawArtifact(stateRoot, descriptor), { exists: true, digestMatches: true });
  assert.deepEqual(await cleanupExpiredArtifacts({ stateRoot, now: new Date("2026-02-01T00:00:00.000Z") }), [descriptor.artifactId]);
  assert.deepEqual(await inspectRawArtifact(stateRoot, descriptor), { exists: false, digestMatches: false });
});

test("pinned evidence survives retention cleanup", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-evidence-pinned-"));
  const source = join(directory, "proof.txt");
  await writeFile(source, "proof");
  const descriptor = await preserveArtifact({ stateRoot: join(directory, "state"), repository: join(directory, "repo"), sourcePath: source, mediaType: "text/plain", kind: "log", pinned: true, retentionDays: 1, now: new Date("2026-01-01T00:00:00.000Z") });
  await writeRetentionState(join(directory, "state"), descriptor);
  assert.deepEqual(await cleanupExpiredArtifacts({ stateRoot: join(directory, "state"), now: new Date("2027-01-01T00:00:00.000Z") }), []);
});
