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
- **Logic-layer Prompt Control Injection (LPCI)** (Atta et al., *A Novel Security Vulnerability Class in Agentic Systems*, arXiv:2507.10457): peer-reviewed evidence that encoded, delayed, and conditionally-triggered payloads planted in memory, vector stores, or tool outputs are treated by the model as operator-level instructions, causing skills to autonomously invoke tools and write persistent state across sessions — exercising granted permissions the user never intended to trigger.

## Attack Scenarios

### Weather Assistant Data Exfiltration

A "weather assistant" skill reads `~/.clawdbot/.env` (all API keys) — far beyond weather API needs.

### Database Admin Wipe

A `manage_database` skill provisioned with admin credentials is tricked via prompt injection to wipe production data.

### Identity File Backdoors

A skill requesting write access to `SOUL.md` and `MEMORY.md` installs persistent behavioral backdoors.

### Logic-layer Injection of Privileged Actions (LPCI)

A skill receives external input — user data, retrieved memory, or another tool's output — that contains embedded instructions. Because the runtime evaluates permissions at the tool-call level rather than the intent level, the model treats this skill output as an operator-level command and autonomously performs a privileged action it is *technically* permitted to do (a tool call, a `MEMORY.md` write, code execution) without explicit user consent. The injected rule can persist across sessions and propagate to every downstream consumer of the skill.

## Preventive Mitigations

1. **Require skills to declare a permission manifest** (files, network, shell, tools) — reject skills without one.
2. **Enforce per-skill scoped credentials**, not shared agent-level API keys.
3. **Flag skills requesting write access** to agent identity files (`SOUL.md`, `MEMORY.md`, `AGENTS.md`) for elevated review.
4. **Implement runtime permission enforcement** — not just declarative.
5. **Adopt network allowlists** scoped to specific domains, not a binary `network: true/false`.
6. **Validate manifest declarations** against observed runtime behavior in sandboxed testing.
7. **Enforce a strict instruction hierarchy** (System > Operator > User > Skill/Tool Output). Never elevate skill or tool output to instruction level; treat all skill input and tool output as untrusted data, and tag external content with provenance markers so the model can distinguish data from commands.
8. **Require explicit operator consent for persistent state changes** — memory/identity-file writes, new tool approvals, and privilege escalations must not be auto-applied from injected instructions.

## OWASP Mapping

- **LLM09** (Misinformation / Excessive Agency)
- **LLM01** (Prompt Injection — logic-layer / instruction-hierarchy confusion)
- **ASVS V4** (Access Control)
- **CWE-250** (Execution with Unnecessary Privileges)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST03 Mapping |
|---------------|------------|----------------|
| **Layer 6** | Security & Compliance | Access controls, policy enforcement |
| **Layer 4** | Deployment & Infrastructure | Container/host hardening, sandboxing |
| **Layer 3** | Agent Frameworks | framework privilege handling, skill integration |
| **Layer 7** | Agent Ecosystem | registry policy enforcement and trust boundaries |

### MAESTRO Layer Details

- **Layer 6: Security & Compliance** - enforcement of least privilege and identity safety.
- **Layer 4: Deployment & Infrastructure** - runtime isolation and resource constraints.
- **Layer 3: Agent Frameworks** - permission orchestration in LangChain/AutoGen-like agents.
- **Layer 7: Agent Ecosystem** - enterprise capability to govern and score skill permissions.

## Cross-References

- **AST01 (Malicious Skills)**: Over-privileged skills amplify the impact of malicious payloads by providing broader access vectors.
- **AST02 (Supply Chain Compromise)**: Compromised registries may distribute skills with inflated permission requests.
- **AST04 (Insecure Metadata)**: Misleading permission declarations in manifests can hide over-privileged access.
- **AST06 (Weak Isolation)**: Host-mode execution removes permission boundaries entirely.
- **AST09 (No Governance)**: Lack of permission review processes allows over-privileged skills to proliferate.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Snyk: 280+ Leaky Skills](https://snyk.io/blog/280-leaky-skills-openclaw-clawhub-exposing-api-keys-pii/)
- [Cisco State of AI Security 2026](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)
- [Atta et al. — Logic-layer Prompt Control Injection (LPCI): A Novel Security Vulnerability Class in Agentic Systems (arXiv:2507.10457)](https://arxiv.org/abs/2507.10457)

---

*Last updated: March 2026*