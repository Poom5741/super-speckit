# Skills catalog

The full index of skills in this library. Use this page to browse what's available, find handoff partners, and check what's planned but not yet written.

Each entry links to the skill's `SKILL.md`, which is the canonical source of truth.

---

## Personas

Senior grade role personas an orchestrator can dispatch to. Treat them like the people you'd staff a feature with, design, build, secure, ship, support.

### SDLC personas (batch 1)

| Skill | Job in one line |
|---|---|
| [`engineering-team-lead`](personas/engineering-team-lead/SKILL.md) | Use when planning a sprint or week, breaking an epic into tickets, sizing / estimating work, sequencing tasks across people, unblocking a stuck engineer, running a standup or retro, preparing a 1:1, writing a project update, or reprioritizing in response to a fire. |
| [`principal-security-engineer`](personas/principal-security-engineer/SKILL.md) | Use when threat modeling a system or feature, reviewing code or a design for security flaws, hardening auth / authorization / sessions / secrets, responding to a suspected vulnerability or incident, evaluating dependencies for CVEs, classifying data sensitivity, or designing security controls (CSP, CORS, rate limiting, WAF rules, audit logging, encryption at rest, encryption in transit). |
| [`senior-backend-engineer`](personas/senior-backend-engineer/SKILL.md) | Use when designing, implementing, or reviewing backend code, APIs (REST, GraphQL, gRPC), services, workers, schedulers, queues, databases, and data models. |
| [`senior-devops-sre`](personas/senior-devops-sre/SKILL.md) | Use when building or fixing CI/CD pipelines, designing deploy / rollback / canary / blue green strategies, configuring observability (metrics, logs, traces, alerts, SLOs, dashboards), responding to a production incident, writing a runbook, planning capacity, or hardening the platform. |
| [`senior-frontend-engineer`](personas/senior-frontend-engineer/SKILL.md) | Use when building, reviewing, or debugging user interfaces, React, Next. |
| [`senior-product-manager`](personas/senior-product-manager/SKILL.md) | Use when scoping a product or feature, writing or reviewing a PRD / one pager / spec, defining the problem and the target user, prioritizing a roadmap or backlog (RICE, ICE, MoSCoW, Kano), drafting user stories with acceptance criteria, defining success metrics / north star / activation / retention, preparing a launch plan, or making a build / cut / defer decision. |
| [`senior-qa-test-engineer`](personas/senior-qa-test-engineer/SKILL.md) | Use when designing a test strategy for a feature or service, writing or reviewing unit / integration / e2e / contract / property tests, building test infrastructure (fixtures, factories, test DBs, golden files), investigating a flaky test, raising or lowering coverage where it matters, setting test gates in CI, or planning regression coverage for a release. |
| [`senior-technical-writer`](personas/senior-technical-writer/SKILL.md) | Use when writing or rewriting a README, API reference, user guide, tutorial, quickstart, onboarding doc, changelog, release notes, runbook prose, contributing guide, ADR / RFC polish, internal documentation, or any developer facing text. |
| [`senior-ux-designer`](personas/senior-ux-designer/SKILL.md) | Use when designing or critiquing user flows, information architecture, screen layouts, interaction patterns, microcopy, empty / error / loading states, or accessibility of a UX. |
| [`staff-software-architect`](personas/staff-software-architect/SKILL.md) | Use when designing a system, choosing a database / framework / cloud / message bus, writing an ADR or RFC, deciding build vs buy, planning capacity or scaling, reviewing an architecture diagram or proposal, sequencing a migration, or weighing technical tradeoffs at the CTO level. |

### Specialty personas (batch 4)

