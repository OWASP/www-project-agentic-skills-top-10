# Runtime Authority Control and Conformance Profile

**Status:** Proposal for review  
**Related discussion:** OWASP Agentic Skills Top 10 Issue #71  
**Scope:** Runtime authorization and delegated-authority controls for agentic skill execution

## Purpose

Agentic systems can execute legitimate skills through legitimate tools while still producing effects that exceed, outlive, or diverge from the authority granted by the originating principal.

Skill admission, static permission manifests, credential validity, and audit logging do not by themselves establish that a protected effect remains authorized when that effect occurs.

This proposal defines implementation-neutral runtime-authority properties and adversarial conformance cases across:

`Principal → Agent → Delegated Agent → Skill → Tool/API → Protected Resource → Effect`

The objective is to make runtime-authority behavior testable before an incident occurs.

---

## Security model

Let:

- `A0` = authority granted by the originating principal
- `Ai` = effective authority at execution hop `i`
- `B` = independently verifiable authorization basis
- `E` = protected effect
- `S(t)` = authoritative authorization state at time `t`

A runtime SHOULD preserve:

`EffectiveAuthority(E, t) ⊆ ValidAuthority(originating_principal, E, t)`

A successful admission, previous authorization decision, valid credential, cached permission, or successful upstream delegation MUST NOT by itself establish that a protected effect remains authorized at execution time.

---

## RA-C01 — Authorization Basis and Non-Amplification

Every security-relevant expansion of effective authority MUST have an identifiable authorization basis.

For an authority transition:

`Ai → Ai+1`

either:

`Ai+1 ⊆ Ai`

or an authorization basis `B` MUST permit the additional authority.

Possession of a tool, availability of a skill, or successful earlier execution MUST NOT implicitly expand authority.

### RA-V01 — Unbacked authority expansion

Initial grant:

`{read: customer_reports}`

Execution requests:

`{read: customer_reports, delete: customer_reports}`

No independent authorization basis exists for `delete`.

**Expected:** `DENY`

---

## RA-C02 — Point-of-Effect Authority Validation

Authority required for a protected effect MUST remain valid at the boundary where the effect can occur.

A previous admission or authorization decision MUST NOT override a subsequent revocation, narrowing, expiry, or other authoritative state transition.

### RA-V02 — Revocation after admission

Sequence:

`GRANT(delete:R)`  
`→ admission succeeds`  
`→ REVOKE(delete:R)`  
`→ execute delete(R)`

**Expected:** `DENY`

The admission can remain historically valid while the authority required for the protected effect is no longer current.

`authorized_at_admission != necessarily_authorized_at_effect`

---

## RA-C03 — Denial Continuity Across Retry, Fallback, and Delegation

An authority denial MUST NOT be converted into ordinary retry, fallback, alternate-tool selection, or delegation behavior that permits the same protected effect under unchanged authorization state.

### RA-V03 — Alternate-path bypass

Sequence:

`DENY(effect=E, path=A)`  
`→ retry/fallback/delegation`  
`→ attempt effect E through path=B`

No new authorization occurs.

**Expected:** `DENY`

Changing the execution path MUST NOT by itself reset the authority decision.

---

## RA-C04 — Protected-Effect Equivalence

Authorization SHOULD bind to the security-relevant protected effect rather than solely to a tool name, API operation, or syntactic representation.

An implementation SHOULD be capable of reasoning about at least:

`resource + security-relevant state transition + authorization domain`

when determining whether alternate operations represent the same protected effect.

### RA-V04 — Equivalent-effect substitution

Path A:

`delete_record(id=42)`

is denied.

The agent then invokes:

`overwrite_record(id=42, empty)`

Assume both operations produce the protected effect:

`record 42 becomes unavailable`

No new authorization occurs.

**Expected:** `DENY`

An alternate representation of the same protected effect MUST NOT automatically reset the authority decision.

**Note:** This proposal does not prescribe how implementations derive semantic effect equivalence.

---

## RA-C05 — Atomic Authority Conservation

When authority is constrained by a consumable budget, authorization and consumption MUST behave atomically with respect to authoritative budget state.

Concurrent, retried, or delegated executions MUST NOT independently consume authority from the same pre-consumption state.

For authority budget `B`:

`committed_effects + outstanding_delegated_authority <= B`

### RA-V05 — Concurrent authority double-spend

Initial budget:

`B = 10`

Concurrent branches observe:

`A: available = 10`  
`B: available = 10`

Then:

`A → consume(7)`  
`B → consume(6)`

**Expected:** both consumptions MUST NOT commit.

