# Skill Security Assessment Checklist

A practical checklist for evaluating AI agent skills against the [OWASP Agentic Skills Top 10](README.md). Use this during skill review, approval, and periodic reassessment.

> **How to use**: For each skill under review, work through the applicable sections below. A "No" answer indicates a gap that should be addressed before deployment. Items marked with severity reflect the risk rating of the parent AST category.

---

## AST01 — Malicious Skills `Critical`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 1.1 | Has the skill been obtained from a verified, trusted source? | Publisher identity confirmed; not a typosquat of a known skill name |
| 1.2 | Has the skill passed behavioral security analysis (not just pattern matching)? | Scan report from a tool that evaluates intent, not only code signatures |
| 1.3 | Has cryptographic signature verification been performed? | Valid ed25519 signature; `content_hash` matches published manifest |
| 1.4 | Have all skill scripts and natural language instructions been reviewed for malicious patterns? | No encoded payloads, no `curl` to unknown endpoints, no credential access beyond stated function in code or natural language instructions |
| 1.5 | Has the skill been tested in an isolated canary environment before production deployment? | Dynamic test report showing observed behavior matches declared behavior |
| 1.6 | Does the skill avoid writing to agent identity files (`SOUL.md`, `MEMORY.md`, `AGENTS.md`)? | No write access to identity files unless explicitly justified and approved *(see also 3.6 — privilege angle)* |

**Motivated by**: ClawHavoc campaign (1,184 malicious skills); 5 of top 7 most-downloaded ClawHub skills at peak infection were confirmed malware.

---

## AST02 — Supply Chain Compromise `Critical`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 2.1 | Has the skill publisher's identity been verified against a code-signing key? | Linked to a verified identity (e.g., `did:web:`, GitHub verified org) |
| 2.2 | Is the skill version pinned to a specific, immutable content hash (`sha256:`)? | No version ranges; hash matches registry record |
| 2.3 | Are all nested dependencies also pinned to immutable hashes? | `requirements.txt`, `package.json` dependencies locked — no `^` or `~` ranges |
| 2.4 | Has a Software Bill of Materials (SBOM) been generated for the skill and its dependencies? | SBOM available in a standard format (CycloneDX, SPDX) |
| 2.5 | Are repository configuration files (hooks, `.claude/settings.json`, env overrides) treated as executable code with trust gates? | Config files reviewed and approved; not auto-executed on clone/open |
| 2.6 | Has the recursive dependency tree been scanned (not just top-level skill files)? | Deep scan report covering transitive dependencies |

**Motivated by**: Claude Code CVE-2025-59536 (CVSS 8.7) — repo config files trigger RCE at project open before user dialog. ClawHub had no automated scanning at time of ClawHavoc.

---

## AST03 — Over-Privileged Skills `High`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 3.1 | Does the skill declare a permission manifest with explicit, scoped permissions? | Manifest present; permissions enumerated (not open-ended) |
| 3.2 | Are permissions minimized to the skill's stated functionality? | No access beyond what the described function requires |
| 3.3 | Does the skill avoid unrestricted shell access (`shell: true`)? | `shell: false` or shell access scoped to specific commands |
| 3.4 | Are file permissions scoped to specific paths (no `**/*` wildcards)? | Explicit file paths declared; no broad globs |
| 3.5 | Does the skill use per-skill scoped credentials (not shared agent-level API keys)? | Credentials isolated to this skill's scope; rotated on schedule |
| 3.6 | Is write access to agent identity files (`SOUL.md`, `MEMORY.md`) flagged for elevated review? | Write access to identity files requires explicit justification and approval *(see also 1.6 — persistence angle)* |
| 3.7 | Are network permissions declared as domain allowlists (not binary `network: true/false`)? | Specific domains listed; default deny for all other egress |
| 3.8 | Does the skill avoid accessing credential stores, `.env` files, wallet files, or SSH keys beyond its stated function? | No reads to `~/.ssh/`, `~/.aws/`, `.env`, `**/credentials*`, `*.wallet`, or browser data directories unless explicitly required and justified |

**Motivated by**: 280+ ClawHub skills exposing API keys and PII beyond declared function (Snyk, Feb 2026). ClawHavoc campaign specifically targeted `.env` files, exchange API keys, wallet private keys, SSH credentials, and browser passwords. OpenClaw default grants full shell, file, network, and cron access.

---

## AST04 — Insecure Metadata `High`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 4.1 | Does the skill description accurately and completely reflect its actual functionality? | No hidden capabilities; description matches observed behavior |
| 4.2 | Has metadata been scanned for ASCII smuggling, zero-width Unicode, and base64-encoded payloads? | Clean scan; no steganographic content in `SKILL.md` natural language instructions or manifest |
| 4.3 | Are default metadata configurations secure (not permissive)? | No default-open permissions; dangerous capabilities (shell, network, identity file writes) require explicit opt-in in the manifest |
| 4.4 | Has metadata been validated against a security schema? | Schema validation passed; no unexpected or undeclared fields |
| 4.5 | Is the declared `risk_tier` consistent with the actual permission scope? | Cross-reference: a skill declaring `L0` (safe) with `shell: true` is a red flag |
| 4.6 | Has brand/trademark impersonation been checked? | Skill name does not impersonate a known brand without affiliation |