| Skill | Job in one line |
|---|---|
| [`senior-data-engineer`](personas/senior-data-engineer/SKILL.md) | Use when designing, building, reviewing, or operating data pipelines, warehouses, lakes, and lakehouses; batch and streaming ELT/ETL; dbt models; orchestration (Airflow, Dagster, Prefect, Mage); transformation (Spark, Flink, SQL); ingestion from Kafka, Kinesis, Pub/Sub, CDC; and storage on Snowflake, BigQuery, Redshift, Databricks, Iceberg, Delta. |
| [`senior-data-scientist`](personas/senior-data-scientist/SKILL.md) | Use when designing an experiment or A/B test, writing or reviewing an experiment proposal or analysis plan, sizing a study (power, alpha, MDE), checking an A/A test, picking a unit of randomization, choosing between A/B, multi armed bandit, switchback, or a quasi experiment (difference in differences, regression discontinuity, instrumental variable, synthetic control), analyzing results with confidence intervals and multiple testing correction, interpreting lift, defining primary and guardrail metrics, running cohort or segmentation analysis, or writing a result memo with a decision recommendation. |
| [`senior-developer-advocate`](personas/senior-developer-advocate/SKILL.md) | Use when building a sample app or demo app, writing a getting started tutorial or integration guide, preparing a conference talk or workshop, running a livestream demo or office hours, scoping a hackathon, drafting an ambassador or partner relations plan, or routing community signal back to product and engineering. |
| [`senior-embedded-engineer`](personas/senior-embedded-engineer/SKILL.md) | Use when designing, implementing, or reviewing firmware for microcontrollers and embedded devices, bringing up new hardware, writing peripheral drivers, designing RTOS task and ISR layouts, planning OTA update mechanisms, budgeting memory and power, hardening field deployments, or debugging timing, watchdog, and brownout issues. |
| [`senior-game-engineer`](personas/senior-game-engineer/SKILL.md) | Use when building, reviewing, profiling, or shipping games in Unity, Unreal (UE4, UE5), Godot, or a custom engine. |
| [`senior-ml-engineer`](personas/senior-ml-engineer/SKILL.md) | Use when designing, training, evaluating against an existing eval set, shipping, or operating classical machine learning models in production. |
| [`senior-mlops-engineer`](personas/senior-mlops-engineer/SKILL.md) | Use when operating the platform that trains, evaluates, deploys, serves, monitors, and retires ML models: building or reviewing training pipelines, model registries, feature stores, batch or online inference services, shadow and canary rollouts, drift detectors, model cards, retraining triggers, or model governance. |
| [`senior-mobile-engineer`](personas/senior-mobile-engineer/SKILL.md) | Use when planning, building, reviewing, or shipping mobile apps across iOS and Android. |
| [`senior-platform-engineer`](personas/senior-platform-engineer/SKILL.md) | Use when building or evolving an internal developer platform (IDP), designing paved roads and golden paths, shipping an internal CLI, scaffolding new services, wiring a service catalog (Backstage, Port, Roadie), standing up ephemeral preview environments per PR, building a developer portal, running user research with internal engineers, measuring time to first deploy / DX NPS / adoption, or coaching a team on product mindset for internal tooling. |

### Industry vertical personas (batch 5)

| Skill | Job in one line |
|---|---|
| [`compliance-engineer`](personas/compliance-engineer/SKILL.md) | Use when scoping, building, or running a compliance program: SOC 2 (Type 1 or Type 2), ISO 27001, ISO 27017, ISO 27018, ISO 27701, HIPAA, HITECH, PCI DSS, GDPR, CCPA, CPRA, FedRAMP, StateRAMP, FISMA, NIST 800-53, NIST CSF, Section 508, 21 CFR Part 11, SOX. |
| [`ecommerce-engineer`](personas/ecommerce-engineer/SKILL.md) | Use when building, reviewing, or operating online stores, storefronts, catalogs, carts, checkouts, inventory, order management, fulfillment, returns, and promotions. |
| [`edtech-engineer`](personas/edtech-engineer/SKILL.md) | Use when designing, implementing, or reviewing education technology: LMS, MOOCs, K-12 classroom tools, higher ed admin, assessment and proctoring, tutoring, gradebooks, parent portals, and SIS integrations. |
| [`fintech-engineer`](personas/fintech-engineer/SKILL.md) | Use when designing, implementing, or reviewing payments, money movement, accounts, balances, ledgers, settlement, reconciliation, KYC, AML, sanctions screening, disputes, chargebacks, FX, or regulated financial product surfaces. |
| [`healthcare-engineer`](personas/healthcare-engineer/SKILL.md) | Use when building, integrating, or reviewing healthcare software: patient portals, clinician tools, EHR integrations, telehealth, digital therapeutics, claims and eligibility flows, or anything that touches PHI. |

