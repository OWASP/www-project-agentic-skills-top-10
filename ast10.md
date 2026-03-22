---
layout: col-sidebar
title: AST10 — Cross-Platform Reuse
tags: agentic-security, ast10, cross-platform-reuse
level: 2
type: documentation
---

**Severity**: Medium  
**Platforms Affected**: All

## Description

Skills are increasingly ported across platforms (OpenClaw → Claude Code → Cursor → VS Code) without translating the security properties of the source format. A skill with a permission manifest on one platform is stripped of that manifest on another. Security controls that exist in one ecosystem's metadata format simply do not exist in another's — creating exploitable gaps when skills cross platform boundaries.

## Why It's Unique to Skills

MCP standardizes the protocol. AST10 addresses the content security within skills — the fact that there is no universal skill format and no normalization of security metadata when skills are ported. This is not a protocol problem; it is a behavioral abstraction problem.

## Real-World Evidence

- **Snyk ToxicSkills** confirmed malicious skills published simultaneously on ClawHub and `skills.sh` by the same threat actors (zaycv, moonshine-100rze), exploiting the fact that neither platform shared scanning intelligence.
- **Snyk's `toxicskills-goof` proof-of-concept** demonstrates a fake Vercel skill that works across Gemini CLI and OpenClaw — the same malicious `SKILL.md` is effective on multiple runtimes.
- **The absence of a universal format** means organizations managing a multi-platform agent stack cannot apply a single governance policy — each platform requires separate tooling, separate scanning, and separate approval workflows.

## Attack Scenarios

### Security Property Loss in Translation

A skill with `risk_tier: L3` (destructive) is ported to a platform that doesn't support `risk_tier`; the warning is silently dropped.

### Cross-Registry Arbitrage

Attacker publishes a skill on a lightly-scanned registry (`skills.sh`) and promotes it to a more-trusted registry, leveraging the install count as a false trust signal.

### Multi-Platform Campaign

Same malicious payload deployed across four platforms simultaneously; security teams on each platform are unaware of the others' incidents.

## Preventive Mitigations

1. **Adopt the Universal Skill Format** (see below) for all new skill development.
2. **When porting skills across platforms**, require a full security metadata re-validation — never assume equivalence.
3. **Establish cross-registry threat intelligence sharing** between major skill registries.
4. **Build platform-agnostic skill scanners** that evaluate the content layer independently of the runtime.
5. **Normalize `risk_tier`, `permissions`, and `signature` fields** across all platform-specific formats.

## Universal Skill Format Proposal

The following YAML format is proposed as a cross-platform standard that mitigates AST10 and provides the metadata foundation required to address AST01 through AST09. It is designed to be a superset of all current platform-specific formats.

```yaml
---
# Universal Agentic Skill Format v1.0
# Compatible with: OpenClaw, Claude Code, Cursor/Codex, VS Code

name: example-skill
version: 1.0.0
platforms: [openclaw, claude, cursor, vscode]

description: "Safe example skill — concise, honest statement of function"
author:
  name: "Author Name"
  identity: "did:web:example.com"         # Decentralized identity anchor
  signing_key: "ed25519:pubkey_hex_here"

permissions:
  files:
    read:
      - ~/.config/app.json                 # Explicit paths only; no wildcards
    write:
      - ~/.config/app.json
    deny_write:
      - SOUL.md
      - MEMORY.md
      - AGENTS.md                          # Identity files require explicit grant
  network:
    allow:
      - api.example.com                    # Domain allowlist, not binary on/off
    deny: "*"                              # Default deny all other egress
  shell: false                             # Explicit shell access declaration
  tools:
    - web_fetch
    - read_file

requires:
  binaries: [jq, curl]
  min_runtime_version: "2026.1.0"

risk_tier: L1                              # L0=safe, L1=low, L2=elevated, L3=destructive
scan_status:
  scanner: "snyk-agent-scan@1.4.0"
  last_scanned: "2026-02-15"
  result: "pass"

signature: "ed25519:ABCDEF1234567890..."   # Signs the canonical hash of this manifest
content_hash: "sha256:abcdef1234..."       # Hash of the complete skill package

changelog:
  - version: "1.0.0"
    date: "2026-02-01"
    notes: "Initial release"
---
```

**Format design rationale:**
- `permissions.deny_write` protects identity files (`SOUL.md`, `MEMORY.md`) by default — must be explicitly overridden.
- `network.allow` is a domain allowlist, not a boolean — closing the "network: true" over-permission gap (AST03).
- `signature` and `content_hash` together enable Merkle-root registry verification (AST01/AST02).
- `scan_status` creates a machine-readable provenance trail (AST08/AST09).
- `risk_tier` enables automated governance policies without per-skill review (AST09/AST10).

## OWASP Mapping

- **LLM03** (Supply Chain)
- **CWE-1357** (Reliance on Insufficiently Trustworthy Component)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST10 Mapping |
|---------------|------------|----------------|
| **Layer 7** | Agent Ecosystem | cross-platform marketplace/registry intelligence |
| **Layer 3** | Agent Frameworks | translation and normalization controls across platforms |
| **Layer 6** | Security & Compliance | uniform policy enforcement and compliance across ecosystems |

### MAESTRO Layer Details

- **Layer 7: Agent Ecosystem** - cross-registry incident sharing, false trust signals.
- **Layer 3: Agent Frameworks** - framework-level normalization of security metadata.
- **Layer 6: Security & Compliance** - cross-platform governance for skill attributes.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Snyk: toxicskills-goof](https://github.com/snyk-labs/toxicskills-goof)
- [OWASP MCP Top 10](https://owasp.org/www-project-model-context-protocol-top-10/)

---

*Last updated: March 2026*