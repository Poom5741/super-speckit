import assert from "node:assert/strict";
import test from "node:test";
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { SocketCoordinatorClient } from "@super-speckit/client";
import { Coordinator } from "@super-speckit/coordinator";
import { CardId } from "@super-speckit/protocol";
import { CoordinatorDaemon } from "./index.ts";

test("the daemon preserves coordinator state across separate clients", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-daemon-"));
  const socketPath = join(directory, "coordinator.sock");
  const token = "a".repeat(32);
  const coordinator = new Coordinator({ databasePath: join(directory, "runtime.sqlite") });
  const daemon = new CoordinatorDaemon({ coordinator, socketPath, token });
  await daemon.start();
  const client = new SocketCoordinatorClient({ socketPath, token });
  const receipt = await client.execute({
    protocolVersion: 1,
    requestId: "request-1",
    principal: "tester",
    expectedVersion: 0,
    command: { kind: "observeCard", cardId: "card-1", revision: "a".repeat(64), observedAt: "2026-10-30T00:00:00.000Z" },
  });
  assert.equal(receipt.kind, "accepted");
  const snapshot = await client.query({ kind: "card", cardId: new CardId("card-1") });
  assert.equal(snapshot?.version, 1);
  await daemon.stop();
  coordinator.close();
});

test("a restarted daemon reconstructs state from the WAL-backed ledger", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-daemon-restart-"));
  const databasePath = join(directory, "runtime.sqlite");
  const socketPath = join(directory, "coordinator.sock");
  const token = "b".repeat(32);
  const firstCoordinator = new Coordinator({ databasePath });
  const firstDaemon = new CoordinatorDaemon({ coordinator: firstCoordinator, socketPath, token });
  await firstDaemon.start();
  const firstClient = new SocketCoordinatorClient({ socketPath, token });
  assert.equal((await firstClient.execute({ protocolVersion: 1, requestId: "restart-observe", principal: "tester", expectedVersion: 0, command: { kind: "observeCard", cardId: "card-restart", revision: "f".repeat(64), observedAt: "2026-10-30T00:00:00.000Z" } })).kind, "accepted");
  await firstDaemon.stop();
  firstCoordinator.close();
  const secondCoordinator = new Coordinator({ databasePath });
  const secondDaemon = new CoordinatorDaemon({ coordinator: secondCoordinator, socketPath, token });
  await secondDaemon.start();
  const restored = await new SocketCoordinatorClient({ socketPath, token }).query({ kind: "card", cardId: new CardId("card-restart") });
  assert.equal(restored?.version, 1);
  await secondDaemon.stop();
  secondCoordinator.close();
});

test("daemon startup refuses to unlink a non-socket path", async () => {
  const directory = await mkdtemp(join(tmpdir(), "ssk-daemon-safe-path-"));
  const socketPath = join(directory, "coordinator.sock");
  await writeFile(socketPath, "do not delete");
  const coordinator = new Coordinator({ databasePath: join(directory, "runtime.sqlite") });
  const daemon = new CoordinatorDaemon({ coordinator, socketPath, token: "c".repeat(32) });
  await assert.rejects(daemon.start(), /refusing to remove non-socket/);
  coordinator.close();
});