### AI engineering personas (batch 6)

| Skill | Job in one line |
|---|---|
| [`senior-ai-agent-engineer`](personas/senior-ai-agent-engineer/SKILL.md) | Use when designing, building, evaluating, or operating AI agents and agentic systems: single agent loops, planner / executor splits, orchestrator with subagents, swarms, tool using agents, ReAct style loops, and Model Context Protocol (MCP) servers. |
| [`senior-ai-safety-engineer`](personas/senior-ai-safety-engineer/SKILL.md) | Use when threat modeling an LLM or agent system, defending against prompt injection (direct and indirect), designing output safety pipelines, hardening tool use authorization, running an authorized red team set, classifying a system under EU AI Act / NIST AI RMF / ISO 42001, responding to an AI safety incident (jailbreak gone public, harmful output reported, system prompt leak), or evaluating training data privacy risk. |
| [`senior-cv-engineer`](personas/senior-cv-engineer/SKILL.md) | Use when designing, training, evaluating, or shipping computer vision systems: image classification, object detection, segmentation, OCR, document AI, video understanding, action recognition, tracking, pose estimation, depth, multi camera, augmented reality, edge inference. |
| [`senior-eval-engineer`](personas/senior-eval-engineer/SKILL.md) | Use when designing an eval set or eval harness for an LLM app, agent, RAG pipeline, classifier, or generative output; building a gold set; configuring an LLM as judge with a rubric; calibrating a judge against human raters; designing slice metrics; wiring a regression suite into CI; running a vibe check with rigor; choosing between exact match, BLEU, ROUGE, BERTScore, faithfulness, groundedness, or retrieval recall at K; computing inter rater agreement (Cohen kappa, Krippendorff alpha); auditing judge drift; or reporting eval deltas vs a baseline. |
| [`senior-fine-tuning-engineer`](personas/senior-fine-tuning-engineer/SKILL.md) | Use when scoping, justifying, running, evaluating, or operating a fine tune of an LLM or other foundation model: supervised fine tuning (SFT), direct preference optimization (DPO), RLHF or RLAIF, instruction tuning, continued pretraining, parameter efficient adapters (LoRA, QLoRA, PEFT), knowledge distillation, dataset curation, preference pair labeling, decontamination against eval, hosted fine tuning APIs (OpenAI, Anthropic, Together, Replicate), or bring your own GPU training on `Llama-3. |
| [`senior-llm-app-engineer`](personas/senior-llm-app-engineer/SKILL.md) | Use when designing, implementing, evaluating, shipping, or operating production LLM applications: chat, copilots, classification, structured extraction, summarization, drafting, and agentic flows. |
| [`senior-model-router-engineer`](personas/senior-model-router-engineer/SKILL.md) | Use when designing, building, or operating the gateway between applications and LLM or model providers: routing requests across Claude, OpenAI, Gemini, and open weights, enforcing per route SLOs, configuring provider failover, tracking cost per call site, designing prompt and semantic caches, applying per tenant rate limits, supporting BYOK (bring your own key), enforcing zero data retention (ZDR) and regional routing, or wiring gateway observability. |
| [`senior-rag-engineer`](personas/senior-rag-engineer/SKILL.md) | Use when designing, building, reviewing, or operating retrieval augmented generation systems: corpus parsing, chunking, embedding, indexing, retrieval (semantic, lexical, hybrid), reranking, citation, evaluation, and ingestion freshness. |
| [`senior-recommender-engineer`](personas/senior-recommender-engineer/SKILL.md) | Use when designing, building, evaluating, or operating production ranking and recommendation systems: feed ranking, product recommendations, search ranking, content discovery, ads relevance, related items, you may also like, up next, home feed. |
| [`senior-voice-ai-engineer`](personas/senior-voice-ai-engineer/SKILL.md) | Use when designing, building, evaluating, or operating production conversational voice systems: IVR, voice agents, voice assistants, agent voice fronts, voice cloning compliant products. |

## Capabilities

Cross role capabilities focused on a single job. Personas reach for these the way a person reaches for a power tool.

| Skill | Job in one line |
|---|---|
| [`api-contract-designer`](capabilities/api-contract-designer/SKILL.md) | Use when designing an API, writing a contract, choosing REST vs GraphQL vs gRPC, authoring OpenAPI / swagger / GraphQL SDL / proto, defining endpoints, request and response shapes, error codes, idempotency keys, pagination, webhooks, SDK surface, or stating a versioning policy. |
| [`data-modeler`](capabilities/data-modeler/SKILL.md) | Use when designing or reviewing a database schema, ERD, table, column, index, foreign key, or identifier strategy; when choosing between relational, document, or column oriented stores; when normalizing, denormalizing, picking types (money, UUID, ULID, UUIDv7, enums), planning partitions or sharding, or defining soft delete and lifecycle policy. |
| [`dependency-auditor`](capabilities/dependency-auditor/SKILL.md) | Use when reviewing dependencies, lockfile diffs, CVE alerts, supply chain risk, SBOM generation, npm audit, pip-audit, dependabot or renovate PRs, version bumps, postinstall scripts, transitive packages, or package manifests like package. |
| [`incident-commander`](capabilities/incident-commander/SKILL.md) | Use when a live production incident is happening or about to be declared, when paging fires, when user impact is suspected, when someone asks "who is IC", when a war room is being opened, or when an incident needs structured coordination. |
| [`migration-planner`](capabilities/migration-planner/SKILL.md) | Use for migration, replatform, schema change, backfill, dual write, shadow read, cutover, rollback, kill switch, expand contract, big bang, online migration, blue green, framework upgrade, cloud migration, zero downtime change. |
| [`postmortem-author`](capabilities/postmortem-author/SKILL.md) | Use when the team needs a postmortem, RCA, root cause analysis, incident writeup, blameless review, lessons learned doc, sev review, or action item list after an outage. |
| [`senior-code-reviewer`](capabilities/senior-code-reviewer/SKILL.md) | Use when reviewing a pull request, diff, patch, or code change; when leaving PR comments, requesting changes, approving, or considering LGTM; when triaging review feedback, labeling severity (blocking, strong suggestion, nit), or rewriting a vague review into a useful one. |
| [`senior-debugger`](capabilities/senior-debugger/SKILL.md) | Use when a bug, broken feature, error, exception, stack trace, crash, panic, NPE, segfault, undefined value, or intermittent failure needs root cause diagnosis. |
| [`senior-performance-engineer`](capabilities/senior-performance-engineer/SKILL.md) | Use when a system is slow, when latency or throughput regresses, when memory grows unbounded, when a hot path needs profiling, when a perf budget or regression guard is needed, or when Core Web Vitals (LCP, INP, CLS) miss target. |
| [`senior-refactorer`](capabilities/senior-refactorer/SKILL.md) | Use when refactoring, cleaning up, extracting a method or component, renaming, moving, inlining, deduping, simplifying, restructuring, addressing a code smell, or paying down technical debt without changing observable behavior. |

## Stacks

Stack specific experts that complement the personas with technology depth.

| Skill | Job in one line |
|---|---|
| [`aws-expert`](stacks/aws-expert/SKILL.md) | Use when work touches AWS: EC2, S3, RDS, Aurora, Lambda, DynamoDB, IAM, VPC, ALB, NLB, CloudFront, ECS, EKS, Fargate, SQS, SNS, EventBridge, Step Functions, CloudFormation, Secrets Manager, KMS, CloudWatch, X-Ray, AWS Organizations, SCPs, Control Tower, Route 53, ACM, WAF, GuardDuty, IAM Identity Center, or OIDC federation for CI. |
| [`csharp-dotnet-expert`](stacks/csharp-dotnet-expert/SKILL.md) | Use when writing, reviewing, or upgrading a C# / . |
| [`django-expert`](stacks/django-expert/SKILL.md) | Use when writing or debugging Django and Django REST Framework: ORM querysets, migrations, signals, admin, async views, Channels, Celery / Dramatiq / RQ tasks, ASGI / WSGI deploys, settings. |
| [`flutter-expert`](stacks/flutter-expert/SKILL.md) | Use for Flutter and Dart work on iOS and Android. |
| [`gcp-expert`](stacks/gcp-expert/SKILL.md) | Use when the request names GCP, Google Cloud, gcloud, GCE, GKE, Cloud Run, Cloud Functions, BigQuery, Cloud SQL, Spanner, Firestore, AlloyDB, Pub/Sub, Cloud Storage, GCS, VPC, Cloud Load Balancing, IAM, Workload Identity, Workload Identity Federation, Cloud KMS, Secret Manager, Cloud Logging, Cloud Monitoring, Cloud Trace, Cloud Build, Artifact Registry, VPC Service Controls, or Organization Policy. |
| [`golang-expert`](stacks/golang-expert/SKILL.md) | Use when writing, reviewing, or upgrading a Go (Golang) service anchored to Go 1. |
| [`java-expert`](stacks/java-expert/SKILL.md) | Use when writing, reviewing, or upgrading a Java service on JDK 21 LTS or newer; designing records, sealed interfaces, pattern matching, virtual threads (Project Loom), and structured concurrency; building Spring Boot 3 services (Spring Web, Spring Data JPA, Spring Security, Actuator) or evaluating Quarkus, Micronaut, Helidon for native image; tuning the JVM (G1, ZGC, heap sizing), reading JFR recordings, running async-profiler; managing Maven or Gradle builds; testing with JUnit 5, AssertJ, Mockito, and Testcontainers against real Postgres or Kafka. |
| [`kubernetes-expert`](stacks/kubernetes-expert/SKILL.md) | Use when working with Kubernetes, k8s, kubectl, manifests, YAML for Deployment, StatefulSet, DaemonSet, Service, Ingress, Gateway API, ConfigMap, Secret, RBAC, ServiceAccount, Helm charts, Kustomize overlays, CRDs, operators, controllers, HPA, VPA, PodDisruptionBudget, NetworkPolicy, Argo CD or Flux GitOps, Istio or Linkerd service mesh, EKS, GKE, AKS, kubeadm, or day two cluster operations (etcd backup, certificate rotation, control plane upgrades, node lifecycle). |
| [`nextjs-expert`](stacks/nextjs-expert/SKILL.md) | Use when building, reviewing, or debugging Next. |
| [`playwright-expert`](stacks/playwright-expert/SKILL.md) | Use when writing, reviewing, or debugging Playwright tests, setting up Playwright Test for a new project, migrating from Cypress or Selenium, designing locator strategy, fixing flaky e2e tests, configuring CI sharding and traces, building auth fixtures with storageState, adding visual regression with toHaveScreenshot, or shaping the e2e tier of a test pyramid. |
| [`postgres-expert`](stacks/postgres-expert/SKILL.md) | Use when working with PostgreSQL or Postgres on a real workload: a slow query, a missing or wrong index, a vacuum or autovacuum problem, partitioning, replication, a version upgrade, lock contention, deadlock, JSONB modeling, pgvector, or a connection pool decision. |
| [`python-expert`](stacks/python-expert/SKILL.md) | Use when writing, reviewing, or debugging modern Python (3. |
| [`rails-expert`](stacks/rails-expert/SKILL.md) | Use when writing, reviewing, or upgrading a Ruby on Rails app (Rails 7 or Rails 8); designing ActiveRecord models and queries, ActionPack controllers, Hotwire (Turbo, Stimulus, Turbo Streams) views, Sidekiq or Solid Queue workers, Action Mailer, Devise plus Pundit auth, RSpec plus factory_bot tests, and reversible migrations with strong_migrations. |
| [`react-native-expert`](stacks/react-native-expert/SKILL.md) | Use when building, reviewing, debugging, or shipping React Native apps to the App Store and Play Store. |
| [`redis-expert`](stacks/redis-expert/SKILL.md) | Use when the user mentions Redis, Valkey, cache layer design, eviction policy, RDB or AOF persistence, Sentinel, Redis Cluster, hash tags, pub/sub, Streams, consumer groups, sorted sets, hashes, lists, sets, INCR, EXPIRE, TTL, hot key, SLOWLOG, LATENCY DOCTOR, MULTI EXEC, Lua scripts, EVALSHA, pipelining, cluster slots, replicas, replicaof, ElastiCache, MemoryDB, or Memorystore. |
| [`rust-expert`](stacks/rust-expert/SKILL.md) | Use when writing, reviewing, or debugging Rust code (stable 1. |
| [`swift-ios-expert`](stacks/swift-ios-expert/SKILL.md) | Use for Swift and iOS work. |
| [`tailwind-expert`](stacks/tailwind-expert/SKILL.md) | Use when building, reviewing, or debugging Tailwind CSS interfaces, design tokens, utility classes, theming, dark mode, container queries, or component libraries built on Tailwind. |
| [`terraform-expert`](stacks/terraform-expert/SKILL.md) | Use when working with Terraform, OpenTofu, Pulumi, Terragrunt, CDKTF, or infrastructure as code in general. |
| [`typescript-expert`](stacks/typescript-expert/SKILL.md) | Use when writing, reviewing, or debugging TypeScript: designing types, authoring generics, modeling state with discriminated unions, branding IDs, configuring tsconfig and `moduleResolution`, setting up monorepo project references, picking build tooling (tsup, vite, tsx), or validating data with zod. |

---

## How to read a skill

Every skill in this library follows the same nine section structure so you can scan many of them quickly:

1. **Role**, who this skill is when invoked.
2. **When to invoke**, verbose trigger situations.
3. **Operating principles**, the opinions that shape the work.
4. **Workflow**, concrete steps the skill follows.
5. **Deliverables**, the artifacts it produces, with templates.
6. **Quality bar**, the self-verification checklist.
7. **Antipatterns**, what this skill explicitly does not do.
8. **Handoffs**, when to defer to another skill.
9. **Quick reference**, cheat sheet for reactivation.

If you're contributing, the same nine sections are required. See [`shared/style-guide.md`](../shared/style-guide.md).

## Composition example

A realistic multi agent flow that uses several skills together:

```
User: "We want to add team SSO to the dashboard."

→ senior-product-manager       writes the one-pager and success metric
→ staff-software-architect     picks SAML vs OIDC, writes the ADR
→ principal-security-engineer  threat models the auth flow
→ senior-ux-designer           flows the sign in + invite + role switch
→ senior-frontend-engineer     implements the UI
→ senior-backend-engineer      implements the endpoints + sessions
→ senior-qa-test-engineer      writes the regression suite
→ senior-devops-sre            rolls out behind a flag, sets the SLOs
→ senior-technical-writer      writes the admin doc and the release notes
```

Each skill knows which skill to hand off to next, see the **Handoffs** section of any `SKILL.md`.
