---
layout: col-sidebar
title: AST06 — Weak Isolation
tags: agentic-security, ast06, weak-isolation
level: 2
type: documentation
---

# AST06 — Weak Isolation

**Severity**: High  
**Platforms Affected**: All

## Description

Skills execute in the same security context as the host agent — with full file system access, shell access, and network egress — because sandboxing is either unavailable, optional, or disabled by default. This removes all containment guarantees and turns every installed skill into a potential full-system compromise.

## Why It's Unique to Skills

Traditional software sandboxing is an engineering default with well-understood tooling (containers, VMs, seccomp). The agent skill ecosystem has grown so rapidly that sandboxing is an afterthought — and the agents themselves are designed to have broad permissions, making scope reduction architecturally non-trivial.

## Real-World Evidence

- **OpenClaw documentation (2026)**: "tools run on the host for the main session, so the agent has full access when it's just you." Docker sandboxing is available but requires explicit configuration that most users never apply.
- **SecurityScorecard (Feb 2026)**: 135,000+ OpenClaw instances publicly internet-exposed on TCP port 18789; no default firewall, authentication, or process isolation.
- **Microsoft Defender advisory (Feb 2026)**: explicitly warned that OpenClaw "should be treated as untrusted code execution with persistent credentials" and "is not appropriate to run on a standard personal or enterprise workstation."
- **ClawJacked (CVE-2026-28363, CVSS 9.9)**: Web-based attack against locally-bound agent instance — cross-origin WebSocket brute force bypassed all isolation assumptions of a localhost-only deployment.

## Attack Scenarios

### Host Escape

Malicious skill executes `os.system()` to plant a cron job on the host, persisting beyond skill uninstall.

### Network Pivot

Agent with no network sandbox egresses to an attacker C2, exfiltrates credentials from other co-located services.

### Skill Shadowing

OpenClaw's three-tier precedence system (workspace > managed > bundled) allows an attacker who plants a skill in a workspace folder to shadow legitimate built-in functionality — active immediately via hot-reload.

### Localhost Attack Surface

Locally-bound agent WebSocket is reachable from any browser tab; malicious site brute-forces the session token.

## Preventive Mitigations

1. **Require Docker/container isolation for skill execution by default**; host-mode should require explicit opt-in with documented risk.
2. **Bind agent control interfaces to localhost with authentication**; never `0.0.0.0` by default.
3. **Apply seccomp/AppArmor profiles** to constrain agent syscall surface.
4. **Implement per-skill process isolation** — each skill runs in its own namespace.
5. **Restrict skill hot-reload / workspace precedence**; require explicit user confirmation for workspace skill overrides.
6. **Rate-limit and authenticate all WebSocket connections**, including from localhost.

## OWASP Mapping

- **LLM08** (Excessive Agency)
- **CWE-653** (Insufficient Compartmentalization)
- **ASVS V12** (File/Resource)

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [SecurityScorecard: 135,000+ OpenClaw instances exposed](https://securityscorecard.com/)
- [Microsoft Defender: OpenClaw Enterprise Security Advisory](https://www.microsoft.com/security/)
- [Oasis Security: ClawJacked (CVE-2026-28363)](https://oasis.security/)

---

*Last updated: March 2026*