**Motivated by**: Malicious "Google," "Solana Wallet Tracker," and "Polymarket Trader" skills on ClawHub — none affiliated with named brands. ASCII smuggling confirmed in Snyk's toxicskills-goof samples.

---

## AST05 — Unsafe Deserialization `High`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 5.1 | Are all YAML files parsed with safe loaders (`yaml.safe_load`, not `yaml.load`)? | No unsafe YAML tags (`!!python/object`, `!!python/apply`) in skill files |
| 5.2 | Are skill config files parsed and validated in an isolated subprocess or container before execution? | Deserialization happens in sandboxed context with no access to host resources |
| 5.3 | Is an allowlist of permitted YAML/JSON keys enforced? | Unexpected or undeclared fields are rejected |
| 5.4 | Are `requirements.txt`, `package.json`, and `pyproject.toml` within skill packages treated as untrusted code? | Dependency installation sandboxed; not executed with agent privileges |
| 5.5 | Has schema validation (JSON Schema, Pydantic, or equivalent) been applied before any deserialization of skill-provided data? | Validation step confirmed in skill loader pipeline |
| 5.6 | Is deserialization performed with minimum privileges (not elevated agent context)? | Privilege drop confirmed before parsing |

**Motivated by**: PyYAML `!!python/object` allows arbitrary code execution on load. ClawHavoc staged downloads: safe SKILL.md triggered secondary payload during dependency install phase.

---

## AST06 — Weak Isolation `High`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 6.1 | Will the skill run in an isolated container or sandbox (not host-mode)? | Docker/container isolation confirmed; host-mode requires explicit opt-in |
| 6.2 | Is filesystem access limited to declared paths only? | No access outside declared scope; verified in dynamic testing |
| 6.3 | Is network access controlled — localhost bound with authentication, not `0.0.0.0`? | Agent control interfaces require auth; not exposed to network |
| 6.4 | Are seccomp/AppArmor profiles applied to constrain system calls? | Profile attached to skill execution context |
| 6.5 | Is the skill isolated from other skills and agents (per-skill namespacing)? | Process-level isolation confirmed; no shared memory or filesystem between skills |
| 6.6 | Are WebSocket connections rate-limited and authenticated (including from localhost)? | Rate limiting and auth confirmed on all control channels |
| 6.7 | Is skill hot-reload / workspace precedence restricted in production? | Workspace skill overrides require explicit user confirmation *(see also 7.5 — update drift angle)* |

**Motivated by**: 135,000+ OpenClaw instances publicly exposed with no default firewall or authentication (SecurityScorecard). ClawJacked (CVE-2026-28363, CVSS 9.9): browser tab brute-forces localhost WebSocket to hijack local agent.

---

## AST07 — Update Drift `Medium`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 7.1 | Is the skill pinned to a specific immutable content hash (`sha256:`)? | Hash recorded in inventory; not a mutable version tag |
| 7.2 | Is auto-update disabled or gated behind re-approval in production? | Updates require explicit human approval before deployment |
| 7.3 | Are updates cryptographically signed by the original publisher? | Signature verification on every update; reject unsigned |
| 7.4 | Will updates trigger automatic security re-scanning? | Scan pipeline runs on every version change |
| 7.5 | Is hot-reload disabled in non-development environments? | `SkillsWatcher` or equivalent disabled in production; changes require restart + approval *(see also 6.7 — isolation angle)* |
| 7.6 | Is there an active subscription to security advisories for installed skills? | CVE alerts configured for all installed skill packages |

**Motivated by**: 12,812 OpenClaw instances exploitable via RCE during patch-lag window (SecurityScorecard). OpenClaw SkillsWatcher enables real-time hot-reload — compromised upstream becomes instantly active.

---

## AST08 — Poor Scanning `Medium`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 8.1 | Has behavioral / semantic analysis been performed (not just pattern matching)? | Scan tool evaluates intent and natural language instructions, not only regex signatures |
| 8.2 | Have both the code layer AND the natural language instruction layer been scanned independently? | Separate scan results for code artifacts and `SKILL.md` / manifest natural language instructions |
| 8.3 | Has credential detection scanning been run (Gitleaks, TruffleHog, or equivalent)? | Clean scan for API keys, tokens, passwords, and PII in all skill files |
| 8.4 | Was scanning performed in an isolated environment that prevents skill interference? | Scan environment instrumented; skill cannot detect or influence scanning context |
| 8.5 | Has dynamic behavioral testing been performed in a sandboxed runtime? | Observed behavior log: file access, network calls, shell commands match declared scope |
| 8.6 | Are scan results from skill-based scanners treated as advisory only (not sole gate)? | No reliance on a single scanner — especially not a scanner that is itself a skill |

