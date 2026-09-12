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

Every skill execution produces two records, linked by a content-derived identifier:

**Admission receipt** — produced before execution:
- `attempt_id`: shared identifier across both records
- `agent_id`: identity of the executing agent
- `action_type`: the skill or tool being invoked
- `scope`: resource boundary (e.g., `file:read`, `email:send`)
- `policy_version`: the governance policy in effect at decision time
- `decision`: `ALLOW`, `DENY`, or `ESCALATE`
- `timestamp_ms`: epoch milliseconds (integer)

**Outcome receipt** — produced after execution:
- `attempt_id`: same as admission receipt
- `action_ref`: content-derived join key, independently recomputable
- `terminal_state`: `COMMITTED` or `FAILED`
- `signature`: over the canonical field set

### Key Properties

**Denied-before-dispatch carries equal audit weight**: a DENY decision with no execution should produce an admission receipt. Absence of an outcome receipt for a given `attempt_id` proves the action was blocked.

**`attempt_id` is mandatory in both records**: without it, an auditor cannot confirm the admitted action and the executed action were the same.

**`policy_version` must be bound at decision time**: a policy change between admission and execution creates an audit gap if the version is not recorded with the decision.

### EU AI Act Article 12 Relevance

Article 12 (enforcement August 2, 2026) requires high-risk AI systems to maintain logs enabling post-hoc verification of system operation. Bilateral receipts with independent verifiability satisfy this requirement in a way that operator-controlled logs do not: a regulator or auditor can verify the receipt without access to the operator's infrastructure.


*Last updated: June 2026*