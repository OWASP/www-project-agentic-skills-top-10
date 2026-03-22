---
layout: col-sidebar
title: AST04 — Insecure Metadata
tags: agentic-security, ast04, insecure-metadata
level: 2
type: documentation
---

**Severity**: High  
**Platforms Affected**: All

## Description

Skill metadata fields — name, description, author, permissions, `requires`, `risk_tier` — are attacker-controlled strings with no validation, signing, or trust anchoring. Malicious actors exploit this to impersonate trusted brands, understate permissions, misdeclare risk tiers, and poison registry search results.

## Why It's Unique to Skills

Skill metadata is the primary signal users rely on to make installation decisions. Unlike code, which can be statically analyzed, metadata manipulation targets human judgment — and increasingly, the automated trust decisions made by the installing agent itself.

## Real-World Evidence

- **ClawHub**: skills named "Google Calendar Integration," "Solana Wallet Tracker," "Polymarket Trader" — none affiliated with the named brands. No trademark validation at publish time.
- **Snyk (Feb 10, 2026)**: documented a malicious "Google" skill that passed casual inspection because the name, description, and README were professionally written.
- **ASCII smuggling**: Snyk's `toxicskills-goof` repository documents malicious skills that hide instructions via ASCII control characters and base64-encoded strings in `SKILL.md` files — invisible to human reviewers.

## Attack Scenarios

### Brand Impersonation

Publish `google-workspace-integration` before Google does; capture traffic from users searching for the official skill.

### Permission Understating

Declare `network: false` in metadata while the underlying script calls `curl` to an external endpoint.

### Risk Tier Spoofing

Self-classify as `risk_tier: L0` (safe) while embedding destructive operations.

### Steganographic Injection

Hide malicious instructions using zero-width Unicode, base64, or ASCII smuggling in Markdown — visible to the agent's prompt compiler, invisible to human reviewers.

## Preventive Mitigations

1. **Apply static analysis** to all metadata fields at publish time; flag suspicious patterns.
2. **Validate declared permissions** against runtime behavior in a sandboxed pre-publish test.
3. **Implement brand/trademark protection mechanisms** at registry level.
4. **Scan `SKILL.md` prose** for ASCII smuggling, base64 payloads, and zero-width characters.
5. **Cross-reference `risk_tier` declarations** against permission manifest scope.
6. **Surface metadata provenance** (who declared it, when, from which signing key) in registry UI.

## OWASP Mapping

- **LLM04** (Data/Model Poisoning)
- **CWE-345** (Insufficient Verification of Data Authenticity)
- **ASVS V14.5** (HTTP Security)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST04 Mapping |
|---------------|------------|----------------|
| **Layer 7** | Agent Ecosystem | Marketplace manipulation, identity spoofing |
| **Layer 3** | Agent Frameworks | metadata parsing and validation in skill frameworks |
| **Layer 6** | Security & Compliance | metadata integrity and provenance policy |

### MAESTRO Layer Details

- **Layer 7: Agent Ecosystem** - metadata-based trust decisions and registry abuse.
- **Layer 3: Agent Frameworks** - how frameworks integrate and verify skill metadata.
- **Layer 6: Security & Compliance** - enforcing schema and metadata authenticity policies.

## Cross-References

- **AST01 (Malicious Skills)**: Insecure metadata enables social engineering attacks to distribute malware.
- **AST02 (Supply Chain Compromise)**: Metadata spoofing can hide supply chain attacks.
- **AST03 (Over-Privileged Skills)**: Misleading permission declarations in metadata can grant excessive access.
- **AST08 (Poor Scanning)**: Metadata-based attacks may bypass static analysis scanners.
- **AST10 (Cross-Platform Reuse)**: Inconsistent metadata formats across platforms create confusion and exploitation opportunities.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Snyk: How a Malicious Google Skill on ClawHub Tricks Users](https://snyk.io/blog/)
- [Snyk: toxicskills-goof](https://github.com/snyk-labs/toxicskills-goof)

---

*Last updated: March 2026*