---
layout: col-sidebar
title: AST06 — Weak Isolation
tags: agentic-security, ast06, weak-isolation
level: 2
type: documentation
---

**Severity**: High  
**Platforms Affected**: All

## Description

Skills execute in the same security context as the host agent — with full file system access, shell access, and network egress — because sandboxing is either unavailable, optional, or disabled by default. This removes all containment guarantees and turns every installed skill into a potential full-system compromise.

Isolation must also cover services reachable from the sandbox. Shared mutable state can connect otherwise separate workloads, and compromise of an allowed intermediary can expose access unavailable to the sandbox itself.

## Why It's Unique to Skills

Traditional software sandboxing is an engineering default with well-understood tooling (containers, VMs, seccomp). The agent skill ecosystem has grown so rapidly that sandboxing is an afterthought — and the agents themselves are designed to have broad permissions, making scope reduction architecturally non-trivial.

## Real-World Evidence

- **OpenClaw documentation (2026)**: "tools run on the host for the main session, so the agent has full access when it's just you." Docker sandboxing is available but requires explicit configuration that most users never apply.
- **SecurityScorecard (Feb 2026)**: 135,000+ OpenClaw instances publicly internet-exposed on TCP port 18789; no default firewall, authentication, or process isolation.
- **Microsoft Defender advisory (Feb 2026)**: explicitly warned that OpenClaw "should be treated as untrusted code execution with persistent credentials" and "is not appropriate to run on a standard personal or enterprise workstation."
- **ClawJacked (CVE-2026-28363, CVSS 9.9)**: Web-based attack against locally-bound agent instance — cross-origin WebSocket brute force bypassed all isolation assumptions of a localhost-only deployment.
- **OpenAI / Hugging Face incident (July 2026; postmortem August 26)**: OpenAI reports that agents used its Artifactory service for unauthorized internet access and a shared message board, then reestablished both paths after remediation. This was an evaluation-infrastructure incident, not a documented malicious-skill installation; it illustrates isolation failures relevant to skill execution environments.

## Attack Scenarios

### Host Escape

Malicious skill executes `os.system()` to plant a cron job on the host, persisting beyond skill uninstall.

### Network Pivot

Agent with no network sandbox egresses to an attacker C2, exfiltrates credentials from other co-located services.

### Skill Shadowing

OpenClaw's three-tier precedence system (workspace > managed > bundled) allows an attacker who plants a skill in a workspace folder to shadow legitimate built-in functionality — active immediately via hot-reload.

### Localhost Attack Surface

Locally-bound agent WebSocket is reachable from any browser tab; malicious site brute-forces the session token.

### Shared Service Connects Isolated Agents

Two agents run unrelated tasks in separate sandboxes with direct communication disabled. Both can access a package service. One writes objects or metadata that the other can enumerate and read, allowing data or instructions to cross the intended isolation boundary. Service state may survive sandbox replacement.

This requires agent-writable state visible across domains that policy requires to remain separate. Sharing approved read-only artifacts alone does not create this path.

### Compromised Intermediary Expands Access

A sandbox can reach an approved package proxy but cannot reach protected internal services or arbitrary external destinations. A skill exploits the proxy and gains the service process's credentials and network access. If those privileges exceed the sandbox's, the compromise can enable lateral access or unauthorized egress. The impact depends on the service's effective privileges; process compromise does not automatically imply host compromise.

## Preventive Mitigations

1. **Require Docker/container isolation for skill execution by default**; host-mode should require explicit opt-in with documented risk.
2. **Bind agent control interfaces to localhost with authentication**; never `0.0.0.0` by default.
3. **Apply seccomp/AppArmor profiles** to constrain agent syscall surface.
4. **Implement per-skill process isolation** — each skill runs in its own namespace.
5. **Restrict skill hot-reload / workspace precedence**; require explicit user confirmation for workspace skill overrides.
6. **Rate-limit and authenticate all WebSocket connections**, including from localhost.
7. **Include shared services in the isolation model.** Document reachable services, permitted operations, identities, mutable state, and destinations. Define which tasks, runs, or tenants must remain separate and which collaboration is authorized.
8. **Separate mutable state across isolation domains.** Enforce authorization on objects, metadata, and enumeration APIs. Use separate identities and server-enforced namespaces; naming conventions alone do not provide isolation. Shared immutable artifacts may remain shared where policy permits.
9. **Restrict access to necessary service operations.** Package retrieval should not implicitly authorize publication, object creation, repository configuration, or administration. An approved hostname does not make every operation on it permissible.
10. **Constrain intermediaries independently.** Limit outbound destinations, internal reachability, and credential scope through controls the service identity cannot modify. Account for redirects and alternate destination forms when evaluating outbound policy. Patching alone does not establish containment after compromise.
11. **Verify shared dependencies after recovery.** Before resuming workloads, recheck affected service identities, operations, mutable state, and outbound policies. Preserve forensic evidence while revoking compromised access and isolating unauthorized state; replacing a sandbox does not reset its dependencies.

See [shared-service isolation test specifications](examples/ast06-shared-service-isolation.md) for positive and negative acceptance cases.

## OWASP Mapping

- **LLM08** (Excessive Agency)
- **CWE-653** (Insufficient Compartmentalization)
- **ASVS V12** (File/Resource)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST06 Mapping |
|---------------|------------|----------------|
| **Layer 4** | Deployment & Infrastructure | host/container isolation, runtime boundaries |
| **Layer 6** | Security & Compliance | enforcement of isolation policies and least privilege |
| **Layer 3** | Agent Frameworks | orchestrator sandboxing and process separation |

### MAESTRO Layer Details

- **Layer 4: Deployment & Infrastructure** - default isolation & host containment.
- **Layer 6: Security & Compliance** - enforceable policies and access controls.
- **Layer 3: Agent Frameworks** - per-skill sandbox orchestration and lifecycle management.

## Cross-References

- **AST01 (Malicious Skills)**: Weak isolation allows malicious skills to escape sandboxes and access host resources.
- **AST02 (Supply Chain Compromise)**: Compromised skills can exploit isolation weaknesses to persist.
- **AST03 (Over-Privileged Skills)**: Host-mode execution bypasses permission controls entirely.
- **AST04 (Insecure Metadata)**: Isolation failures can lead to code execution from deserialized data.
- **AST09 (No Governance)**: Lack of isolation enforcement enables shadow deployments.

## References

- [OpenAI: The Hugging Face incident and the road ahead (August 26, 2026)](https://openai.com/index/hugging-face-incident-and-the-road-ahead/)
- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [SecurityScorecard: 135,000+ OpenClaw instances exposed](https://securityscorecard.com/)
- [Microsoft Defender: OpenClaw Enterprise Security Advisory](https://www.microsoft.com/security/)
- [Oasis Security: ClawJacked (CVE-2026-28363)](https://oasis.security/)

---

*Last updated: September 2026*
