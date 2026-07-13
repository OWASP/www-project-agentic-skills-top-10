---
layout: col-sidebar
title: AST05 — Untrusted External Instructions
tags: agentic-security, ast05, external-instructions
level: 2
type: documentation
---

**Severity**: High  
**Platforms Affected**: All

## Description

Skills routinely reference external documentation — API references, SDK guides, schemas, runbooks — pointing the agent at a URL or remote file to read at runtime. In practice that content *becomes part of the skill's instructions*: the agent loads it, trusts it as it trusts the skill, and acts on it with the host agent's full permissions. Yet unlike the skill package — which can be reviewed, signed, and version- or hash-pinned — this referenced content is mutable, lives outside the trust boundary, and has no equivalent control; it can change at any moment. It can be poisoned by an attacker who owns the external source, or rewritten by the skill's own author after the skill has passed review — so the skill that was audited is never the skill that actually runs.

## Why It's Unique to Skills

External code dependencies are a known, well-mitigated problem in traditional software — version and hash pinning, lockfiles, signed packages. Textual external dependencies are unique to skills, and inherit none of that framework: there is no field to pin a document's hash, no lockfile for prose, and signing the skill says nothing about what a URL returns at runtime. And unlike a library's documentation — which humans read as reference — a skill's referenced text is consumed as *instructions, not data*: followed as faithfully as the `SKILL.md` itself, and executed with the agent's full permissions.

## Real-World Evidence

- **Vendor acknowledgment (Anthropic, Agent Skills documentation)**: Anthropic's own security guidance warns that "Skills that fetch data from external URLs pose particular risk, as fetched content may contain malicious instructions," and that "even trustworthy Skills can be compromised if their external dependencies change over time" — the platform vendor documenting both the injection and the rug-pull variants of this exact risk.
- **POC for agent takeover using external instructions (Air Security, The Story of Skills (June 22, 2026))**: Air's research shows how a skill pointing to malicious external instructions can lead to full agent compromise.
- **Ecosystem-wide measurement of untrusted instruction sources (Air Security, The Circus of Skills (June 24, 2026))**: a scan of 142,836 live skills found 17,822 (~12.4%, 6.7M installs) reference at least one external instruction source — unvetted domains, zero-reputation GitHub repos, packages, free-tier hosts — that a reviewer has no good reason to trust won't turn malicious.

## Attack Scenarios

### Author Rug-Pull

The author ships a benign skill that points the agent at documentation they control. It passes review and scanning — then, once trusted and deployed, the author edits the referenced document to inject new instructions (exfiltrate a file, auto-approve a command), which every agent running the skill now obeys.

### Reviewer Bait-and-Switch

The referenced URL serves clean documentation to reviewers, scanners, and crawlers (keyed on IP, user-agent, or timing) but malicious instructions to live agent runs — so inspecting the link passes while the agent is hijacked.

### Transitive Reference Chaining

The referenced document tells the agent to read still more external resources. Because the agent follows references transitively, the attacker need only control a link buried deep in the chain, well past where review stopped.

## Preventive Mitigations

1. **Pin and verify referenced content**: record a content hash for every external document a skill references at review time, and re-verify it on every load — refusing content that is unpinned or has drifted from the reviewed version.
2. **Prefer inlining over fetching**: snapshot external documentation into the signed skill package at publish time, so referenced content is reviewable and pinnable. When the content must stay current, deliver updates through a controlled, auto-updating marketplace channel — with its own review and provenance — rather than pointing the skill at an uncontrollable URL.
3. **Allowlist permitted reference domains**: using the OWASP Universal Agentic Skill Format, restrict the external hosts a skill may fetch from to a vetted allowlist of trusted, stable domains and URL globs unlikely to lapse or turn malicious.
4. **Audit references transitively**: follow every reference — including remote ones and the chains they point to — as part of the skill's attack surface, and make sure they too are vetted, trusted, and reputable.
5. **Maintain fleet-wide visibility of referenced sources**: keep an inventory of which deployed skills fetch from which external sources, so a source that is later compromised, changed, or abandoned can be traced to every affected skill and revoked.
6. **Rescan continuously**: when a skill fetches an external instruction source, treat each scan not as a one-time event but as a snapshot of a mutable state - and rescan often.

## OWASP Mapping

- **LLM01** (Prompt Injection — indirect)
- **LLM03** (Supply Chain)
- **CWE-829** (Inclusion of Functionality from Untrusted Control Sphere)
- **ASVS V5** (Validation, Sanitization and Encoding)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST05 Mapping |
|---------------|------------|----------------|
| **Layer 3** | Agent Frameworks | skill loaders resolve references and follow them as instructions |
| **Layer 2** | Data Operations | untrusted external content ingested into the agent's context |
| **Layer 7** | Agent Ecosystem | trust in external documentation sources, hosts, and marketplaces |
| **Layer 6** | Security & Compliance | missing integrity verification and provenance for referenced content |

### MAESTRO Layer Details

- **Layer 3: Agent Frameworks** - primary: the skill loader resolves references — including remote and transitive ones — and injects their content into the model as instructions, without treating it as untrusted.
- **Layer 2: Data Operations** - externally referenced documentation enters the agent's context as untrusted data and is acted on as instruction (indirect prompt injection).
- **Layer 7: Agent Ecosystem** - referenced external sources are ecosystem dependencies whose owners can change, lapse, or be compromised (rug-pull, host takeover, dangling reclaim).
- **Layer 6: Security & Compliance** - no requirement to pin, verify, or attest the integrity of referenced content across its lifecycle.

## Cross-References

- **AST01 (Malicious Skills)**: a malicious author can place the payload in referenced content rather than the skill body, so the skill itself stays clean and passes inspection.
- **AST02 (Supply Chain Compromise)**: AST02 covers the code and dependency supply chain, which integrity controls can pin and verify; AST05 covers the documentation a skill points to, which those controls do not reach.
- **AST04 (Insecure Metadata)**: AST04 executes a payload through unsafe parsing of the skill's own files at load time; AST05 requires no code execution — the agent simply follows instructions in externally referenced text.
- **AST07 (Update Drift)**: AST07 addresses the skill version changing; AST05 is the same drift applied to referenced content, which can change while the skill stays pinned and unchanged.
- **AST08 (Poor Scanning)**: externally referenced content can be absent at scan time or served selectively, widening AST08's detection gap to content a scanner may never see.

## References

- [Anthropic: Agent Skills — Security considerations](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Air Security: The Story of Skills](https://www.air.security/blog-posts/the-story-of-skills)
- [Air Security: The Circus of Skills](https://www.air.security/blog-posts/the-circus-of-skills)

---

*Last updated: June 2026*
