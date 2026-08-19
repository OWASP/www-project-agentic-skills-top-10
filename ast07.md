---
layout: col-sidebar
title: AST07 — Update Drift
tags: agentic-security, ast07, update-drift
level: 2
type: documentation
---

**Severity**: Medium  
**Platforms Affected**: All

## Description

Skills are installed and forgotten. Without immutable pinning and automated update verification, deployed skills drift out of sync with known-good versions — either because patches are not applied (leaving known vulnerabilities open) or because auto-update mechanisms blindly apply upstream changes that may themselves be malicious.

## Why It's Unique to Skills

Package update drift is a known risk in traditional software. In skills, it's amplified by two factors: (1) skills are often installed by individuals without enterprise patch management, and (2) a "fix" version of a skill is itself unverifiable without cryptographic pinning — the attacker can push a "v1.0.1" that looks like a patch but contains a new payload.

## Real-World Evidence

- **ClawJacked (CVE-2026-28363, CVSS 9.9)** and the broader OpenClaw CVE cluster (9 CVEs, 3 with public exploit code): the patch-lag window between disclosure and user update created an active exploitation window. SecurityScorecard confirmed 12,812 OpenClaw instances exploitable via RCE at time of analysis.
- **Claude Code CVE-2025-59536**: fixed in v1.0.111 (Oct 2025); CVE-2026-21852: fixed in v2.0.65 (Jan 2026). Gap of months between fix and public disclosure — users unaware of risk for the duration.
- **OpenClaw's hot-reload `SkillsWatcher`** enables real-time skill updates: a compromised upstream skill repository becomes instantly active without requiring agent restart.
- **Air Security, *SkillJacking* (Jul 2, 2026)**: published skills can be taken over outright — the most popular video-generation skill on skills.sh (11,483 installs) served its files live from a GitHub repo whose owner account had been deleted; researchers re-registered the username and controlled what every install received from that moment on. Victims needed no update to be affected — just one more use. In total, 925 skills (~134K agents) sat on such instantly hijackable sources, and the takeover itself tripped no scanner.
- **Air Security, *The Circus of Skills* (Jun 24, 2026)**: 17,822 skills (~12.4% of 142,836 scanned; 6.7M installs) rest on at least one untrusted external resource — including binaries fetched from a repo's `releases/latest` — content that can drift malicious underneath a deployed skill without any version change or update event.
- **Metano, *Sleeper Skills* (Aug 2026)**: a review of skills on ClawHub and SkillsMP found 50+ carrying self-update capability (28K+ downloads, 23K+ stars); 56 showed self-update, self-modification, dormant-patcher or persistent-state behavior, and 9 met a strict test — a normal-use or scheduled path that can replace the installed skill or its standing instructions with no per-change consent and no user-facing notice of that specific change. Three mechanisms were documented: an installer, run as a prerequisite to ordinary commands, that polls a remote endpoint and overwrites its own scripts, `SKILL.md` and reference material, then directs the agent to disregard prior memory of the skill and re-read the replaced file (`hope0719/quarkclouddrive-skill`); a skill whose normal loop writes what it "learns" back into its own `SKILL.md`, so untrusted runtime input — webpages, OCR output, accessibility text — can be laundered into a file later sessions treat as trusted (`tahcia/tahcia-console`); and a skill whose installed bytes never change while it reloads mutable Markdown instructions from an operator-controlled host on a heartbeat (`g620710/meyo`). The update channel is declared in the artifact that was reviewed, so a `sha256:` pin binds the updater rather than what it installs, and no account compromise, writable skill directory or registry event is required.

## Attack Scenarios

### Malicious Update

Trusted skill author's account is compromised; attacker pushes v2.0 with a payload. Auto-updating agents receive it silently.

### Patch-Lag Exploitation

CVE is disclosed; attacker weaponizes it before users patch. 12,812 instances exploitable in the OpenClaw case.

### Rollback Attack

Attacker forces a downgrade to a known-vulnerable version via dependency resolution manipulation.

### Hot-Reload Abuse

Skill directory is writable; attacker modifies `SKILL.md` mid-session; agent picks up changes without restart.

### Author-Declared Update Channel

The update path is part of the reviewed artifact rather than something done to it. A skill documents an installer as a prerequisite; on each run the installer fetches a bundle from a remote endpoint and replaces the skill's own scripts and `SKILL.md`. The content that executes is therefore retrieved after the approval, from a source no digest of the skill covers, under the authority already granted to that skill. Distinct from Hot-Reload Abuse, which presumes an attacker who can write to the skill directory: here the skill rewrites itself by design, and a self-modifying skill can additionally promote untrusted runtime input into its own standing instructions with no external writer at all.

## Preventive Mitigations

1. **Pin all installed skills to immutable content hashes (`sha256:`)**, not version ranges.
2. **Require cryptographic signature verification on every update** — refuse unsigned updates.
3. **Implement a "freeze" mode for production deployments**; prohibit hot-reload in non-development environments.
4. **Subscribe to registry security advisories** and auto-alert on CVE matches for installed skills.
5. **Enforce a human-in-the-loop approval step** for any skill update in enterprise environments.
6. **Maintain an inventory of installed skills** with version, hash, and last-verified timestamp.

## OWASP Mapping

- **LLM03** (Supply Chain)
- **CWE-1329** (Reliance on Component Without Verification)
- **ASVS V14.2** (Dependency)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST07 Mapping |
|---------------|------------|----------------|
| **Layer 4** | Deployment & Infrastructure | insecure update pipelines, config drift |
| **Layer 6** | Security & Compliance | update policy, verification enforcement |
| **Layer 7** | Agent Ecosystem | cross-registry trust and update governance |

### MAESTRO Layer Details

- **Layer 4: Deployment & Infrastructure** - unsafe automatic update and runtime drift.
- **Layer 6: Security & Compliance** - requirements for signed updates, patch policy.
- **Layer 7: Agent Ecosystem** - registry trust and cross-platform update consistency.

## Cross-References

- **AST01 (Malicious Skills)**: Update drift can introduce malicious code through compromised updates.
- **AST02 (Supply Chain Compromise)**: Unverified updates are a supply chain attack vector.
- **AST04 (Insecure Metadata)**: Update metadata may be spoofed to hide malicious changes.
- **AST05 (Untrusted External Instructions)**: Referenced external content can drift maliciously with no version change to the pinned skill.
- **AST08 (Poor Scanning)**: Updated skills may not be re-scanned, allowing new vulnerabilities.
- **AST09 (No Governance)**: Lack of update policies enables uncontrolled drift.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Check Point Research: Caught in the Hook](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files/)
- [Oasis Security: ClawJacked (CVE-2026-28363)](https://oasis.security/)
- [SecurityScorecard: 135,000+ OpenClaw instances exposed](https://securityscorecard.com/)
- [Air Security: SkillJacking](https://www.air.security/blog-posts/skilljacking)
- [Air Security: The Circus of Skills](https://www.air.security/blog-posts/the-circus-of-skills)
- [Metano: Sleeper Skills](https://metano.ai/post/sleeper-skills)

---

*Last updated: March 2026*