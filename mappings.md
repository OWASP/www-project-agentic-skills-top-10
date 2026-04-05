# AI TIPS Governance Layer for OWASP Agentic Skills Top 10

> Enterprise Governance Crosswalk: Mapping 8-Pillar Controls and Lifecycle Gates to AST10 Skill-Level Security Risks

**Author**: Pamela Gupta, Founder & CEO, [Trusted AI](https://trustedai.ai)
**Framework**: AI TIPS V2 (Trust Integrated Pillars for Sustainability)
**Contribution to**: OWASP Agentic Skills Top 10 (AST10) Project
**AST10 Leads**: Ken Huang & Fabio Cerullo
**Date**: April 2026
**Contact**: pamela.gupta@trustedai.ai
**License**: CC-BY-SA-4.0, consistent with the AST10 project license

---

## 1. Executive Summary

The OWASP Agentic Skills Top 10 (AST10) provides the security community with the first comprehensive taxonomy of skill-level risks in AI agent ecosystems. It catalogs threats from malicious skills and supply chain compromise to weak isolation and governance gaps, grounded in real-world incidents including the ClawHavoc campaign (1,184 malicious skills), critical CVEs in Claude Code, and 135,000+ exposed agent instances.

AST10 answers **what can go wrong** at the skill level. This position paper proposes a complementary governance layer that answers **how enterprises prevent, detect, and respond** to these risks at scale using the AI TIPS framework (Trust Integrated Pillars for Sustainability).

AI TIPS is an 8-pillar, 243-control enterprise AI governance system with a six-phase gated lifecycle (Phase 0 through Phase 6), Trust Index scoring (0 to 100), and regulatory crosswalks to the EU AI Act, NIST AI RMF, ISO 42001, and CSA AI Controls Matrix. Originally created in 2019 — four years before NIST AI RMF was published — AI TIPS V2 was released on arXiv in January 2025.

This document maps each AST10 risk to the AI TIPS pillars and lifecycle gates that address it, providing enterprise security teams with a governance overlay they can operationalize immediately while NIST, ISO, and sector regulators develop agent-specific standards.

---

## 2. The Governance Gap in Agentic AI

The CSA CSAI Foundation research note "The AI Agent Governance Gap: What CISOs Need Now" (April 2026) documents a structural governance deficit facing enterprises deploying AI agents. Key findings include:

- 92% of organizations are concerned about AI agent security implications, yet most report significant gaps in AI security governance (CSA State of AI Cybersecurity 2026, 1,500+ security leaders).
- 92% of large-enterprise CISOs lack full visibility into their AI agent identities; 95% doubt they could detect or contain a compromised agent (2026 CISO AI Risk Report, 235 CISOs/CIOs).
- 64% of companies with revenue above $1 billion reported losses exceeding $1 million associated with AI system failures during 2025 (EY/AIUC-1 Consortium).
- Existing frameworks (NIST AI RMF 1.0, ISO 42001, EU AI Act) were architected before autonomous, tool-calling agents and contain structural gaps for agentic deployments.
- The first substantive NIST deliverables for agent-specific controls are not expected before late 2026; SP 800-53 control overlays for agentic systems remain in development.

This gap is precisely what AST10 addresses at the skill-security level and what AI TIPS addresses at the enterprise governance level. Together they form a complete stack: AST10 identifies **what to inspect**, AI TIPS provides the lifecycle controls, accountability structures, and trust scoring that determine **when and how** those inspections happen, **who** is responsible, and **what evidence** is produced for regulators.

---

## 3. AI TIPS Framework Overview

### 3.1 The Eight Pillars

AI TIPS organizes governance across eight essential pillars, each with mapped controls from the CSA AI Controls Matrix (AICM):

| Pillar | Focus | AICM Domains |
|--------|-------|--------------|
| 1. Cybersecurity | Protect AI systems from unauthorized access, adversarial attacks, supply chain compromise | IVS, SIM, TVM, SCM |
| 2. Privacy | Safeguard personal/sensitive data; prevent extraction and re-identification | DSP, IAM, EKM |
| 3. Ethics & Bias | Ensure fairness, detect and mitigate algorithmic bias | GRM, HRS, BCR |
| 4. Transparency | Visibility into operations, decision processes, governance structures | AMA, BCR, GRM |
| 5. Explainability | Enable understanding of how AI reaches decisions | LOG, DSP, A&A |
| 6. Regulations | Adherence to laws, standards, contractual obligations | GRM, A&A, DSP |
| 7. Audit | Systematic examination, verification of controls, evidence trails | A&A, LOG, SIM |
| 8. Accountability | Clear ownership, RACI, consequences, redress mechanisms | GRM, HRS, BCR |

### 3.2 Gated Lifecycle

AI TIPS implements a six-phase lifecycle with mandatory stage gates. Each gate requires satisfying minimum criteria across relevant pillars before progression:

| Phase | Focus | Gate Criteria |
|-------|-------|--------------|
| Phase 0 | Concept & Planning | Business case, initial risk assessment, governance structure established |
| Phase 1 | Data Collection & Preparation | Privacy/security controls validated, data quality confirmed |
| Phase 2 | Model Development & Training | Adversarial robustness, bias detection, secure supply chain |
| Phase 3 | Evaluation & Validation | Independent validation of performance, fairness, safety, security |
| Phase 4 | Deployment & Operations | Production monitoring, incident response, human oversight confirmed |
| Phase 5 | Monitoring & Improvement | Drift detection, continuous assessment, periodic re-validation |
| Phase 6 | Retirement | Safe decommissioning, data deletion, audit evidence preserved |

### 3.3 Trust Index

The Trust Index (Ti) quantifies governance maturity on a 0-to-100 scale, calculated as the weighted aggregation of Control Maturity and Risk Exposure across all eight pillars. Default weights: Cybersecurity 15%, Privacy 15%, Ethics & Bias 15%, Transparency 10%, Explainability 10%, Regulations & Compliance 15%, Audit 10%, Accountability 10%. Organizations can adjust weights to reflect industry context. The Trust Index provides the quantitative foundation that allows enterprises to compare skill governance maturity across vendors, business units, and agent deployments.

---

## 4. AST10-to-AI TIPS Crosswalk

The following table maps each AST10 risk to the AI TIPS pillars, lifecycle gates, and governance controls that address it. This is the operational core of the crosswalk.

| AST10 Risk | Sev. | AI TIPS Pillars | Lifecycle Gates | Key Governance Controls |
|------------|------|-----------------|-----------------|------------------------|
| **AST01 — Malicious Skills** | Critical | P1: Cybersecurity, P7: Audit, P8: Accountability | Phase 2 (supply chain), Phase 3 (validation), Phase 4 (deployment) | Cryptographic skill verification at install; Behavioral analysis in isolated canary env; Skill inventory with owner-of-record; IR playbook for skill compromise |
| **AST02 — Supply Chain Compromise** | Critical | P1: Cybersecurity, P6: Regulations, P7: Audit | Phase 1 (dependency ctrl), Phase 2 (SBOM), Phase 3 (provenance) | SBOM for all skill dependencies; Immutable hash pinning; Config files as executable code; Recursive dependency scanning |
| **AST03 — Over-Privileged Skills** | High | P1: Cybersecurity, P2: Privacy, P4: Transparency | Phase 0 (scoping), Phase 3 (validation), Phase 5 (drift) | Least-privilege manifest review; Domain-level network allowlists; Identity file write flagged; Per-skill scoped credentials |
| **AST04 — Insecure Metadata** | High | P4: Transparency, P3: Ethics & Bias, P7: Audit | Phase 2 (schema valid.), Phase 3 (behavior check) | Schema validation on fields; ASCII smuggling scans; Brand impersonation checks; Risk tier cross-reference |
| **AST05 — Unsafe Deserialization** | High | P1: Cybersecurity, P7: Audit | Phase 2 (secure code), Phase 3 (deser. testing) | Safe YAML/JSON loaders; Sandboxed parsing; Allowlisted config keys; Isolated dependency install |
| **AST06 — Weak Isolation** | High | P1: Cybersecurity, P8: Accountability | Phase 4 (sandbox enforce), Phase 5 (monitoring) | Container default (host opt-in); Filesystem to declared paths; Localhost with auth; Per-skill namespacing |
| **AST07 — Update Drift** | Medium | P1: Cybersecurity, P6: Regulations, P7: Audit | Phase 4 (version pin), Phase 5 (re-approval) | Immutable hash pinning; Updates gated behind approval; Signed updates required; Hot-reload disabled in prod |
| **AST08 — Poor Scanning** | Medium | P7: Audit, P1: Cybersecurity, P5: Explainability | Phase 3 (multi-tool scan), Phase 5 (continuous) | Behavioral + semantic analysis; Code and NL layers separate; Credential detection; No single-scanner reliance |
| **AST09 — No Governance** | Medium | P8: Accountability, P6: Regulations, P7: Audit, P4: Transparency | Phase 0 (governance), Phase 4 (inventory), Phase 5 (review), Phase 6 (deprov.) | Centralized skill inventory; Risk tier L0–L3; Approval workflow + audit trail; Agent NHI in IAM; Revocation process |
| **AST10 — Cross-Platform Reuse** | Medium | P1: Cybersecurity, P6: Regulations, P4: Transparency | Phase 3 (per-platform), Phase 4 (gap analysis) | Per-platform validation; Security property consistency; Cross-registry intel sharing; Universal Skill Format |

---

## 5. Threat Research Alignment

### 5.1 Google DeepMind Manipulation Study (March 2026)

Google DeepMind tested AI manipulation across 10,000+ participants in the UK, US, and India. AI models demonstrated high influence in simulated finance scenarios while health-related manipulation proved least effective. The study measured efficacy (whether AI altered beliefs) and propensity (how frequently models attempt manipulative tactics). For AST10, this validates why skill-level governance matters: a malicious or poorly governed skill in a financial context has empirically demonstrated capability to manipulate end-user decisions. AI TIPS addresses this through Phase 0 intent declaration controls, Phase 2 red teaming for manipulation propensity, Phase 3 behavioral boundary guardrails, and Phase 5 manipulation efficacy audits.

### 5.2 Google DeepMind Agent Traps Study (April 2026)

A second GDM study identifies six categories of attacks on autonomous AI agents: perception, reasoning, memory, action, multi-agent dynamics, and human supervisor manipulation. Poisoning a small number of RAG documents reliably skews agent output; agents handed over confidential data in 10 out of 10 test scenarios. These agent-level traps map directly to AST10: memory poisoning aligns with AST01 (malicious skills writing to MEMORY.md/SOUL.md), perception manipulation aligns with AST04 (insecure metadata), and action hijacking aligns with AST03 (over-privileged skills). AI TIPS lifecycle gates catch these at Phase 2 (adversarial robustness), Phase 3 (independent validation), and Phase 5 (behavioral drift monitoring).

### 5.3 CSA Governance Gap Analysis (April 2026)

The CSA CSAI Foundation confirms enterprises cannot wait for standards bodies. NIST targets an Interoperability Profile by Q4 2026; SP 800-53 overlays are further out; ISO/IEC JTC 1 operates on multi-year timelines. AI TIPS is already crosswalked to the CSA AICM (243 controls mapped to 18 AICM domains), making it a ready-to-deploy governance layer organizations can implement today.

---

## 6. The Three-Layer Governance Model

This crosswalk positions AST10 within a three-layer governance model for agentic AI:

| Layer | Framework | Scope | Answers |
|-------|-----------|-------|---------|
| Threat Research | GDM Manipulation, GDM Agent Traps | Empirical evidence of AI manipulation and agent attacks | What is the threat? |
| Skill Security | OWASP AST10, CSA MAESTRO | Skill-level risk taxonomy, platform mitigations, threat modeling | What can go wrong? |
| Enterprise Governance | AI TIPS, CSA AICM | 8-pillar controls, lifecycle gates, Trust Index, regulatory crosswalks | How do we prevent it? |

**No single layer is sufficient.** Threat research without governance is academic. Governance without threat intelligence is theoretical. Skill security without enterprise controls is unenforceable. The three layers working together create a defensible, auditable, and regulatorily aligned posture for agentic AI deployment.

---

## 7. Regulatory Alignment

AI TIPS is crosswalked to four major regulatory frameworks. Governance controls applied through the AST10-to-AI TIPS mapping simultaneously produce evidence for:

| Framework | Relevant Provisions | AST10 Connection |
|-----------|-------------------|-----------------|
| EU AI Act | Art. 9 (Risk Mgmt), Art. 14 (Human Oversight), Art. 43 (Conformity) | AST09 governance controls produce Art. 9 evidence; lifecycle gates support Art. 14 oversight |
| NIST AI RMF | Govern, Map, Measure, Manage functions | AI TIPS pillars map to all four; Trust Index provides Measure quantification |
| ISO 42001 | 38 controls across PDCA governance | AI TIPS 243 controls are a superset; ISO certification path supported |
| CSA AICM | 18 security domains, 240+ control objectives | Direct mapping; MAESTRO complements AST10 threat model |

---

## 8. Implementation Guidance

### Immediate (Week 1–2)

- Conduct an AI agent and skill inventory across all platforms in use
- Apply the AST10 Security Assessment Checklist to all deployed skills
- Classify each skill using the L0–L3 risk tier system
- Establish an approval workflow for new skill installations

### Short-term (Month 1–3)

- Map current agent deployments against the AI TIPS 8-pillar framework
- Implement lifecycle gates for new agent/skill deployments (start with Phase 3 and Phase 4)
- Deploy multi-tool scanning pipeline (behavioral + credential + dependency)
- Register agent identities as non-human identities (NHIs) in existing IAM

### Strategic (Quarter 2–4)

- Calculate Trust Index scores for each agent deployment
- Establish continuous monitoring with manipulation efficacy and propensity testing
- Build regulatory evidence packages aligned to EU AI Act, NIST AI RMF, ISO 42001
- Integrate AST10 threat intelligence into AI TIPS Phase 5 continuous improvement cycle

---

## 9. Conclusion

AST10 provides the definitive skill-level risk taxonomy for agentic AI. AI TIPS provides the enterprise governance layer that operationalizes those risks into enforceable controls, measurable trust scores, and regulatory-aligned evidence. Together with CSA MAESTRO and the GDM empirical research, these frameworks form a complete, evidence-based governance stack for agentic AI.

Organizations deploying AI agents today cannot wait for formal agent-specific standards. This crosswalk provides an operational bridge: a governance overlay enterprises can implement immediately using existing frameworks, with a clear upgrade path as standards emerge.

---

**Pamela Gupta**
Founder & CEO, Trusted AI | Creator, AI TIPS Framework
pamela.gupta@trustedai.ai

---

## References

1. OWASP Agentic Skills Top 10 (AST10). March 2026. https://owasp.org/www-project-agentic-skills-top-10/
2. Gupta, P. "AI TIPS 2.0: A Comprehensive Framework for Operationalizing AI Governance." arXiv, January 2025.
3. CSA CSAI Foundation. "The AI Agent Governance Gap: What CISOs Need Now." April 2026.
4. Google DeepMind. "Protecting People from Harmful Manipulation." March 26, 2026.
5. Google DeepMind. "AI Agent Traps: A Systematic Framework." April 2026.
6. Cloud Security Alliance. "The State of AI Cybersecurity 2026." April 2026.
7. Cybersecurity Insiders. "2026 CISO AI Risk Report." January 2026.
8. Help Net Security / EY-AIUC-1 Consortium. "Enterprise AI Agent Security 2026." March 2026.
9. NIST/CAISI. "RFI: Security Considerations for AI Agents." Docket NIST-2025-0035. January 2026.
10. NIST. "AI Agent Standards Initiative." February 2026.
11. Snyk. "ToxicSkills: Security Audit of AI Agent Skill Ecosystem." February 2026.
12. Cloud Security Alliance. "MAESTRO Threat Modeling Framework." 2025–2026.
13. Cloud Security Alliance. "AI Controls Matrix (AICM)." 2025–2026.
14. OWASP. "AST10 Security Assessment Checklist." March 2026.

---

© 2026 Trusted AI. Contributed to OWASP AST10 under CC-BY-SA-4.0. AI TIPS is a trademark of Trusted AI. Provisional patent pending.
