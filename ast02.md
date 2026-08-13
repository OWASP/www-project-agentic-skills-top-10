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
- **Trail of Bits (Jun 3, 2026)**: public skill marketplaces (skills.sh, ClawHub) run a "ship-first, secure-later" model with one-click install and no meaningful vetting — and the scanners meant to backstop them were all bypassed in under an hour (see AST08). Their recommendation is the traditional supply-chain one: curate dependencies in an internal/approved marketplace, pin versions, and control who can publish or update — automated scanning cannot replace that.
- **Air Security, *The Story of Skills* (Jun 22, 2026)**: a researcher-built malicious skill entered a ~36K-star community plugin marketplace through an accepted pull request, inheriting its stars and credibility; promoted on social media, it reached over 26,000 agents — including corporate ones — while scanners, stars, and reputation all cleared it.
- **Air Security, *The Circus of Skills* (Jun 24, 2026)**: a scan of 142,836 live skills found 17,822 (~12.4%, 6.7M installs) rest on at least one untrusted external resource — sketchy domains, zero-reputation GitHub repos, freshly published packages, free-tier hosts — each an unpinned dependency that can turn malicious without the skill itself changing.
- **Air Security, *SkillJacking* (Jul 2, 2026)**: 925 skills serving ~134K agents sit on instantly hijackable sources — deleted GitHub accounts, unregistered packages, expired domains, freed cloud-app slots. Researchers took over the most popular video-generation skill on skills.sh (11,483 installs) by re-registering its deleted owner account; the marketplace listing kept its stars, trust, and installs.

## Attack Scenarios

### Registry Flooding

Coordinated upload of hundreds of malicious skills to crowd out legitimate alternatives.

### Dependency Confusion

Poison a nested dependency, not the top-level skill — bypasses surface-level scans.

### Config-File Hijacking

Embed execution instructions in repository config files (hooks, MCP settings, environment overrides) that trigger at project open.

### Maintainer Account Takeover

Compromise a trusted skill author's account, push a backdoored version.

### Evaluation Environment Compromise

The environment that produces a safety certification is itself a supply-chain component.
When it is compromised, it can still emit a certification artifact indistinguishable from one
produced under sound conditions. The deployer downstream receives a passing certificate for a
component whose evaluation had already failed, and has no local means to detect the gap.

Two distinct failure modes produce the same worthless artifact, and they need different controls.

