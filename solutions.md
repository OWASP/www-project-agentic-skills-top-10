# Open Source Tools Supporting AST10 Mitigations

This page catalogs open source tools that implement mitigations for one or more AST10 risks. Listings are factual and vendor-neutral. Inclusion does not imply OWASP endorsement.

## How to Add a Tool

Submit a PR adding your tool using the template at the bottom of this page. All fields are required. Entries that read as promotional will be asked to revise.

## Summary


| Tool                                                                               | License | AST Risks Addressed                             | Language |
| ---------------------------------------------------------------------------------- | ------- | ----------------------------------------------- | -------- |
| [AgentMint](https://github.com/aniketh-maddipati/agentmint-python)| MIT     | AST01, AST02, AST03, AST04, AST07, AST08, AST09 | Python   |
| [EMILIA Protocol](https://github.com/emiliaprotocol/emilia-protocol)| Apache-2.0 | AST03, AST04, AST07, AST09 | TypeScript, JavaScript, Python, Go |
| [Nobulex](https://github.com/arian-gogani/nobulex)| MIT     | AST03, AST04, AST07, AST09                       | Python, TypeScript |
| [SkilLock](https://github.com/skills-lock/skil-lock)| Apache-2.0 | AST03, AST04, AST07, AST08, AST09, AST10 | Go   |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector)| Apache-2.0 | AST01, AST02, AST03, AST04, AST08, AST09, AST10 | Python   |


---

## AgentMint

**Description:** Runtime enforcement and signed evidence for AI agent tool calls. Evaluates every tool call against a human-approved scope before execution. Produces cryptographically signed, hash-chained receipts for every decision (allow or deny).

**License:** MIT  
**Repository:** [https://github.com/aniketh-maddipati/agentmint-python](https://github.com/aniketh-maddipati/agentmint-python)  
**Install:** `pip install agentmint`  
**Dependencies:** 2 (pynacl, requests)

### AST Risks Addressed

**AST01 — Malicious Skills:** Ed25519 signatures and SHA-256 hash chains on every receipt provide tamper-evident audit trails. Evidence packages are independently verifiable without vendor software.

**AST02 — Supply Chain Compromise:** Signed plans include key ID for provenance tracking. Receipt chains with optional RFC 3161 timestamps support independent verification of action history.

**AST03 — Over-Privileged Skills:** Runtime scope enforcement using pattern matching with wildcard hierarchies. Actions outside the approved scope are blocked before execution. Checkpoint mechanism requires human re-approval for sensitive actions.

**AST04 — Insecure Metadata:** Plan metadata (scope, delegates, checkpoints, expiry) is covered by Ed25519 signature. Modifying any field invalidates the plan.

**AST07 — Update Drift:** Plans have TTL-based expiry. Policy version is captured in every receipt via a policy hash (SHA-256 of canonical scope, checkpoints, and delegates).

**AST08 — Poor Scanning:** Shield module scans tool inputs for prompt injection (23 pattern categories), PII, secrets, encoding evasion, and structural injection. Pattern-based only; does not perform semantic analysis.

**AST09 — No Governance:** Per-agent session tracking with configurable escalation thresholds. Circuit breaker rate limiting prevents runaway execution. Signed audit trail links every action to a human-approved plan.

### Risks Not Addressed

**AST04 — Insecure Metadata (deserialization):** Does not parse skill manifests or configs from untrusted sources.  
**AST06 — Weak Isolation:** Runs in-process. Does not provide containerization or sandbox isolation.  
**AST10 — Cross-Platform Reuse:** Receipt format is tool-specific; does not yet implement the Universal Skill Format.

### Known Limitations

- Scanning is regex-based. Semantic and behavioral attacks are not detected.
- Runs in-process alongside the agent. A compromised process can bypass enforcement.
- No web dashboard or UI. Designed as a library, not a platform.

### Framework Integration

Integrates via hooks with CrewAI, OpenAI Agents SDK, Google ADK, and MCP. Typical integration requires approximately 20 lines of code per framework.

---

## EMILIA Protocol

**Description:** Reference implementation for receipt-gated admission of configured consequential actions. It verifies signed human authority for the exact canonical action under relying-party-pinned keys, atomically consumes that authority before entering a protected adapter, and records separately authenticated admission and outcome evidence.

**License:** Apache-2.0

**Repository:** [https://github.com/emiliaprotocol/emilia-protocol](https://github.com/emiliaprotocol/emilia-protocol)

**Install:** `npm install @emilia-protocol/gate @emilia-protocol/issue @emilia-protocol/verify`

**Dependencies:** The Gate package has 3 direct runtime dependencies: `@noble/curves` and 2 EMILIA packages. The issue and verify packages have no runtime dependencies.

### AST Risks Addressed

**AST03 — Over-Privileged Skills:** A Gate admission is bound to the complete canonical action, executor, audience, assurance tier, expiry, and configured relying-party policy. An action that differs from the approved bytes is refused. The same approval cannot authorize a second admitted occurrence after its authority is consumed.

**AST04 — Insecure Metadata:** Authority and evidence objects are signed over canonical encodings and verified under keys pinned by the relying party. Embedded presenter keys do not establish trust. The implementation distinguishes trusted executor observations from presenter-supplied claims.

**AST07 — Update Drift:** Admissions bind policy and key-state commitments at decision time. Expiry, issuer revocation, supersession, action drift, and stale status are checked before consumption. Protected adapters can re-read the trusted action before entry and refuse drift.

**AST09 — No Governance:** Every admission decision produces machine-readable evidence, and accepted authority is consumed before the protected effect boundary. Outcome handling distinguishes `EXECUTED`, `FAILED_BEFORE_EFFECT`, and `INDETERMINATE`; an unknown outcome is frozen for reconciliation instead of being retried as fresh work. Evidence packets can be verified offline under relying-party-pinned trust roots.

### Risks Not Addressed

**AST01 — Malicious Skills:** Does not classify skill intent or scan skill source. Pair with a pre-install scanner.

**AST02 — Supply Chain Compromise:** Does not establish the provenance or integrity of the skill package being invoked. Use signed artifacts, dependency controls, and a separate supply-chain verifier.

**AST05 — Untrusted External Instructions:** Exact-action admission can stop unapproved action substitution, but it does not make untrusted instructions safe or prove that an agent interpreted them correctly.

**AST06 — Weak Isolation:** Does not provide a process, container, network, or credential sandbox. The effect path must be exclusively mediated by a protected adapter for admission enforcement to apply.

**AST08 — Poor Scanning:** Not a malware, prompt-injection, or behavioral scanner.

**AST10 — Cross-Platform Reuse:** The authority and evidence objects are portable, but each runtime still needs an adapter that derives the trusted exact action and owns the consequence boundary.

### Known Limitations

- Integrators must pin acceptable issuers and providers independently of presented records, supply durable atomic consumption storage, and ensure the protected effect cannot bypass Gate.
- Signed evidence establishes who signed a bounded statement. It does not by itself establish source truth, external physical effect, population completeness, trusted time, audit sufficiency, or legal compliance.
- The repository is a reference implementation, not a hosted sandbox or general policy-control service. Concrete effect adapters remain deployment-specific.

### Framework Integration

Published packages cover OpenAI Agents, LangChain, MCP, and direct Gate adapters. The repository includes hostile conformance vectors for action substitution, replay, revocation, drift, concurrent admission, and unknown outcomes.

---

## Nobulex

**Description:** Cryptographic receipt layer for AI agent actions. Produces Ed25519-signed, JCS-canonical (RFC 8785) bilateral receipts — a pre-execution admission record and a post-execution outcome record — linked by a content-derived `action_ref = SHA-256(JCS({agent_id, action_type, scope, timestamp_ms}))`. Receipts are independently verifiable against the issuer's public key without operator cooperation.

**License:** MIT  
**Repository:** [https://github.com/arian-gogani/nobulex](https://github.com/arian-gogani/nobulex)  
**Install:** `pip install nobulex` (Python) or `npm install @nobulex/core` (TypeScript)  
**Dependencies:** Python — `cryptography`, `rfc8785`. TypeScript — `@noble/ed25519`, `canonicalize`.

### AST Risks Addressed

**AST03 — Over-Privileged Skills:** Each receipt binds the action to the `scope` field at decision time. A scope mismatch between the admission receipt (what was authorized) and the outcome receipt (what executed) produces non-matching `action_ref` hashes, detectable without trusting the runtime. The denied-before-dispatch path is first-class: a DENY decision produces an admission receipt; absence of an outcome receipt with that `attempt_id` proves the action was blocked rather than silently dropped.

**AST04 — Insecure Metadata:** The signed bilateral receipt covers `agent_id`, `action_type`, `scope`, `policy_version`, and `timestamp_ms` under one Ed25519 signature. Modifying any field invalidates the signature; the canonical preimage is recomputable from the receipt fields by any third party.

**AST07 — Update Drift:** `policy_version` is bound at decision time inside the admission receipt. A policy change between admission and execution is detectable because the receipt records the version that authorized the action, not the version in effect at audit time.

**AST09 — No Governance:** Hash-chained receipts produce a tamper-evident audit trail where each receipt references the prior receipt's digest. The chain is exportable as a structured package and verifiable offline against the agent's published Ed25519 public key — directly supporting the operator-independent verification property that EU AI Act Article 12 (enforcement August 2, 2026) requires.

### Risks Not Addressed

**AST01 — Malicious Skills:** Out of scope — does not scan, classify, or analyze skill code or intent. Pair with a scanner (e.g., SkillSpector) for pre-install detection.  
**AST02 — Supply Chain Compromise:** Out of scope — does not verify upstream provenance of the skill itself, only records the actions a skill takes once running.  
**AST05 — Untrusted External Instructions:** Out of scope — does not inspect or sandbox external content fetched at runtime.  
**AST06 — Weak Isolation:** Out of scope — provides no runtime sandboxing or process isolation. A compromised agent process can choose not to emit receipts; the audit trail then shows absence, not a forged execution.  
**AST08 — Poor Scanning:** Out of scope — not a scanner.  
**AST10 — Cross-Platform Reuse:** Partial — receipts are framework-agnostic at the field level (the receipt format is plain JSON + Ed25519), but the receipt records skill *calls*, not skill *definitions*, so it does not contribute to a Universal Skill Format.

### Known Limitations

- Receipts prove what the agent *self-reported* about its actions. A compromised agent can refuse to emit receipts; absence in the chain is detectable but does not by itself prove what the agent actually did externally. Pair with isolation (AST06) for runtime enforcement.
- Receipt verification is per-record. Set completeness (proving no receipts were dropped between two known ones) requires additional sequence-number and lifecycle fields not present in the current 4-field preimage. Verifiers checking contiguity need to pin the scope themselves.
- No on-chain anchoring in the core SDK. Long-horizon non-repudiation requires composition with a separate timestamping layer (RFC 3161 TSA, on-chain anchor, or transparency log).

### Framework Integration

Wraps any tool-call boundary: pre-execution admission emit + post-execution outcome emit. Integration examples shipped for LangChain, LangGraph, CrewAI, AutoGen, and direct MCP tool wrappers. Typical integration is one decorator or middleware function per agent. Benchmark: ~13,700 receipts/second on a 2024 M-series laptop, single-process (reproducible via `benchmarks/bench.ts` in the repo).

---

## SkilLock

**Description:** Behavior-layer lockfile and capability-delta PR review for AI agent skills. Statically parses each skill's `SKILL.md` fenced bash blocks and bundled scripts to record the *observed* capability surface (shell, network, file reads/writes, tool grants, scripts) into a committed `skills.lock` file, then blocks unapproved drift in CI and shows the capability delta in every pull request.

**License:** Apache-2.0 (the `SPEC.md` interop spec is CC BY 4.0)  
**Repository:** [https://github.com/skills-lock/skil-lock](https://github.com/skills-lock/skil-lock)  
**Install:** `go install github.com/skills-lock/skil-lock/cmd/skil-lock@latest` (also `brew install skills-lock/tap/skil-lock`, or download a SHA-256-checksummed release binary)  
**Dependencies:** Go 1.22+ at build time; ships as a single static binary with no runtime dependencies (cobra, goldmark, yaml.v3 build-time only)

### AST Risks Addressed

**AST03 — Over-Privileged Skills:** Records the observed capability surface (shell commands, network URLs, file reads/writes, tool grants) parsed from `SKILL.md` and bundled scripts, independent of what the frontmatter declares. Per SkilLock's own [scan of 17,065 public skills](https://github.com/skills-lock/skil-lock/blob/main/docs/ecosystem-scan-2026-06.md), 38.8% executed shell but only 4.0% declared it; the `SKL-SHELL` / `SKL-NETWORK` / `SKL-TOOLS` detectors surface that declared-versus-observed gap so reviewers can right-size permissions.

**AST04 — Insecure Metadata:** The core check is manifest-versus-behavior mismatch — capabilities a skill actually exercises but does not declare in its `allowed-tools` / frontmatter are flagged in the PR, making under-declared or misleading metadata visible at review time rather than at runtime.

**AST07 — Update Drift:** The committed `skills.lock` pins the approved behavior surface; on every change SkilLock computes a capability delta against that baseline and fails the CI gate when a skill's observed behavior drifts from what was last approved. A PR-scoped override file records explicit, auditable approvals. This is the tool's primary function.

**AST08 — Poor Scanning:** Six deterministic detectors (`SKL-SHELL`, `SKL-NETWORK`, `SKL-FILE-READ`, `SKL-FILE-WRITE`, `SKL-TOOLS`, `SKL-SCRIPTS`) parse fenced bash blocks and bundled scripts to extract the behavior surface. Detection is deterministic and parse-based — no semantic or LLM analysis — so results are reproducible in CI, with the coverage limits that implies (see Known Limitations).

**AST09 — No Governance:** `skills.lock` is a committed, human-readable inventory of every skill's approved capability surface. The GitHub Action posts a per-PR capability-delta comment and emits SARIF v2.1.0 to GitHub Code Scanning, providing an auditable approval trail and a queryable inventory kept in version control.

**AST10 — Cross-Platform Reuse:** Parses the shared `SKILL.md` content layer used by both Claude Code and Codex, evaluating skill behavior independently of the runtime. It validates the existing shared format across the two supported platforms rather than defining a new universal format (see Known Limitations).

### Risks Not Addressed

**AST01 — Malicious Skills:** Partial. Capability-delta detection flags a previously-approved skill that gains dangerous behavior (new shell / network / exfiltration surface) in an update, but SkilLock performs no first-party malware or intent classification (no signatures or heuristics) and cannot judge a never-seen skill as malicious on first sight.  
**AST02 — Supply Chain Compromise:** Partial. Per-file content digests of bundled scripts detect tampered or newly-added scripts on update; SkilLock does not verify registry provenance or upstream signatures of the skill source itself.  
**AST05 — Untrusted External Instructions:** Partial. The `SKL-NETWORK` detector inventories the external hosts and URLs a skill references — useful for spotting and tracking external sources — but SkilLock does not pin, hash-verify, or sandbox the content fetched from them. (The deserialization concern, now folded into AST04, is likewise out of scope: frontmatter is parsed with a safe YAML library, but SkilLock does not analyze or sandbox deserialization the skills themselves perform.)  
**AST06 — Weak Isolation:** Not addressed. SkilLock is a post-install, CI-time review tool and provides no runtime sandboxing or process isolation (a runtime guard is explicitly out of scope for v1).

### Known Limitations

- Behavior is extracted by static parsing of fenced bash and bundled scripts; dynamically constructed commands, heavy obfuscation, or capabilities exercised only at runtime can evade it. Use it as a review-layer gate, not a sandbox.
- Deterministic detectors only — no semantic or LLM intent analysis. Pair with a pre-install scanner (AST01 / AST08) and runtime isolation (AST06).
- It detects *change* against an approved baseline; the strength of the gate depends on that baseline being reviewed carefully when first locked.

### Framework Integration

CLI (`scan`, `lock`, `init --baseline`, `diff`, `verify`, `ci`) plus a GitHub Action that posts the capability delta as a PR comment and uploads SARIF v2.1.0 to GitHub Code Scanning. Supports Claude Code and Codex skills (same `SKILL.md` format). Runs on ubuntu and macos GitHub-hosted runners (amd64 + arm64).

---

## SkillSpector

**Description:** Open-source security scanner for AI agent skills (NVIDIA). Performs two-stage analysis — fast static checks plus optional LLM semantic evaluation — to answer "is this skill safe to install?" before installation. Produces a 0–100 risk score with severity labels and SARIF, JSON, or Markdown reports.

**License:** Apache-2.0  
**Repository:** [https://github.com/NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector)  
**Install:** `git clone https://github.com/NVIDIA/SkillSpector && make install` (or run via the included Dockerfile)  
**Dependencies:** Python 3.12+; optional LLM provider (Anthropic / OpenAI-compatible) for semantic analysis; OSV.dev for live CVE lookups

### AST Risks Addressed

**AST01 — Malicious Skills:** Detects malicious patterns and likely-malicious intent via YARA signatures, rogue-agent and trigger-abuse heuristics, and optional LLM intent analysis. Per NVIDIA's SkillSpector project, roughly 5.2% of scanned skills show likely malicious intent.

**AST02 — Supply Chain Compromise:** Supply-chain pattern category plus live OSV.dev CVE lookups against declared dependencies (with offline fallback).

**AST03 — Over-Privileged Skills:** Flags excessive agency, privilege escalation, tool misuse, and MCP least-privilege violations.

**AST04 — Insecure Metadata:** Scans `SKILL.md` prose and metadata for prompt injection and system-prompt leakage.

**AST08 — Poor Scanning:** Directly addresses the scanning gap — combines static analysis (AST-based dangerous-code detection, taint tracking, YARA) across both the code and natural-language layers with optional LLM semantic evaluation, covering 64 patterns across 16 categories.

**AST09 — No Governance:** Emits SARIF v2.1.0 for GitHub Code Scanning and CI gates; the 0–100 risk score supports approval workflows and scan-result inventories.

**AST10 — Cross-Platform Reuse:** Platform-agnostic content-layer scanner (Claude Code, Codex CLI, Gemini CLI) that evaluates skills independently of the runtime.

### Risks Not Addressed

**AST04 — Insecure Metadata (deserialization):** Partial only — dangerous-code and taint analysis can flag unsafe parsing, but it does not sandbox deserialization.  
**AST06 — Weak Isolation:** Out of scope — a pre-install static/LLM scanner does not provide runtime sandboxing or process isolation.  
**AST07 — Update Drift:** Partial — re-scanning on update and OSV freshness help, but it does not pin versions or enforce an update policy.

### Known Limitations

- Pre-install analysis: catches issues before installation, not runtime behavior. Pair with sandboxing (AST06) and governance (AST09).
- The LLM semantic stage requires an API key / model provider; static-only mode (`--no-llm`) runs without one but with reduced intent coverage.
- Static pattern coverage, like any scanner, can be evaded by sufficiently novel obfuscation — use as one layer of a pipeline, not the sole gate.

### Framework Integration

CLI and Docker; scans Git repos, URLs, zip files, directories, or single files. Emits SARIF v2.1.0 for GitHub Code Scanning and other SARIF consumers, plus JSON and Markdown. Integrates into CI/CD as a pre-merge or pre-publish gate keyed on the risk score.

---

## Template for New Entries

```markdown
## [Tool Name]

**Description:** [One to two sentences. What the tool does, factually.]

**License:** [SPDX identifier]  
**Repository:** [URL]  
**Install:** [Command]  
**Dependencies:** [Count and notable ones]

### AST Risks Addressed

**AST[XX] — [Risk Name]:** [How the tool addresses this risk. Factual, no superlatives.]

[Repeat for each applicable risk.]

### Risks Not Addressed

**AST[XX] — [Risk Name]:** [Brief reason.]

[Repeat for each non-applicable risk.]

### Known Limitations

- [Limitation 1]
- [Limitation 2]

### Framework Integration

[Which agent frameworks it works with and how.]

```

