---
layout: col-sidebar
title: AST02 — Supply Chain Compromise
tags: agentic-security, ast02, supply-chain
level: 2
type: documentation
---

# AST02 — Supply Chain Compromise

**Severity**: Critical  
**Platforms Affected**: All

## Description

Skill registries and distribution channels lack the provenance controls common in mature package ecosystems (npm, PyPI, Cargo). Attackers exploit this absence through coordinated mass uploads, dependency confusion, account takeover, and repository poisoning. Configuration files that were once passive metadata have become active execution paths — the CI/CD pipeline now includes skills as a first-class attack surface.

## Why It's Unique to Skills

The barrier to publishing on ClawHub was a `SKILL.md` file and a GitHub account one week old. No code signing, no security review, no sandbox by default. Agent skills also inherit execution context from the agent runtime, meaning a compromised skill gains the agent's full credential set — not just the permissions of a sandboxed package.

## Real-World Evidence

- **ClawHub**: no automated scanning at time of ClawHavoc; publishers could upload unlimited packages.
- **Claude Code CVE-2025-59536 / CVE-2026-21852**: repository configuration files (`.claude/settings.json`, hooks) become execution paths; simply cloning and opening a malicious repo triggers RCE and API key exfiltration before the user sees any dialog.
- **Dependency confusion**: a skill's `package.json` or `requirements.txt` pulls a typosquatted nested dependency containing the actual payload — the surface skill appears clean.
- **Snyk-documented attack**: skill named "Summarize YouTube Videos" imports `yutube-dl-core` instead of a legitimate package; nested dependency installs a backdoor.

## Attack Scenarios

### Registry Flooding

Coordinated upload of hundreds of malicious skills to crowd out legitimate alternatives.

### Dependency Confusion

Poison a nested dependency, not the top-level skill — bypasses surface-level scans.

### Config-File Hijacking

Embed execution instructions in repository config files (hooks, MCP settings, environment overrides) that trigger at project open.

### Maintainer Account Takeover

Compromise a trusted skill author's account, push a backdoored version.

## Preventive Mitigations

1. **Implement skill provenance tracking**: link each published skill to a verified code-signing identity.
2. **Require transparency logs** for all registry operations (publish, update, delete) — similar to Certificate Transparency.
3. **Pin all nested dependencies** to immutable hashes (`sha256:`), not version ranges.
4. **Treat repository configuration files** (hooks, `.claude/settings.json`, `ANTHROPIC_BASE_URL`) as executable code and apply trust gates accordingly.
5. **Scan recursive dependency trees**, not just top-level skill files.
6. **Support an internal skill mirror / allowlist** for enterprise deployments.

## OWASP Mapping

- **LLM03** (Supply Chain)
- **ASVS V14.2** (Dependency)
- **CWE-494** (Download of Code Without Integrity Check)

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Check Point Research: Caught in the Hook](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files/)
- [Antiy CERT: ClawHavoc Campaign Analysis](https://www.antiy.com/)

---

*Last updated: March 2026*