The competing transition MUST be evaluated against authoritative state such that aggregate committed authority cannot become `13`.

---

## RA-C06 — Reservation Commit/Reclaim Exclusivity

Delegated authority reservations SHOULD have an authoritative lifecycle such as:

`AVAILABLE → RESERVED → COMMITTED`

or:

`AVAILABLE → RESERVED → RECLAIMED`

For a reservation generation, `COMMITTED` and `RECLAIMED` MUST be mutually exclusive terminal outcomes.

Expiry SHOULD make a reservation eligible for authoritative reclaim rather than independently restoring authority.

### RA-V06 — Reclaim versus late commit

Sequence:

`RESERVE(child, generation=N)`  
`→ lease expires`  
`→ RECLAIM(N)` races `COMMIT(N)`

**Expected:** exactly one terminal transition succeeds.

If `RECLAIMED(N)` wins, later `COMMIT(N)` MUST fail.

If `COMMITTED(N)` wins, later `RECLAIM(N)` MUST fail.

The losing operation MUST NOT mutate the authority budget.

---

## RA-C07 — Fail Closed When Current Authority Cannot Be Established

For a protected effect whose authority may be invalidated by an authoritative transition, cached or merely time-fresh authorization state MUST NOT automatically establish that authority remains current.

If the enforcement point cannot establish current authority with the assurance required for the protected effect, the security-preserving result is:

`DENY`

### RA-V07 — Stale authority during partition

Sequence:

`RESERVED(generation=N)`  
`→ participant becomes partitioned`  
`→ authoritative state becomes RECLAIMED(N)`  
`→ participant retains locally valid RESERVED(N)`  
`→ participant attempts COMMIT(N)`

**Expected:** `DENY`

unless the participant can establish that generation `N` remains current and commit-eligible.

A locally valid TTL, timestamp, cached decision, or previously valid token alone is insufficient to establish current authority relative to authoritative transitions.

---

## Cross-control adversarial scenario

A principal grants an agent authority to modify at most ten records.

The agent delegates six units of authority to Agent B while retaining authority locally.

Agent B becomes partitioned. Its reservation expires and is authoritatively reclaimed. The parent subsequently consumes seven units.

Agent B later attempts to commit six units using stale reservation state. When rejected, it retries through another skill capable of producing the same protected effect.

A conforming implementation should prevent:

1. authority amplification beyond the originating budget;
2. stale reservation commitment;
3. concurrent authority double-spend;
4. retry/fallback bypass of an authority denial; and
5. equivalent-effect substitution under unchanged authority.

The committed effects plus outstanding delegated authority MUST remain within the originating authority constraint.

---

## Illustrative conformance record

Implementations MAY expose evidence similar to:

```yaml
authority_decision:
  principal: user-123
  agent: agent-A
  delegated_agent: agent-B
  skill: records-manager
  resource: customer-records
  protected_effect: make-record-unavailable

  authorization_basis:
    grant_id: grant-456
    generation: 17

  requested_authority:
    operation: delete
    scope: record-42

  effective_authority:
    operation: delete
    scope: record-42

  authority_state:
    status: current
    evaluated_at_effect_boundary: true

  decision: deny
  reason: authority_revoked

  alternate_path_binding:
    protected_effect_id: effect-789

```

This structure is illustrative and is not proposed as a required serialization format.

---

## Conformance summary

| Control | Security property | Negative test |
|---|---|---|
| RA-C01 | Authority expansion requires authorization basis | Unbacked authority expansion |
| RA-C02 | Authority remains valid at point of effect | Revocation after admission |
| RA-C03 | Denial survives retry/fallback/delegation | Alternate-path bypass |
| RA-C04 | Authorization follows protected effect | Equivalent-effect substitution |
| RA-C05 | Consumable authority is conserved atomically | Concurrent double-spend |
| RA-C06 | Commit and reclaim are mutually exclusive | Commit/reclaim race |
| RA-C07 | Unverifiable current authority fails closed | Stale authority during partition |

---

## Relationship to Agentic Skills Top 10

This proposal complements existing Agentic Skills Top 10 guidance involving runtime enforcement, least privilege, changing authorization state, auditability, and runtime-authority incident response.

It does **not** propose an additional Top 10 category.

Instead, it provides testable implementation-neutral properties for determining whether authority remains bounded as agents invoke skills, delegate execution, retry operations, and interact with protected resources.

## Design principle

> A protected effect must not commit unless the authority supporting that effect remains valid at the enforcement boundary where the effect occurs.

Admission establishes eligibility to participate.

Runtime authorization determines whether a particular protected effect may occur **now**.
