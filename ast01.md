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

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Check Point Research: Caught in the Hook](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files/)
- [Antiy CERT: ClawHavoc Campaign Analysis](https://www.antiy.com/)

---

*Last updated: March 2026*