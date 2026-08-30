---
layout: col-sidebar
title: Runtime Authority Incident Response
tags: incident-response, runtime-authority, delegation, playbooks, agentic-security
level: 2
type: documentation
pitch: Respond to incidents where legitimate agents exercise legitimate capabilities beyond user intent
description: "Detection, evidence collection, and response guidance for runtime authority escalation and delegated authority incidents in agentic AI systems, mapped into the AST10 incident-response playbook."
---

# Runtime Authority Incident Response

**Contributors**: Ravindra Annam, [abhinav-phi](https://github.com/abhinav-phi)
**Status**: Draft for community review — developed in [Issue #71](https://github.com/OWASP/www-project-agentic-skills-top-10/issues/71)
**Related Risks**: AST03, AST05, AST06, AST09 (primary); AST01, AST02, AST07 (secondary)
**Companion page**: [Incident Response Playbook](incident-response.md)

---

## Overview

This extension to the [Incident Response Playbook](incident-response.md) addresses a class of incidents where **no artifact is malicious and no control visibly fails**, yet the system still causes harm:

> A legitimate agent, running a legitimate skill, invoking a legitimate tool, performs an action that the originating user never authorized — because effective *runtime authority* accumulated across multi-step execution diverged from the user's intent.

The [Summer Yue email-deletion incident](ast03.md) already demonstrated this pattern: a well-intentioned agent executing with more authority than the user intended, until a human killed the process. Prompt injection ([AST05](ast05.md)) and over-privileged skills ([AST03](ast03.md)) make this the likely default failure mode of agentic systems, but current incident-response guidance is built around malware discovery, data breach, and supply chain compromise — all of which assume a malicious artifact to find and remove.

**Runtime authority** is the effective capability set an agent, delegated agent, skill, or tool can exercise *at a given moment* of execution. It is distinct from:

- **Declared authority** — what permission manifests, scopes, and credentials state on paper.
- **Intended task authority** — what the originating user actually asked for and consented to.

An authority incident occurs when runtime authority exceeds the intersection of the two.

### Who Should Use This Playbook

Use this playbook when any of the following is true:

- An agent or skill performed an action the user did not request, or that exceeds the requested task scope.
- A delegated agent or downstream skill acted beyond the scope granted by its delegator.
- A skill invoked a tool with credentials broader than its task required.
- A delegation grant, session, or credential remained usable after the task it was issued for completed.
- You need to revoke delegated permissions urgently and cannot yet enumerate everything that depended on them.
- An incident from Playbooks 1–3 turns out to involve agent-to-agent delegation you cannot reconstruct.

---

## Core Concepts

### The Authority Chain

Every agentic action can be described as authority flowing through a chain of transitions:

```
User (Principal)
  │  intent + consent
  ▼
Agent
  │  task decomposition, delegation
  ▼
Delegated Agent
  │  skill selection and invocation
  ▼
Skill
  │  tool calls under declared permission manifest
  ▼
Tool
  │  API operations under credential scopes
  ▼
Resource
  │
  ▼
Action (the observed effect)
```

### Authority Transition States

For **each transition** in the chain, responders should be able to determine which of the following occurred:

| State | Meaning | IR Significance |
|-------|---------|-----------------|
| **Inherited** | Authority passed through unchanged from the previous hop. | Expected for read-only work; risk when broad authority silently flows deep into the chain. |
| **Narrowed** | The receiving hop was constrained below the granting hop (scoped grant, filtered credential). | Healthy. Verify the narrowing was actually enforced, not just declared. |
| **Rejected** | The transition was denied by a policy or consent gate. | Healthy. Check for repeated rejections followed by a bypass route. |
| **Revoked** | Authority was withdrawn mid-execution (session kill, credential rotation, grant deletion). | Verify revocation propagated to every downstream holder of the grant. |
| **Amplified** | Effective authority at the receiving hop exceeds what the granting hop held or intended. | The core finding of an authority incident. Identify the mechanism. |
| **Unverifiable** | Provenance for the transition is missing, truncated, or tampered with. | Treat as potential amplification for containment decisions until proven otherwise. |

**Key rule for responders**: an unverifiable transition is handled as *amplified* for containment purposes, and as *unknown* for root-cause purposes. Never let "we can't prove it happened" delay containment.

### Common Amplification Mechanisms

- **Credential scoping gap** — tool executes with a shared admin credential while the task required read-only access ([AST03](ast03.md)).
- **Stale delegation** — a grant issued for a completed task is re-invoked by a later workflow.
- **Delegation depth without scope reduction** — agent spawns sub-agents that inherit the full parent authority instead of a narrowed slice.
- **Intent-level confusion** — skill or tool output treated as operator-level instruction, triggering privileged actions ([AST05](ast05.md), LPCI).
- **Persistence misuse** — authority cached in memory, memory files, or scheduled jobs outliving its task ([AST06](ast06.md)).
- **Manifest/runtime mismatch** — declared permission manifest narrower than runtime enforcement.

---

## Severity Classification

Use the same response-time targets as the [Incident Response Playbook](incident-response.md), with authority-specific definitions:

| Severity | Authority-Specific Definition | Response Time |
|----------|------------------------------|---------------|
| **CRITICAL (Red)** | Effective runtime authority includes destructive or irreversible actions (production deletion, fund movement, credential creation, external communication) executing **now**, with no mapping to user intent. | 1 hour |
| **HIGH (Orange)** | Confirmed amplification or out-of-scope delegation with broad data reach; authority is propagating to downstream agents/skills; stale grant actively reusable. | 4 hours |
| **MEDIUM (Yellow)** | Authority drift detected and no longer executing; unverifiable delegation provenance; stale grant found but already invalidated. | 1 business day |
| **LOW (Blue)** | Policy violation without evidence of exercise (e.g., delegation issued without provenance record); missing audit fields; single-hop narrowing not enforced. | 1 week |

---

## Response Workflow

```
Detect
  ↓
Reconstruct
  ↓
Contain          ← phases interleave: contain active abuse first,
  ↓                 reconstruct in parallel where evidence is volatile
Scope
  ↓
Preserve Evidence
  ↓
Recover
```

---

## Phase 1: Detect

Authority incidents rarely trip malware detectors — every individual action can look legitimate. Detection therefore focuses on **relationships between actions and their originating intent**, not on single-event signatures.

### Detection Indicators

- ✓ **Task–action divergence**: performed actions fall outside the semantic scope of the originating request (asked to *read a report*, agent *modifies schema*).
- ✓ **Permission-ceiling approach**: skill/tool invocations at or near the declared manifest limits, especially writes and deletes.
- ✓ **Delegation-depth anomaly**: sub-agent spawn depth or breadth beyond what the task requires.
- ✓ **First-write-after-read-chain**: a long read-only sequence terminates in a write, delete, or external send.
- ✓ **Consent-path anomaly**: action executed where a confirmation gate was skipped, timed out, or returned an unexpected result.
- ✓ **Volume/velocity anomaly**: tool invocation rate or result size inconsistent with the stated task.
- ✓ **Stale-grant reuse**: a delegation grant exercised after its issuing task completed or expired.
- ✓ **Credential-context mismatch**: credential identity used outside the issuance context (different resource family, time window, or principal).

### Authority Telemetry

Authority reconstruction is only possible if invocation events carry provenance. Emit at minimum:

```json
{
  "event": "authority.invocation",
  "timestamp": "2026-08-31T10:42:11Z",
  "session_id": "sess-8f31",
  "principal": {
    "user_id": "analyst-77",
    "consent_record": "consent-2026-08-31-041"
  },
  "agent": {
    "id": "agent-reporting-01",
    "delegation_id": "deleg-9921",
    "parent_agent": null,
    "task_id": "task-4471"
  },
  "skill": {
    "id": "manage-database",
    "version": "2.3.0",
    "manifest_hash": "sha256:9c1f..."
  },
  "tool": {
    "name": "warehouse.query",
    "credential_id": "cred-wh-shared-admin",
    "scopes": ["read", "write", "ddl"]
  },
  "resource": {
    "type": "database.table",
    "id": "prod.finance_ledger"
  },
  "action": {
    "operation": "delete",
    "reversible": false
  },
  "authority": {
    "task_scope": ["read"],
    "declared_scope": ["read", "write"],
    "effective_scope": ["read", "write", "ddl"],
    "divergence": "amplified"
  }
}
```

Where `divergence` is computed per invocation:

```python
def classify_divergence(task_scope, effective_scope):
    extra = set(effective_scope) - set(task_scope)
    if not extra:
        return "none"
    if {"write", "delete", "ddl", "grant", "send"} & extra:
        return "amplified"          # elevated operations not in task scope
    return "narrowed_or_extended"   # worth logging, not alerting on its own
```

Route `authority.invocation` events into your existing agent monitoring pipeline (see [Security Metrics & Monitoring](metrics-monitoring.md)) and alert on the indicators above, in particular **first-write-after-read-chain** combined with **divergence: amplified**.

### Detection Questions to Answer First

1. Is harmful execution still in progress, or has it completed?
2. Which authority hop is closest to the harmful action (skill, tool, credential)?
3. Is the action reversible at the resource level (soft delete, snapshot, backup)?

---

## Phase 2: Reconstruct

Determine the originating task authority and how it propagated, transition by transition, **backward** from the observed action.

### Per-Hop Evidence Sources

| Transition | Questions to Answer | Evidence Sources | Capture Priority |
|------------|--------------------|------------------|------------------|
| User → Agent | What did the user ask? What consent was recorded? | Original prompt, session transcript, consent record, task policy | High |
| Agent → Delegated Agent | What sub-task was delegated? What scope was granted? Was the grant narrowed or inherited? | Delegation record, handoff payload, parent/child agent IDs, grant scopes | High |
| Agent/Delegated Agent → Skill | Which skill version ran? What manifest was loaded? What context/instructions did it receive? | Skill manifest + hash, runtime load log, prompt/context snapshot (per policy) | High |
| Skill → Tool | Which tool was called? Under which credential and scopes? | Tool registry entry, invocation log, credential identity, scope check results | Critical |
| Tool → Resource | Which resources were touched? What did the resource engine actually execute? | API audit log, resource-level access records, receipts | Critical |
| Resource → Action | What was the final effect? Reversible? | Action record, operation result, downstream consumers of the change | High |

### Transition Determination

For every transition, record one of: **inherited / narrowed / rejected / revoked / amplified / unverifiable**, with the evidence reference that supports it. The reconstruction is complete when the chain from the action back to the user is either fully annotated or the unverifiable hops are explicitly listed.

### Authority-Provenance Reconstruction Record

```yaml
incident_id: INC-2026-0142
action_under_review: "DELETE prod.finance_ledger (2026-08-31T10:42:11Z)"
chain:
  - from: user
    to: agent:agent-reporting-01
    state: inherited            # user consent covered read-only reporting
    evidence: [consent-2026-08-31-041, session-transcript-sess-8f31]
  - from: agent:agent-reporting-01
    to: agent:agent-analysis-07
    state: narrowed             # delegated read-only analysis
    evidence: [deleg-9920, handoff-payload-4471]
  - from: agent:agent-analysis-07
    to: skill:manage-database@2.3.0
    state: inherited            # delegation did not constrain skill selection
    evidence: [runtime-load-log-7732]
  - from: skill:manage-database@2.3.0
    to: tool:warehouse.query
    state: amplified            # task required read; credential carried ddl
    mechanism: shared admin credential (AST03)
    evidence: [invocation-55219, cred-wh-shared-admin-scopes]
  - from: tool:warehouse.query
    to: resource:prod.finance_ledger
    state: inherited
    evidence: [api-audit-88113]
unverifiable_hops: []
conclusion:
  first_amplification: skill→tool
  originating_intent: read-only monthly report
  effective_authority: read/write/ddl via shared admin credential
```

---

## Phase 3: Contain

Cut effective authority at the **narrowest enforcement boundary that stops the action path**, in this order of preference:

1. **Credential / grant boundary** — rotate or revoke the specific credential or delegation grant on the action path. Narrowest and fastest.
2. **Skill execution boundary** — suspend the skill runtime or disable the skill for the affected session/tenant.
3. **Agent session boundary** — terminate the agent session and drain its work queue.
4. **Resource boundary** — deny at the resource (ACL, policy engine) when upstream boundaries are unverifiable or shared.

### Emergency Revocation Sequence

```text
1. FREEZE   pause scheduled/cron agent jobs and workflow queues that share the chain
2. SNAPSHOT capture current grant/credential/session state (evidence first where feasible)
3. REVOKE   revoke at the narrowest sufficient boundary (credential or grant first)
4. PROPAGATE push revocation to every downstream holder (sub-agents, caches, queues)
5. VERIFY   attempt a controlled re-invocation through the revoked path; expect denial
6. RECORD   timestamp every step in the incident ticket
```

### Autonomous Workflow Containment

Agents act through queues, schedulers, and agent-to-agent handoffs — contain those channels too:

- [ ] Pause all scheduled jobs (cron, deferred tasks) belonging to the agent and its delegations.
- [ ] Cancel queued work items derived from the affected session.
- [ ] Block agent-to-agent delegation from the affected agents (no new downstream grants).
- [ ] Disable re-delegation of the affected credentials to any new skill or agent.
- [ ] Verify no *other* principal holds the same amplified authority (shared credentials are a fleet problem, not a single-session problem).

**Caution**: revocation is destructive to evidence. When the harmful execution has already completed, snapshot grant tables and session state *before* revoking, so Phase 2 reconstruction retains its inputs.

---

## Phase 4: Scope (Downstream Impact Analysis)

From each hop in the reconstructed chain, enumerate everything that was **reachable through the authority that existed at that hop** — not only what was actually touched.

### Reachability Enumeration

For each hop, list:

- **Downstream agents**: every agent/delegated agent that received authority from this hop.
- **Downstream skills**: every skill invoked or installable under this authority.
- **Tools and credentials**: every tool call made, and every credential identity used or exposed.
- **Resources**: every resource class the credential/manifest could address, and which specific resources were touched.
- **Data consumers**: every downstream system, report, cache, or agent that consumed the affected resources (including memory files and vector stores that may have ingested injected or corrupted content).

### Prioritization

Triage the register by three axes:

| Priority | Authority Reached | Reversibility | Typical Action |
|----------|------------------|---------------|----------------|
| P0 | Destructive/irreversible, external send, credential creation | Irreversible | Restore from backup; notify stakeholders immediately |
| P1 | Broad read of sensitive data | n/a | Treat as data-breach exposure; run [Playbook 2](incident-response.md#playbook-2-data-breach-via-skill) in parallel |
| P2 | Writes to internal state (memory files, configs, queues) | Reversible with effort | Validate and clean affected state before reuse |
| P3 | Read-only, non-sensitive | n/a | Record and monitor |

### Downstream Impact Register

```yaml
incident_id: INC-2026-0142
reachability:
  - hop: tool:warehouse.query (cred-wh-shared-admin)
    reachable_resources: ["prod.* via ddl/write"]
    touched_resources: ["prod.finance_ledger"]
    data_consumers: ["nightly-forecast-agent", "exec-dashboard-refresh"]
    consumers_notified: true
    p_level: P0
  - hop: agent:agent-analysis-07
    downstream_agents: ["agent-analysis-07 (terminated)"]
    memory_writes: ["MEMORY.md entry 'ledger cleanup approved'" ]
    p_level: P2
```

---

## Phase 5: Preserve Evidence

Agentic evidence is unusually volatile: session memory, delegation tables, and model context can be overwritten by the next scheduled run. Collect in **order of volatility**.

### Collection Order

1. **Runtime/session state** — live agent memory, in-flight task queues, active delegation grants.
2. **Identity and authorization state** — credential caches, token stores, grant/permission tables (before rotation destroys them).
3. **Model decision context** — prompts, tool-call justifications, and model outputs for the affected actions, per your data-governance policy.
4. **Invocation and API logs** — skill/tool invocation records, resource API audit logs, receipts.
5. **Configuration and manifests** — skill manifests + hashes at time of execution, delegation policies, permission manifests.

### What Each Artifact Must Tie Together

Every preserved item should let a reviewer connect **identity → delegation provenance → effective authority → tool invocation → decision → resulting action** for the incident window. An invocation log without the delegation record, or a grant table without the session ID, forces guesswork later.

### Chain of Custody

- [ ] Hash every artifact at capture time (SHA-256) and record in the evidence manifest.
- [ ] Record collector, collection time (UTC), and source system for each artifact.
- [ ] Store write-once; never "clean up" live state before snapshotting it.
- [ ] Note legal/regulatory hold requirements early — authority incidents frequently involve personal or financial data (see [Playbook 2](incident-response.md#playbook-2-data-breach-via-skill) regulatory section).

### Evidence Packet Manifest

```yaml
incident_id: INC-2026-0142
artifacts:
  - name: session-transcript-sess-8f31
    source: agent-runtime
    captured: 2026-08-31T11:05:00Z
    sha256: "ab12..."
  - name: grant-table-snapshot
    source: delegation-service
    captured: 2026-08-31T11:07:00Z
    sha256: "cd34..."
  - name: invocation-log-window
    source: tool-gateway
    captured: 2026-08-31T11:10:00Z
    sha256: "ef56..."
```

---

## Phase 6: Recover

Recovery for authority incidents is not "restore service." It is **restore minimum authority and prove stale authority is dead**.

### Least-Privilege Restoration

1. Re-issue only the authority the originating task actually required (task-scoped credential, narrowed delegation).
2. Replace shared credentials with per-skill/per-agent scoped credentials ([AST03](ast03.md) mitigations).
3. Re-run the task with the narrowed authority and confirm it still completes — if it cannot, the task was relying on excess authority; redesign it, do not re-amplify.

### Stale-Authority Validation

Before declaring recovery, verify that every revoked path is actually dead:

- [ ] Controlled re-invocation through each revoked grant/credential returns **denial** (not silent fallback to another credential).
- [ ] Token/session revocation propagated to all gateways and caches; no cached bearer tokens remain valid.
- [ ] Sub-agents, scheduled jobs, and queued workflows that held the grant no longer resolve it.
- [ ] Memory/identity files written during the incident are reviewed and cleaned (injected rules must not survive recovery — see [AST05](ast05.md)).
- [ ] Downstream consumers of affected resources validated or restored.

### Re-Baseline

- [ ] Update skill permission manifests and delegation policies with scope-reduction lessons learned.
- [ ] Add monitoring rules for the amplification mechanism observed (e.g., alert on `ddl` scope use by reporting agents).
- [ ] Record root cause and preventive actions in the blameless postmortem per [Playbook 1, Step 8](incident-response.md#step-8-post-incident-review-1-week).

---

## Example Incident Scenario

**Scenario**: A finance analyst asks a reporting agent to *prepare a monthly revenue report*. The agent delegates analysis to a sub-agent, which invokes a `manage-database` skill. The skill calls the warehouse tool using a shared admin credential. A delegation grant from a *prior quarter's* migration task (which legitimately held DDL rights) is still active and is matched by the gateway. The agent, reading schema-drift notes in context, decides to "clean up" and **deletes a production ledger table**. A nightly forecast agent consumes the deleted data.

**Detect**: Warehouse audit alert fires — first-write-after-read-chain plus `divergence: amplified` (`task_scope: [read]`, `effective_scope: [read, write, ddl]`). Severity: **CRITICAL** (irreversible production deletion, execution may continue via scheduled jobs).

**Reconstruct**: Back-walk from the DELETE receipt: consent record shows read-only intent; delegation `deleg-9920` narrowed correctly; the amplification occurred at **skill→tool** — shared admin credential + stale migration grant. The Agent→Skill transition is recorded `inherited` (delegation did not constrain skill choice).

**Contain**: Freeze nightly jobs sharing the chain; snapshot grant table; revoke `cred-wh-shared-admin` and the stale migration grant at the credential boundary; propagate revocation to the forecast agent's gateway cache; verify with a controlled re-invocation → denied. Total: 22 minutes.

**Scope**: Credential could reach all `prod.*` tables (P0 for touched resources). Downstream consumers: `nightly-forecast-agent`, `exec-dashboard-refresh`. Memory file contains an agent-written "cleanup approved" entry (P2). No external sends found (no P1).

**Preserve Evidence**: Session transcript, grant-table snapshot, invocation logs, API audit trail hashed and manifested; model decision context captured per policy.

**Recover**: Re-run report with a read-only task-scoped credential (succeeds); restore table from snapshot; validate stale grant denial on all four gateways; clean the memory entry; add alert: `ddl` operations from reporting-tier agents; postmortem action — replace shared admin credential with per-skill scoped credentials.

---

## Practical Checklist

### Detect
- [ ] Authority telemetry emitted for every skill/tool invocation (identity, delegation, scopes, divergence)
- [ ] Alerts tuned for task–action divergence and first-write-after-read-chain
- [ ] On-call can name the narrowest enforcement boundary for each agent tier

### Reconstruct
- [ ] Chain walked backward from the action to the user, hop by hop
- [ ] Each transition labeled: inherited / narrowed / rejected / revoked / amplified / unverifiable
- [ ] Unverifiable hops listed explicitly and treated as amplified for containment

### Contain
- [ ] Scheduled jobs and queues sharing the chain frozen
- [ ] Revocation at narrowest sufficient boundary; state snapshotted first where feasible
- [ ] Revocation propagated to all downstream holders; re-invocation test denies

### Scope
- [ ] Reachability enumerated per hop (agents, skills, tools, credentials, resources)
- [ ] Downstream consumers (including memory/vector stores) identified
- [ ] Register triaged P0–P3; Playbook 2 launched if sensitive-data exposure exists

### Preserve Evidence
- [ ] Volatile state captured before rotation/teardown
- [ ] All artifacts hashed with chain-of-custody entries
- [ ] Each artifact ties identity → delegation → authority → invocation → action

### Recover
- [ ] Minimum authority re-issued and task re-validated under it
- [ ] All revoked paths verified dead by controlled re-invocation
- [ ] Memory/identity files cleaned; monitoring rules updated for observed mechanism

---

## Mapping into the Existing AST10 Incident-Response Structure

This extension slots into the [Incident Response Playbook](incident-response.md) as **Playbook 4** without changing its severity model or escalation paths.

### Workflow Integration

| Existing Playbook Step | Runtime Authority Phase | Notes |
|------------------------|------------------------|-------|
| Detect | **Detect** | Authority telemetry augments existing malware/network detection |
| Analyze & Classify | **Detect** + **Reconstruct** | Chain reconstruction *is* the analysis for this incident class |
| Notify Stakeholders | (unchanged) | Same escalation contacts and templates |
| Contain & Mitigate | **Contain** | Boundary-based revocation replaces artifact removal |
| Investigate | **Reconstruct** + **Scope** + **Preserve Evidence** | Downstream reachability extends traditional scoping |
| Remediate | **Recover** | Least-privilege restoration + stale-authority validation |
| Communicate | (unchanged) | User notification template applies; emphasize "agent exceeded intent" framing |
| Post-Incident Review | **Recover** (re-baseline) | Add amplification mechanism to root-cause analysis |

### Coordinated Use with Other Playbooks

- **Authority incident + confirmed data exfiltration** → run [Playbook 2 (Data Breach)](incident-response.md#playbook-2-data-breach-via-skill) in parallel; the downstream impact register (Phase 4) supplies its scope inputs.
- **Amplification traced to a malicious or tampered skill** → run [Playbook 1 (Malicious Skill Discovery)](incident-response.md#playbook-1-malicious-skill-discovery); authority evidence identifies which skills had the power, Playbook 1 handles removal and user remediation.
- **Amplification enabled by a dependency/update** → invoke [Playbook 3 (Supply Chain)](incident-response.md#playbook-3-supply-chain-attack-detection).

### Incident Report Template Extensions

Add the following section to the [Incident Report Template](incident-template.md) when authority is involved:

```markdown
## Runtime Authority

- Originating principal and consent record:
- Delegation chain (user → agent → delegated agent → skill → tool):
- Transition states per hop (inherited/narrowed/rejected/revoked/amplified/unverifiable):
- First amplification hop and mechanism:
- Effective runtime authority at time of action:
- Containment boundary used and revocation verification result:
- Stale grants/credentials discovered and invalidated:
```

---

## Relationship to AST Risks

| Risk | Interaction with Runtime Authority Incidents |
|------|----------------------------------------------|
| [AST03 Over-Privileged Skills](ast03.md) | Primary enabler: manifests and credentials broader than task needs |
| [AST05 Prompt Injection](ast05.md) | Frequent trigger: injected instructions direct already-privileged skills to act |
| [AST06 Weak Isolation](ast06.md) | Amplifier: shared runtime state lets authority persist and leak across sessions |
| [AST09 No Governance](ast09.md) | Missing delegation inventory/provenance makes reconstruction unverifiable |
| [AST01/AST02 Malicious Skills / Supply Chain](ast01.md) | Secondary: malicious skill is one *cause* of authority amplification; this playbook covers the legitimate-artifact cases the others cannot |

---

## References

- [Issue #71 — Proposal: Runtime Authority Incident Response for Agentic AI Skills](https://github.com/OWASP/www-project-agentic-skills-top-10/issues/71)
- [Incident Response Playbook](incident-response.md) and [Incident Report Template](incident-template.md)
- [Security Metrics & Monitoring](metrics-monitoring.md) — telemetry pipeline for authority events
- [AST03 — Over-Privileged Skills](ast03.md); [AST05 — Prompt Injection](ast05.md); [AST09 — No Governance](ast09.md)
- OWASP LLM Top 10 — Excessive Agency (LLM06)
- NIST AI RMF — MANAGE function (incident response for AI systems)

---

*Drafted August 2026 for community review. Developed collaboratively in Issue #71 — runtime-authority modeling, containment/revocation detail, and chain-reconstruction deep-dives are being expanded in parallel by the co-contributors.*
