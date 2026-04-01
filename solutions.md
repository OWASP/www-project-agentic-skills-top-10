# Open Source Tools Supporting AST10 Mitigations

This page catalogs open source tools that implement mitigations for one or more AST10 risks. Listings are factual and vendor-neutral. Inclusion does not imply OWASP endorsement.

## How to Add a Tool

Submit a PR adding your tool using the template at the bottom of this page. All fields are required. Entries that read as promotional will be asked to revise.

## Summary


| Tool                                                                               | License | AST Risks Addressed                             | Language |
| ---------------------------------------------------------------------------------- | ------- | ----------------------------------------------- | -------- |
| [AgentMint](https://claude.ai/chat/3c4cbcba-b466-4119-917a-6f6f661d50ac#agentmint) | MIT     | AST01, AST02, AST03, AST04, AST07, AST08, AST09 | Python   |


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

**AST05 — Unsafe Deserialization:** Does not parse skill manifests or configs from untrusted sources.  
**AST06 — Weak Isolation:** Runs in-process. Does not provide containerization or sandbox isolation.  
**AST10 — Cross-Platform Reuse:** Receipt format is tool-specific; does not yet implement the Universal Skill Format.

### Known Limitations

- Scanning is regex-based. Semantic and behavioral attacks are not detected.
- Runs in-process alongside the agent. A compromised process can bypass enforcement.
- No web dashboard or UI. Designed as a library, not a platform.

### Framework Integration

Integrates via hooks with CrewAI, OpenAI Agents SDK, Google ADK, and MCP. Typical integration requires approximately 20 lines of code per framework.

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

