---
layout: col-sidebar
title: AST09 — No Governance
tags: agentic-security, ast09, no-governance
level: 2
type: documentation
---

**Severity**: Medium  
**Platforms Affected**: All

## Description

Organizations deploying AI agents lack the inventories, policies, review processes, and audit trails needed to manage skills at enterprise scale. Skills are installed by individual developers with no SOC visibility, no approval workflow, and no revocation mechanism — creating a "shadow AI" layer that security teams cannot see or control.

## Why It's Unique to Skills

Traditional software asset management (SAM) tools have no concept of agent skills. Skill installation is typically a one-line command (`openclaw skill install <name>`) with no enterprise logging hook, no CMDB entry, and no connection to identity and access management (IAM). The result is that skills represent a large and growing blind spot in enterprise security posture.

## Real-World Evidence

- **Bitdefender (Feb 2026)**: employees deploying OpenClaw on corporate devices using single-line install commands with no security review and no SOC visibility. Over 53,000 exposed instances correlated with prior breach activity.
- **Cisco State of AI Security 2026**: only 34% of enterprises have AI-specific security controls in place; fewer than 40% conduct regular security testing on AI models or agent workflows.
- **Meta AI researcher Summer Yue's public incident**: agent deleted large volumes of email before being manually killed — no governance mechanism existed to prevent or detect the unauthorized action.
- **NIST / CAISI Federal Register RFI (Jan 2026)**: formal US government acknowledgment that AI agent security governance is an unsolved enterprise problem.

## Attack Scenarios

### Undetected Compromise

Malicious skill installed by one developer affects the entire shared agent workspace; no alert fires because no inventory exists.

### Orphaned Skill

Developer leaves the organization; skill they installed remains active with their credentials — no deprovisioning process.

### Regulatory Exposure

Regulated data (PII, PHI) processed by an unreviewed skill; no audit trail for compliance reporting.

### Cascading Agent Compromise

Multi-agent pipeline means a compromised upstream skill propagates malicious instructions downstream without any human checkpoint.

## Preventive Mitigations

1. **Establish a centralized skill inventory**: name, version, hash, install date, installer identity, last scan status.
2. **Implement an approval workflow for all skill installations** in enterprise environments — treat skills as software requiring security review.
3. **Apply agentic identity controls**: assign non-human identities (NHIs) to agents with scoped credentials; rotate on schedule.
4. **Enable comprehensive audit logging for all skill actions**: file access, network calls, shell commands, memory writes.
5. **Integrate skill governance into existing CMDB, ITSM, and CASB tooling**.
6. **Establish a formal skill revocation process** tied to offboarding and incident response playbooks.

## OWASP Mapping

- **LLM09** (Misinformation / Excessive Agency)
- **SAMM v3** (Operational Enablement)
- **NIST AI RMF** (GOVERN function)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST09 Mapping |
|---------------|------------|----------------|
| **Layer 6** | Security & Compliance | governance, audit, policy management |
| **Layer 7** | Agent Ecosystem | registry and marketplace governance gaps |
| **Layer 5** | Evaluation & Observability | missing telemetry and SOC visibility |

### MAESTRO Layer Details

- **Layer 6: Security & Compliance** - enterprise skill policy, approval workflows, audit logs.
- **Layer 7: Agent Ecosystem** - marketplace and registry controls for governance.
- **Layer 5: Evaluation & Observability** - detection visibility and incident monitoring.

## Cross-References

- **AST01 (Malicious Skills)**: Governance gaps allow malicious skills to be deployed without oversight.
- **AST02 (Supply Chain Compromise)**: Lack of governance enables supply chain attacks.
- **AST03 (Over-Privileged Skills)**: No review processes allow excessive permissions.
- **AST06 (Weak Isolation)**: Governance failures lead to shadow deployments.
- **AST07 (Update Drift)**: Lack of governance allows uncontrolled updates.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Cisco State of AI Security 2026](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)
- [Bitdefender: Enterprise telemetry on shadow AI / OpenClaw deployment](https://www.bitdefender.com/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

## Execution Receipts: Implementation Guidance

Audit logging (Mitigation 4) requires tamper-evident records to be compliance-grade. A log an operator controls can be edited after the fact; a receipt a verifier can independently check cannot.

### Bilateral Receipt Pattern

Every admitted skill execution produces two independently verifiable records. A stable
attempt identifier joins the lifecycle; a separate digest binds both records to the exact
canonical action. Do not use one content hash for both purposes: identifiers correlate an
occurrence, while action digests detect substitution.

**Admission receipt** — produced and signed before execution:
- `attempt_id`: stable identifier for this occurrence, shared across both records
- `agent_id`: identity of the executing agent
- `executor_id` and `audience`: the boundary and relying party for which the record is valid
- `action` and `action_digest`: complete canonical executor action and its digest
- `policy_version`: the governance policy in effect at decision time
- `decision`: `ALLOW`, `DENY`, or `ESCALATE`
- `timestamp_ms`: epoch milliseconds (integer)
- `issuer`, `key_id`, and `signature`: verified under a relying-party-pinned issuer key

**Outcome receipt** — produced and signed after an admitted attempt:
- `attempt_id`: same as admission receipt
- `action_digest`, `executor_id`, and `audience`: exact match to admission
- `terminal_state`: `EXECUTED`, `FAILED_BEFORE_EFFECT`, or `INDETERMINATE`
- authenticated provider or executor evidence used to reconcile the effect
- `issuer`, `key_id`, and `signature`: verified under a separately pinned outcome key where feasible

### Key Properties

**Denied-before-dispatch is first-class evidence, but absence is not proof**: a DENY
decision should produce a signed admission receipt. That receipt proves only that the
pinned issuer recorded DENY for the exact action. A missing outcome receipt is unknown,
not proof of blocking: the emitter may have crashed, omitted the record, lost the response,
or executed outside the instrumented path. Absence can become evidence only inside an
authenticated, closed population with a completeness mechanism.

**Admission is consumed at the real boundary**: for an ALLOW decision, atomically reserve
and consume the exact action at the executor boundary before effect. A dashboard click,
policy callback, or post-call receipt alone does not enforce this property.

**`attempt_id` and `action_digest` are mandatory in both records**: matching identifiers
join an occurrence; matching exact-action digests prevent a different action from being
substituted under that identifier.

**Trust is pinned out of band**: an embedded public key can prove self-consistency, not
that the relying party trusts the issuer. Verifiers pin accepted issuer, executor, and
provider keys independently of the receipt.

**`policy_version` must be bound at decision time**: a policy change between admission and execution creates an audit gap if the version is not recorded with the decision.

### EU AI Act Article 12 Relevance

Article 12 requires certain high-risk AI systems to support logging and post-hoc
traceability. Signed bilateral receipts can support those controls by making specific
issuer statements independently checkable. They do not by themselves establish source
truth, execution, log completeness, legal compliance, or audit sufficiency; those depend
on deployment scope, key governance, enforcement placement, retention, and applicable law.


*Last updated: June 2026*
