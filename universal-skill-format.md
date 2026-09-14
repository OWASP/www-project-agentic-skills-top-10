---
layout: col-sidebar
title: Universal Skill Format v1.0
tags: agentic-security, universal-format, ast10
level: 2
type: specification
---

# Universal Skill Format v1.0

This specification defines a platform-agnostic manifest for agentic skills. Its goal is to preserve security properties when skills are reused across ecosystems and to mitigate AST10.

## Design Goals

- Normalize security metadata across platforms.
- Preserve permission intent during format translation.
- Provide machine-readable provenance and integrity signals.
- Enable policy-based governance without per-skill manual review.

## Canonical YAML Manifest

```yaml
---
# Universal Agentic Skill Format v1.0
# Compatible with: OpenClaw, Claude Code, Cursor/Codex, VS Code

name: example-skill
version: 1.0.0
platforms: [openclaw, claude, cursor, vscode]

description: "Safe example skill - concise, honest statement of function"
author:
  name: "Author Name"
  identity: "did:web:example.com"
  signing_key: "ed25519:pubkey_hex_here"

permissions:
  files:
    read:
      - ~/.config/app.json
    write:
      - ~/.config/app.json
    deny_write:
      - SOUL.md
      - MEMORY.md
      - AGENTS.md
  network:
    allow:
      - api.example.com
    deny: "*"
  shell: false
  tools:
    - web_fetch
    - read_file

requires:
  binaries: [jq, curl]
  min_runtime_version: "2026.1.0"

risk_tier: L1
scan_status:
  scanner: "snyk-agent-scan@1.4.0"
  last_scanned: "2026-02-15"
  result: "pass"

signature: "ed25519:ABCDEF1234567890..."
content_hash: "sha256:abcdef1234..."

changelog:
  - version: "1.0.0"
    date: "2026-02-01"
    notes: "Initial release"
---
```

## Field Rationale

- `permissions.deny_write`: protects identity-critical files unless explicitly overridden.
- `network.allow` + `network.deny`: supports egress allowlisting and default-deny behavior.
- `signature` and `content_hash`: allows integrity verification and transparency logging via Ed25519 over RFC 8785 JCS canonicalization.
- `author.identity` and `author.signing_key`: supports cryptographic identity resolution via `did:web`, `did:creduent`, and canonical `agent://` URIs bound via DNSSEC TXT records.
- `scan_status`: establishes provenance for scanner version, scan date, and verdict.
- `risk_tier`: enables automated governance policies and approvals.

## Validation Requirements

A compliant manifest SHOULD satisfy:

1. Required top-level fields: `name`, `version`, `description`, `permissions`, `risk_tier`, `content_hash`.
2. `permissions.network.deny` set to `"*"` unless explicit exception policy exists.
3. `signature` present for production distribution.
4. `scan_status.last_scanned` in ISO-8601 date format.

## OWASP AST Crosswalk

- AST01 / AST02: integrity and provenance controls (`signature`, `content_hash`).
- AST03 / AST04: least-privilege and explicit metadata normalization.
- AST08 / AST09: scanner provenance and governance-ready risk tiering.
- AST10: cross-platform semantic consistency.

## Related Documents

- [AST10 - Cross-Platform Reuse](ast10.md)
- [OWASP Agentic Skills Top 10](top10.md)
- [Controls and Checklist](checklist.md)

---

*Last updated: April 2026*
