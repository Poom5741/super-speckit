# Super-SpecKit V2 change story

```mermaid
flowchart LR
  GH[GitHub card intent] --> C[Owned coordinator]
  C --> DB[(SQLite WAL ledger)]
  C --> OC[OpenCode Mission Control]
  C --> R[Native or persistent WSL runner]
  C --> P[Provider adapters]
  P --> H[Herdr]
  P --> A[ADE]
  P --> B[Cloudflare Browser Run]
  DB --> E[Redacted repository evidence]
  E --> GH
  C --> X{Writer handoff approved?}
  X -->|No| F[Fence destination writes]
  X -->|Yes plus source quiescence| D[Destination attempt]
```

GitHub owns card intent; repository ADRs and tests own technical truth; the coordinator alone writes runtime state. Provider adapters never become competing ledgers. Writer transfer requires a frozen capsule, source quiescence, and explicit approval for that exact capsule. Local tests prove these boundaries, while live Herdr, ADE, Cloudflare, Windows/WSL, and `whitelabels-cex` journeys remain release gates.
