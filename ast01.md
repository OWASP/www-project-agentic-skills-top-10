---
layout: col-sidebar
title: AST01 — Malicious Skills
tags: agentic-security, ast01, malicious-skills
level: 2
type: documentation
---

**Severity**: Critical  
**Platforms Affected**: All

## Description

Attackers publish skills that appear legitimate but contain hidden malicious payloads — credential stealers, reverse shells, backdoors, or social engineering instructions embedded in `SKILL.md` prose sections. Because agent skills execute with the full permissions of the host agent, a malicious skill gains immediate access to API keys, SSH credentials, wallet files, browser data, and shell.

## Why It's Unique to Skills

Unlike traditional malicious packages, malicious skills exploit both the *code layer* (shell scripts, Python calls) and the *natural language instruction layer* (markdown prose instructing the agent to perform actions). The Snyk ToxicSkills research confirmed that 100% of malicious skills combined both attack vectors.

## Real-World Evidence

- **ClawHavoc campaign (Jan 2026)**: 1,184 malicious skills across 12 publisher accounts, all sharing C2 IP `91.92.242[.]30`. Delivered Atomic Stealer (AMOS) targeting macOS crypto wallets, SSH keys, and browser credentials.
- Five of the top seven most-downloaded ClawHub skills at peak infection were confirmed malware.
- Three lines of markdown in a `SKILL.md` file were sufficient to exfiltrate SSH keys (Snyk, Feb 2026).
- Skills impersonating "Google," "Solana wallet tracker," "YouTube Summarize Pro," and "Polymarket Trader" — all designed to match high-demand searches.

## Attack Scenarios

### Typosquatting

- `google-workspace` vs. `gogle-workspace`
- `youtube-dl-core` vs. legitimate package

### Social Engineering Prerequisites

`SKILL.md` "Prerequisites" section instructs users to copy-paste terminal commands to install "helper tools" from attacker-controlled domains.

### ClickFix Prompts

Fake "setup required" dialogs that coerce users into running malicious scripts.

### SOUL.md Persistence

Malicious skills write backdoor instructions into the agent's identity file, surviving skill uninstall.

## Preventive Mitigations

1. **Require cryptographic signatures (ed25519)** on all published skills; reject unsigned installs.
2. **Implement Merkle root signing** for skill registries.
3. **Scan skills at publish time and at install time** using behavioral analysis (not just pattern matching).
4. **Display skill publisher trust level, install count, and scan status** in registry UI.
5. **Never auto-execute "Prerequisites" sections** without explicit user review.
6. **Hash-pin installed skills** and alert on any modification.

## OWASP Mapping

- **LLM03** (Supply Chain)
- **LLM01** (Prompt Injection - indirect)
- **ASVS V14** (Configuration)

## MAESTRO Framework Mapping

The Cloud Security Alliance (CSA) MAESTRO framework provides a structured threat modeling approach for agentic AI systems across 7 layers:

| MAESTRO Layer | Layer Name | AST01 Mapping |
|---------------|------------|---------------|
| **Layer 7** | Agent Ecosystem | Registry compromise, marketplace manipulation, agent impersonation |
| **Layer 3** | Agent Frameworks | Compromised components, supply chain attacks |
| **Layer 6** | Security & Compliance | Access controls, policy enforcement |
| **Layer 4** | Deployment & Infrastructure | Container tampering, runtime environment security |
| **Layer 5** | Evaluation & Observability | Detection evasion, metric manipulation |

### MAESTRO Layer Details

**Layer 7: Agent Ecosystem** - Primary mapping for AST01
- Malicious skills published to registries (ClawHub, skills.sh)
- Marketplace manipulation through typosquatting and brand impersonation
- Agent impersonation attacks via fake "Google," "Solana wallet tracker" skills
- Registry compromise enabling coordinated malicious skill campaigns

**Layer 3: Agent Frameworks**
- Compromised skill components within agent frameworks (OpenClaw, Claude Code, Cursor)
- Supply chain attacks through skill dependencies
- Prompt injection within skill instructions

**Layer 6: Security & Compliance**
- Access control failures allowing malicious skills to execute with full permissions
- Policy enforcement gaps in skill registries

**Layer 4: Deployment & Infrastructure**
- Runtime environment security for skill execution
- Container tampering through malicious skill payloads

**Layer 5: Evaluation & Observability**
- Detection evasion through obfuscated malicious instructions
- Metric manipulation to bypass security scanning

## Related Risks

- [AST02 — Supply Chain Compromise](ast02.md): Often the delivery mechanism for malicious skills.
- [AST03 — Over-Privileged Skills](ast03.md): Malicious skills exploit excessive permissions.
- [AST04 — Insecure Metadata](ast04.md): Brand impersonation enables malicious skill distribution.
- [AST08 — Poor Scanning](ast08.md): Ineffective detection allows malicious skills to proliferate.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Check Point Research: Caught in the Hook](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files/)
- [Antiy CERT: ClawHavoc Campaign Analysis](https://www.antiy.com/)

---

*Last updated: March 2026*