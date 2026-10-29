import { createHash, randomUUID } from "node:crypto";
import { copyFile, mkdir, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
import { join } from "node:path";

export type ArtifactDescriptor = Readonly<{
  schemaVersion: 1;
  artifactId: string;
  digest: string;
  bytes: number;
  mediaType: string;
  kind: string;
  createdAt: string;
  expiresAt: string;
  pinned: boolean;
  localHandle: string;
}>;

export async function preserveArtifact(input: Readonly<{
  stateRoot: string;
  repository: string;
  sourcePath: string;
  mediaType: string;
  kind: string;
  pinned?: boolean;
  retentionDays?: number;
  now?: Date;
}>): Promise<ArtifactDescriptor> {
  const now = input.now ?? new Date();
  const retentionDays = input.retentionDays ?? 30;
  if (!Number.isSafeInteger(retentionDays) || retentionDays < 1) throw new Error("retentionDays must be a positive integer");
  const bytes = await readFile(input.sourcePath);
  const digest = createHash("sha256").update(bytes).digest("hex");
  const artifactId = randomUUID();
  const rawDirectory = join(input.stateRoot, "artifacts", artifactId);
  await mkdir(rawDirectory, { recursive: true, mode: 0o700 });
  await copyFile(input.sourcePath, join(rawDirectory, "raw"));
  const descriptor: ArtifactDescriptor = {
    schemaVersion: 1,
    artifactId,
    digest,
    bytes: bytes.byteLength,
    mediaType: safeLabel(input.mediaType, "mediaType"),
    kind: safeLabel(input.kind, "kind"),
    createdAt: now.toISOString(),
    expiresAt: new Date(now.getTime() + retentionDays * 86_400_000).toISOString(),
    pinned: input.pinned ?? false,
    localHandle: `ssk-artifact:${artifactId}`,
  };
  await writeRetentionState(input.stateRoot, descriptor);
  const descriptorDirectory = join(input.repository, ".super-speckit", "evidence");
  await mkdir(descriptorDirectory, { recursive: true });
  await writeFile(join(descriptorDirectory, `${artifactId}.json`), `${JSON.stringify(descriptor, null, 2)}\n`, { flag: "wx" });
  return descriptor;
}

export async function cleanupExpiredArtifacts(input: Readonly<{ stateRoot: string; now?: Date }>): Promise<readonly string[]> {
  const root = join(input.stateRoot, "artifacts");
  let entries: string[];
  try { entries = await readdir(root); } catch (error) { if (isMissing(error)) return []; throw error; }
  const removed: string[] = [];
  for (const artifactId of entries) {
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(artifactId)) continue;
    const directory = join(root, artifactId);
    const descriptorPath = join(directory, "retention.json");
    let retention: unknown;
    try { retention = JSON.parse(await readFile(descriptorPath, "utf8")); } catch (error) {
      if (isMissing(error)) continue;
      throw error;
    }
    const record = recordOf(retention);
    if (record["pinned"] === true) continue;
    const expiresAt = record["expiresAt"];
    if (typeof expiresAt !== "string" || Date.parse(expiresAt) > (input.now ?? new Date()).getTime()) continue;
    await rm(directory, { recursive: true });
    removed.push(artifactId);
  }
  return removed;
}

export async function writeRetentionState(stateRoot: string, descriptor: ArtifactDescriptor): Promise<void> {
  const path = join(stateRoot, "artifacts", descriptor.artifactId, "retention.json");
  await writeFile(path, `${JSON.stringify({ artifactId: descriptor.artifactId, expiresAt: descriptor.expiresAt, pinned: descriptor.pinned }, null, 2)}\n`, { mode: 0o600 });
}

export async function inspectRawArtifact(stateRoot: string, descriptor: ArtifactDescriptor): Promise<Readonly<{ exists: boolean; digestMatches: boolean }>> {
  const path = join(stateRoot, "artifacts", descriptor.artifactId, "raw");
  try {
    const metadata = await stat(path);
    if (!metadata.isFile()) return { exists: false, digestMatches: false };
    const bytes = await readFile(path);
    return { exists: true, digestMatches: createHash("sha256").update(bytes).digest("hex") === descriptor.digest };
  } catch (error) {
    if (isMissing(error)) return { exists: false, digestMatches: false };
    throw error;
  }
}

function safeLabel(value: string, name: string): string {
  if (!/^[a-zA-Z0-9][a-zA-Z0-9.+/_-]{0,127}$/.test(value)) throw new Error(`${name} contains unsafe descriptor characters`);
  return value;
}

function recordOf(value: unknown): Readonly<Record<string, unknown>> {
  if (value === null || Array.isArray(value) || typeof value !== "object") throw new Error("retention state is not an object");
  return Object.fromEntries(Object.entries(value));
}

function isMissing(error: unknown): boolean {
  return error instanceof Error && "code" in error && error.code === "ENOENT";
}