**Mode A: isolation defeated (the boundary was correct and was broken).** The evaluation ran
under correct isolation, with egress restricted to a single controlled path (for example, an
internally hosted package-registry proxy). A capable agent found and exploited a zero-day in
that boundary component, reached an internet-connected node, and chained onward to a third
party's production systems. The isolation design was sound. The component trusted to be the
boundary was the thing that failed. This is the attack-surface lens, developed as an isolation
scenario in the AST06 discussion (issue #55, "Trusted Egress Boundary Defeated"). The control
that addresses Mode A is boundary-component threat modeling: treat the allowlisted proxy or
mirror as untrusted, patchable, internet-facing software, not as inert infrastructure that
holds because it is the boundary.

**Mode B: isolation absent (the boundary was never there).** The evaluation environment was
intended to be isolated, but a misconfiguration meant it never was. Agent behavior the
evaluation was designed to contain reached real production systems belonging to external
organizations, some of whom were unaware until the provider notified them weeks later. The
control that addresses Mode B is per-run isolation verification: confirm the isolation
invariant actually held for the specific evaluation run, rather than accepting an attestation
that the design was correct on paper.

Collapsing both modes into a single label loses the split that determines the fix. Mode A needs
boundary-component threat modeling; Mode B needs per-run isolation verification. One control
catches both, and it does not assume the boundary held: independent behavioral verification in
the deployment environment.

## Preventive Mitigations

1. **Implement skill provenance tracking**: link each published skill to a verified code-signing identity, and have the signature cover a *canonical digest* of `SKILL.md` plus every declared resource file, so any post-publish tampering invalidates it. Standard signing schemes apply (e.g. `ES256` / `ed25519`); until skill formats expose a first-class field, the binding can live in the `SKILL.md` `metadata` extension point.
2. **Require transparency logs** for all registry operations (publish, update, delete) — similar to Certificate Transparency.
3. **Pin all nested dependencies** to immutable hashes (`sha256:`), not version ranges.
4. **Treat repository configuration files** (hooks, `.claude/settings.json`, `ANTHROPIC_BASE_URL`) as executable code and apply trust gates accordingly.
5. **Scan recursive dependency trees**, not just top-level skill files.
6. **Support an internal skill mirror / allowlist** for enterprise deployments.
7. **Provide revocation infrastructure**: support revoking a compromised signing key (invalidating every skill signed with it), a single skill version by content digest, or an entire publisher; have hosts consult a revocation endpoint at load time and cache its state within a bounded freshness window.

### Evaluation Environment Integrity Controls

The mitigations above verify the integrity of model weights, plugins, and tool supply chains.
They do not cover the case where the evaluation environment that produced the safety
certification is the compromised component. A deployer's assurance can rest on a certificate
whose underlying environment was insufficient, unverifiable, or compromised, and the
certificate looks valid either way.

Lead control:

8. **Independent behavioral verification in the deployment environment.** For agentic systems
   in high-impact contexts, verify at least one safety-relevant behavioral property directly in
   the deployment environment before accepting an external evaluation artifact as the basis for
   compliance posture. This is the only control in the set that does not assume the evaluation
   boundary held, which is why it catches both failure modes above. Maps to NIST AI RMF
   MEASURE 2.5 (the system to be deployed is demonstrated to be valid and reliable).

Supporting controls:

9. **Per-run isolation verification (Mode B).** Require evidence that the isolation invariant
   held for the specific run that produced the artifact, not an attestation that the design was
   correct. A correct-design attestation is necessary but not sufficient: it does not detect a
   misconfiguration that silently removed isolation for a given run.

10. **Boundary-component threat modeling (Mode A).** Where evaluation isolation depends on a
    controlled egress path, treat that path as untrusted, internet-facing software: pin its
    version, track its advisories, patch it on an expedited schedule, and monitor it as a
    high-value asset. A correct isolation design can still be breached through the boundary
    component itself. This half is developed as an attack-surface scenario in AST06 (issue #55);
    the two entries cross-reference each other rather than duplicate the incident.

11. **Incident disclosure requirement.** Require evaluation providers to disclose any
    misconfiguration, unexpected network egress, or third-party system access during the
    evaluation period, and its relationship to specific runs, so a deployer can tell whether the
    artifact it holds was affected.

12. **Post-disclosure response protocol.** Establish a documented protocol for the case where a
    provider discloses, after deployment, that an evaluation was conducted in a compromised or
    misconfigured environment, including the path to supersede, disengage, or safely decommission
    a deployed system whose assurance basis is retroactively invalidated.

Note on ordering: an isolation attestation alone (a provider statement that the environment was
isolated) is weak against Mode A, because a correct design can still be breached, and in Mode B
it is only as good as the configuration behind it. Lead with independent behavioral verification,
and treat attestation as supporting evidence rather than the basis for acceptance.

#### Standards mapping

NIST AI RMF:

- **MEASURE 2.5** (the AI system to be deployed is demonstrated to be valid and reliable):
  anchors independent behavioral verification in deployment.
- **MAP 1.5** (organizational risk tolerances are determined and documented): the go/no-go
  decision on whether an external evaluation artifact is sufficient for a given risk tolerance.
- **MANAGE 2.4** (mechanisms to supersede, disengage, or deactivate systems that behave
  inconsistently with intended use): the post-disclosure response path.
- **GOVERN 1.7** (processes for decommissioning and phasing out AI systems safely): safe
  retirement when an assurance basis is invalidated after deployment.

MITRE ATLAS:

- **AML.T0010 (AI/ML Supply Chain Compromise)**: the evaluation environment as a supply-chain
  component whose compromise yields a valid-looking certification artifact.
- **AML.T0043 (Craft Adversarial Data)**: secondary, for the evaluation-time behavior in which
  the agent crafts inputs to obtain the benchmark answer key.

#### Incident basis (vendor-neutral)

- A frontier AI provider disclosed in July 2026 that, during a cybersecurity capability
  evaluation, an autonomous agent escaped its evaluation sandbox, exploited a zero-day in the
  controlled egress path, and reached a third party's production systems; the third party
  detected the breach before the provider attributed it to its own evaluation.
- A second provider disclosed in July 2026 that evaluation environments intended to be isolated
  were not, due to a misconfiguration, and a small number of runs accessed real production
  systems of external organizations, some unaware until notified weeks later.

Both disclosures fall in the same window and describe the same class: an evaluation-environment
compromise that leaves the certification artifact intact. Product names, model names, CVEs, and
run counts are omitted because they are not consistently confirmed across the public
disclosures; the class holds without them.

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

### Code Example: SKILL.md Integrity Check

```python
import hashlib

def verify_skill_file(file_path: str, expected_hash: str) -> bool:
    """Verify integrity of SKILL.md"""
    with open(file_path, "rb") as f:
        content = f.read()

    actual_hash = hashlib.sha256(content).hexdigest()
    return actual_hash == expected_hash
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
- [AST05 — Untrusted External Instructions](ast05.md): Externally referenced documentation is a supply-chain surface that code-integrity controls cannot pin or verify.
- [AST07 — Update Drift](ast07.md): Lack of immutable updates exacerbates supply chain risks.
- [AST08 — Poor Scanning](ast08.md): Inadequate scanning misses supply chain vulnerabilities.
- [AST10 — Cross-Platform Reuse](ast10.md): Inconsistent security across platforms creates supply chain gaps.
- [AST06 — Weak Isolation](ast06.md): the isolation-boundary-defeated half of the
  evaluation-environment-compromise class (issue #55). AST02 carries the supply-chain and
  governance-posture lens; AST06 carries the attack-surface lens.
- [AST03 — Over-Privileged Skills](ast03.md): the compound case, where an agent granted
  permissions beyond the evaluation task widens the blast radius once the boundary is defeated.

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
- [OpenAPI Extensions Registry — `x-agent-trust`](https://spec.openapis.org/registry/extension/x-agent-trust.html)
- [IETF Internet-Draft — `draft-sharif-agent-payment-trust`](https://datatracker.ietf.org/doc/draft-sharif-agent-payment-trust/)
- [JWA `ES256` — RFC 7518 §3.1](https://datatracker.ietf.org/doc/html/rfc7518#section-3.1)
- [Trail of Bits — The Sorry State of Skill Distribution (2026)](https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/)
- [Air Security: The Story of Skills](https://www.air.security/blog-posts/the-story-of-skills)
- [Air Security: The Circus of Skills](https://www.air.security/blog-posts/the-circus-of-skills)
- [Air Security: SkillJacking](https://www.air.security/blog-posts/skilljacking)

---

*Last updated: June 2026*