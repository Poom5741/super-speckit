# Stacks

Stack- or technology specific experts that complement the personas with depth in one ecosystem.

A stack skill knows the idioms, traps, and best practices of one technology, its dialect, its standard library, its deployment story, its testing tools. Personas hand off to a stack expert when the work is technology bound rather than role bound.

## Shipped (batch 3)

- [`rails-expert`](rails-expert/SKILL.md), Rails 7/8 idioms: ActiveRecord, Hotwire, Sidekiq/Solid Queue, strong_migrations, RSpec.
- [`django-expert`](django-expert/SKILL.md), Django 5: ORM, DRF, signals discipline, async views, Celery, migrations.
- [`nextjs-expert`](nextjs-expert/SKILL.md), App Router, RSC, Server Actions, Cache Components, Fluid Compute.
- [`kubernetes-expert`](kubernetes-expert/SKILL.md), manifests, probes, PDB, RBAC, NetworkPolicy, GitOps, day two ops.
- [`terraform-expert`](terraform-expert/SKILL.md), modules, state, providers, drift detection, OIDC for CI.
- [`postgres-expert`](postgres-expert/SKILL.md), EXPLAIN ANALYZE, indexing, autovacuum, partitioning, logical replication.
- [`redis-expert`](redis-expert/SKILL.md), data structures, persistence, eviction, Cluster, hot keys, latency.
- [`aws-expert`](aws-expert/SKILL.md), IAM, VPC, service selection, Organizations, OIDC, cost footguns.
- [`gcp-expert`](gcp-expert/SKILL.md), projects, Workload Identity Federation, VPC Service Controls, Cloud Run, BigQuery.
- [`swift-ios-expert`](swift-ios-expert/SKILL.md), SwiftUI, Swift Concurrency, SwiftData, BGTaskScheduler, App Store submission.

## Shipped (batch 7)

- [`golang-expert`](golang-expert/SKILL.md), Go 1.22+ idioms: errors as values, context, slog, generics, race detector.
- [`rust-expert`](rust-expert/SKILL.md), ownership, lifetimes, async on tokio, error design with thiserror + anyhow.
- [`python-expert`](python-expert/SKILL.md), modern Python 3.12+: type hints, asyncio, uv, ruff, mypy strict.
- [`typescript-expert`](typescript-expert/SKILL.md), type system: narrowing, generics, branded types, `satisfies`, strict tsconfig.
- [`java-expert`](java-expert/SKILL.md), Java 21+: records, sealed, pattern matching, virtual threads, Spring Boot 3.
- [`csharp-dotnet-expert`](csharp-dotnet-expert/SKILL.md), .NET 9: minimal APIs, EF Core, AOT, records.
- [`flutter-expert`](flutter-expert/SKILL.md), Flutter 3.24+: Riverpod, Impeller, go_router, golden tests.
- [`react-native-expert`](react-native-expert/SKILL.md), RN New Arch (Fabric, TurboModules), Expo + EAS, Reanimated 3.
- [`tailwind-expert`](tailwind-expert/SKILL.md), Tailwind v4: `@theme`, OKLCH, container queries, CVA, tailwind-merge.
- [`playwright-expert`](playwright-expert/SKILL.md), e2e with user visible locators, auto-wait, fixtures, trace viewer.

See the [open roadmap issues](https://github.com/dimitris-di/lude-kit/issues?q=is%3Aissue+label%3Anew-skill) for proposals beyond batch 7.

## Authoring a stack expert

1. Open a "new skill" issue first.
2. Copy [`shared/skill-template/SKILL.md`](../../shared/skill-template/SKILL.md) into a new folder here.
3. Stack skills are most useful when they capture the **idioms** and **gotchas** that don't appear in the docs, the parts that a senior engineer in that stack has memorized.
4. Be specific about versions where the dialect has shifted (e.g., Rails 7 vs 8, Next.js App Router vs Pages).
