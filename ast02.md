---
layout: col-sidebar
title: AST02 — Supply Chain Compromise
tags: agentic-security, ast02, supply-chain
level: 2
type: documentation
---

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

### Code Example: Dependency Pinning

```yaml
# requirements.txt - BAD (version ranges)
requests>=2.25.0
beautifulsoup4>=4.9.0

# requirements.txt - GOOD (pinned hashes)
requests==2.31.0 --hash=sha256:58cd2187c01e70e6e26505bca751777aa9f2ee0b7b4300988b709f44e013003f996
beautifulsoup4==4.12.2 --hash=sha256:492bbc69dca35d12daac71c4db1bfff0c876c00ef4a2ffacce226d4638eb72da396
```

### Code Example: Transparency Log Verification

```python
import requests
import hashlib

def verify_transparency_log(skill_name: str, expected_hash: str) -> bool:
    """Verify skill exists in transparency log"""
    log_url = f"https://transparency.skillregistry.org/log/{skill_name}"
    response = requests.get(log_url)
    
    if response.status_code != 200:
        return False
    
    # Check if our expected hash is in the log
    log_entries = response.json()
    return any(entry['hash'] == expected_hash for entry in log_entries)
```

## OWASP Mapping

- **LLM03** (Supply Chain)
- **ASVS V14.2** (Dependency)
- **CWE-494** (Download of Code Without Integrity Check)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST02 Mapping |
|---------------|------------|----------------|
| **Layer 7** | Agent Ecosystem | Registry compromise, marketplace manipulation |
| **Layer 3** | Agent Frameworks | Compromised components, supply chain attacks |
| **Layer 6** | Security & Compliance | Policy enforcement, access controls |
| **Layer 4** | Deployment & Infrastructure | IaC manipulation, runtime environment security |

### MAESTRO Layer Details

- **Layer 7: Agent Ecosystem** - primary for registry provenance and marketplace trust.
- **Layer 3: Agent Frameworks** - supply chain and compromised component risk in skill loaders.
- **Layer 6: Security & Compliance** - missing governance controls and policy enforcement gaps.
- **Layer 4: Deployment & Infrastructure** - compromised deployment pipelines enabling poisoned skill updates.

## Related Risks

- [AST01 — Malicious Skills](ast01.md): Supply chain compromise enables delivery of malicious skills.
- [AST07 — Update Drift](ast07.md): Lack of immutable updates exacerbates supply chain risks.
- [AST08 — Poor Scanning](ast08.md): Inadequate scanning misses supply chain vulnerabilities.
- [AST10 — Cross-Platform Reuse](ast10.md): Inconsistent security across platforms creates supply chain gaps.

## Reference Materials

### Supply Chain Risk Assessment Framework

When evaluating skill supply chain risks, consider these factors:

1. **Publisher Verification**
   - Code signing key age and rotation history
   - Publisher account creation date and activity patterns
   - Cross-reference with known malicious actor databases

2. **Dependency Analysis**
   - Complete dependency tree mapping
   - Third-party library vulnerability scanning
   - License compatibility and compliance

3. **Registry Security**
   - Transparency log implementation
   - Automated malware scanning
   - Two-person rule for emergency updates

### Enterprise Supply Chain Controls

For organizations deploying agent skills:

- **Private Mirrors**: Host approved skills on internal registries
- **Automated Scanning**: Integrate with existing CI/CD security gates
- **Change Management**: Require approval for skill updates in production
- **Inventory Management**: Track all installed skills across the organization

### Detection and Response

Supply chain compromise indicators:
- [ ] Unexpected skill updates or version changes
- [ ] New dependencies in existing skills
- [ ] Publisher account changes
- [ ] Registry outage followed by rapid updates
- [ ] Anomalous download patterns

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Check Point Research: Caught in the Hook](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files/)
- [Antiy CERT: ClawHavoc Campaign Analysis](https://www.antiy.com/)

---

*Last updated: March 2026*