**Motivated by**: 13.4% of critical-severity skills not caught by pattern matching (Snyk). ClawHub's "Skill Defender" scanner — itself a skill — was used by attackers as a false-trust signal. Alice Caterpillar flagged several published skills as actively malicious that were in use by over 6,000 OpenClaw users at time of detection ([Yahoo Finance](https://finance.yahoo.com/news/alice-releases-caterpillar-catching-malicious-191600442.html)).

---

## AST09 — No Governance `Medium`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 9.1 | Is the skill recorded in the organization's centralized skill inventory? | Entry exists with: name, version, hash, install date, installer identity, last scan status |
| 9.2 | Has the skill been assigned a risk tier classification (L0–L3)? | Risk tier documented and consistent with permission scope |
| 9.3 | Is there an approval record for this skill's installation? | Approval workflow completed; approver identity and date recorded |
| 9.4 | Are skill invocations logged with sufficient detail for audit? | Logs capture: skill ID, user context, tools called, files accessed, network connections, outputs |
| 9.5 | Is there a defined review cadence for this skill? | Periodic reassessment scheduled; frequency matches risk tier |
| 9.6 | Is there a formal revocation/deprovisioning process tied to offboarding and incident response? | Skill removal linked to identity lifecycle; IR playbook includes skill-specific scenarios |
| 9.7 | Are agent identities managed as non-human identities (NHIs) with scoped, rotated credentials? | Agent NHI registered in IAM; credentials scoped and rotated on schedule |

**Motivated by**: 53,000+ exposed instances with no SOC visibility (Bitdefender). Only 34% of enterprises have AI-specific security controls (Cisco State of AI Security 2026). NIST/CAISI Federal Register RFI acknowledges AI agent governance as unsolved.

---

## AST10 — Cross-Platform Reuse `Medium`

| # | Check | Evidence to look for |
|---|-------|---------------------|
| 10.1 | Has the skill been independently validated for each target platform? | Per-platform test results; not assumed equivalent |
| 10.2 | Are security properties (permissions, risk_tier, signature) consistently declared across all platform versions? | No silent property loss during porting; `risk_tier` and `permissions` present in every format |
| 10.3 | Have platform-specific security gaps been assessed for each deployment target? | Gap analysis comparing sandbox model, permission enforcement, and default config per platform |
| 10.4 | Is credential handling consistent and secure across all platforms? | Credential storage, scoping, and rotation verified per platform |
| 10.5 | Is there cross-registry threat intelligence sharing for this skill? | If published on multiple registries, scan results and incident reports shared between them |
| 10.6 | Does the skill use the Universal Skill Format (or a platform-agnostic manifest)? | Normalized YAML manifest present with all security metadata fields |

**Motivated by**: Same malicious skills published on ClawHub AND skills.sh by same threat actors (Snyk). toxicskills-goof fake Vercel skill effective across Gemini CLI and OpenClaw simultaneously.

---

## Quick Reference: Severity by Risk

| Severity | Risks | Minimum review depth |
|----------|-------|---------------------|
| **Critical** | AST01, AST02 | Full checklist + dynamic testing + manual review |
| **High** | AST03, AST04, AST05, AST06 | Full checklist + automated scanning |
| **Medium** | AST07, AST08, AST09, AST10 | Checklist review + inventory verification |

---

## Recommended Scanning Tools

The following open-source tools can be used to automate checklist verification:

| Tool | Purpose | Relevant AST Risks |
|------|---------|-------------------|
| [Semgrep](https://github.com/semgrep/semgrep) | Code pattern analysis, custom rules | AST01, AST04, AST05 |
| [Bandit](https://github.com/PyCQA/bandit) | Python-specific security analysis | AST01, AST05 |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Credential and secret detection | AST03, AST08 |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | Secret scanning across repos and history | AST03, AST08 |
| [Caterpillar](https://github.com/alice-dot-io/caterpillar) | Dynamic SAST for AI agents — continuous behavioral analysis | AST01, AST03, AST08 |
| [Snyk](https://snyk.io/) | Dependency and supply chain scanning | AST02, AST07 |

> No single tool covers all risks. A multi-tool pipeline combining static analysis, credential detection, and behavioral/dynamic analysis is recommended (see AST08).

---

## How to Contribute

This checklist is a living document. To suggest additional checks, platform-specific guidance, or corrections:
- Open a [GitHub Issue](https://github.com/kenhuangus/agentic-skills-top-10/issues) with the label `checklist`
- Submit a PR against this file

---

*Part of the [OWASP Agentic Skills Top 10](README.md) project. Licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).*
