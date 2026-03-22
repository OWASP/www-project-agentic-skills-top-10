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

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Cisco State of AI Security 2026](https://blogs.cisco.com/ai/cisco-state-of-ai-security-2026-report)
- [Bitdefender: Enterprise telemetry on shadow AI / OpenClaw deployment](https://www.bitdefender.com/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

*Last updated: March 2026*