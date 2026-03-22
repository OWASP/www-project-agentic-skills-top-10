---
layout: col-sidebar
title: AST03 — Over-Privileged Skills
tags: agentic-security, ast03, over-privileged
level: 2
type: documentation
---

**Severity**: High  
**Platforms Affected**: All

## Description

Skills are granted broader permissions than their stated function requires — either because no permission manifest system exists, or because users accept all permissions without review. This creates excessive blast radius: a legitimate skill with overly permissive database access can be weaponized by a downstream prompt injection attack to execute `DROP TABLE` commands it was never meant to run.

## Why It's Unique to Skills

Traditional application least-privilege is well understood. But skills layer *natural language intent* on top of system permissions. A skill permitted to run `SELECT` queries may be coerced by prompt injection to run `DELETE` — because the permission check happens at the tool call level, not at the intent level.

## Real-World Evidence

- **Snyk ToxicSkills (Feb 2026)**: 280+ skills on ClawHub found exposing API keys and PII beyond their declared function.
- **OpenClaw default execution**: "tools run on the host for the main session, so the agent has full access." Skills can execute shell commands, read/write all files, access network services, and schedule cron jobs — without any per-skill permission scope.
- **Summer Yue (Meta AI)**: asked OpenClaw to review email inbox without taking actions; agent deleted large volumes of email before the process was killed — demonstrating that even well-intentioned agents execute with more authority than intended.

## Attack Scenarios

### Weather Assistant Data Exfiltration

A "weather assistant" skill reads `~/.clawdbot/.env` (all API keys) — far beyond weather API needs.

### Database Admin Wipe

A `manage_database` skill provisioned with admin credentials is tricked via prompt injection to wipe production data.

### Identity File Backdoors

A skill requesting write access to `SOUL.md` and `MEMORY.md` installs persistent behavioral backdoors.

## Preventive Mitigations

1. **Require skills to declare a permission manifest** (files, network, shell, tools) — reject skills without one.
2. **Enforce per-skill scoped credentials**, not shared agent-level API keys.
3. **Flag skills requesting write access** to agent identity files (`SOUL.md`, `MEMORY.md`, `AGENTS.md`) for elevated review.
4. **Implement runtime permission enforcement** — not just declarative.
5. **Adopt network allowlists** scoped to specific domains, not a binary `network: true/false`.
6. **Validate manifest declarations** against observed runtime behavior in sandboxed testing.

## OWASP Mapping

- **LLM09** (Misinformation / Excessive Agency)
- **ASVS V4** (Access Control)
- **CWE-250** (Execution with Unnecessary Privileges)

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Snyk: 280+ Leaky Skills](https://snyk.io/blog/280-leaky-skills-openclaw-clawhub-exposing-api-keys-pii/)
- [Cisco State of AI Security 2026](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)

---

*Last updated: March 2026*