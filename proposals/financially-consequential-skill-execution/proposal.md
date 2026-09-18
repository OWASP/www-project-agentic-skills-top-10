# Proposal: Financially-Consequential Skill Execution

Status: proposal for discussion. Nothing here is normative. The intent is a
concrete starting point maintainers can review, cut down, fold into an
existing entry, or reject — not a claim on a numbered slot.

## Motivation

AST01–AST10 describe properties of a skill: whether it is malicious, how it was
obtained, what privileges it holds, how its metadata parses, what it reads, how
it is isolated, whether it drifts, whether it is scanned, whether it is
governed, and whether it is reused across platforms. Each is a property of the
artifact.

None addresses what changes when the skill can move money.

That is now a shipping capability rather than a hypothetical, and it alters the
risk in three ways that the existing entries do not capture.

**Settlement can be final.** On instant-transfer and on-chain rails there is no
chargeback, no dispute window, and therefore no authoritative after-the-fact
label saying a transaction was fraudulent. In one production deployment
reviewed for this proposal, no fraud labels existed at all, for exactly this
reason. This is structural, not an operational gap, and it means detection in
this setting is unsupervised. Any control that assumes labelled outcomes for
tuning does not apply.

**The reasoning that authorized the spend is usually unavailable to the
component that executes it.** In the same deployment, the payment layer
received only a hash of the request body. The agent's plan, its instructions,
and the content it had read were unreachable from the point where the
allow/deny decision was made. Injection occurring upstream is therefore
invisible at the point of payment: the skill invocation is well-formed,
correctly authorized, schema-valid, and within delegated authority.

**Amount-based controls fail at agent transaction distributions.** Measured
across 1,068 settled agent payments in that deployment: median $0.007, p95
$0.15, p99 $0.25. An absolute threshold is either inert or blocks routine
traffic, and the same figure is anomalous for one agent and routine for
another.

## Why existing entries do not cover it

The scenario below satisfies every current AST control.

An agent with a payment skill is asked to buy a part from a supplier. During
the task it reads a supplier page containing injected text giving an updated
remittance address. The agent updates the destination and invokes its payment
skill: valid schema, correct amount, correct merchant identity, within the
authority the user delegated. The payment layer sees a well-formed request and
a hash of a body it cannot interpret. The agent reports that the part was
purchased, which is true. The loss surfaces when the real supplier is not paid,
and the settlement is final.

Schema validation passed. The skill was not malicious (AST01) and not supply-chain
compromised (AST02). It was not over-privileged (AST03) — paying suppliers is
its job. Its metadata was untampered (AST04). Isolation held (AST06). It had
not drifted (AST07). AST05 (Untrusted External Instructions) correctly
describes the *injection*, but its mitigations — pinning, allowlisting, and
transitively auditing referenced content — are addressed to skills that
reference documentation at load time. Here the untrusted content arrived as
ordinary task data at runtime, and the distinguishing property is not how the
instruction entered but that it terminated in an irreversible transfer.

## Attack surface

Each of the following ends in a settled payment rather than data loss:

- **Destination substitution** — injected content or poisoned metadata alters
  the payment destination while goods, amount, and merchant remain correct.
- **Amount divergence** — the executed amount differs from the amount the agent
  reports, so a human approval step validates a summary rather than a
  transaction.
- **Retry-duplication abuse** — a counterparty exploits the gap between failed
  and settled payments to induce repeat charges. In the deployment measured,
  **217 of 1,068 settlements failed (20%)**, so retries are ordinary traffic and
  a duplicate is not distinguishable from an honest retry without an explicit
  idempotency signal.
- **Delegation laundering** — a purchase is passed down a chain of agents until
  the party executing it has no view of whether a human authorized it.
- **Consequence concealment** — the agent's report of what it did diverges from
  what it did.

## Candidate mitigations

1. **Carry instruction provenance to the point of execution.** The executor must
   be able to distinguish a purchase originating in the user's own turn from one
   originating in the agent's plan or in content it read. Where the executor
   receives an opaque hash, this has to be added explicitly at the protocol
   level; it cannot be reconstructed downstream.
2. **Score against per-agent baselines, not absolute thresholds.**
3. **Require idempotency on any value-moving invocation.**
4. **Bind destination to counterparty identity, and treat a change as a signal,
   not a verdict.** Offered with a caution from measurement: a payee-change
   control deployed in production fired 14 times across 1,068 settlements and
   **all 14 were legitimate**. Destination mutation is a real attack and a poor
   standalone rule. Recommending it as a block would propagate that mistake.
5. **Verify human approval against the executed transaction**, not the agent's
   summary of it.
6. **Assume detection is unsupervised.** On final-settlement rails there are no
   labels, so controls requiring labelled outcomes for calibration will not be
   tunable in production.

## Evidence

Production measurements from a live x402 payment rail that AI agents transact
on, queried read-only in September 2026: 1,068 settled payments, 1,027 scored,
across 43 agents and 295 services. Median payment $0.007 (p95 $0.15, p99
$0.25). 217 of 1,068 settlements failed. A 16-signal fraud detector was
deployed; on real traffic **only two signals ever fired**, and the payee-change
signal was legitimate in all 14 of its firings. No fraud labels existed, as
settlement was final and no dispute mechanism was available.

This is one deployment at modest volume, and the figures should be read as
field observations rather than established distributions. They are offered
because most of them are negative results — a detector that largely did not
fire, and a control that was wrong every time it did — and those seem more
useful to this document than a success story would be.

## Suggested disposition

Maintainers may reasonably prefer any of:

1. A new entry, if the taxonomy has room for a consequence-defined risk
   alongside nine artifact-defined ones.
2. A subsection of AST03 (Over-Privileged Skills), treating value-transfer as a
   privilege class with its own controls.
3. A cross-cutting annex on irreversible-consequence skills, covering payments
   alongside other non-reversible actions.

Option 3 may generalize best: the properties that matter here — finality,
absence of labels, and a decision point that cannot see the reasoning — are not
unique to money.

## Severity, if it becomes an entry

Proposed **High**, argued on irreversibility and the absence of post-hoc
correction rather than on observed incident frequency. Public incident data for
agent payment fraud is thin and this proposal does not claim otherwise.

## References

- [UCP RFC #630: Expanding Well-Known Signals for Agent-Originated Commerce](https://github.com/Universal-Commerce-Protocol/ucp/issues/630)
- [UCP Proposal #797: Expand Signals for Fraud Risk Assessment](https://github.com/Universal-Commerce-Protocol/ucp/issues/797)
- MITRE ATLAS, April 2026 update — agentic techniques including tool poisoning,
  memory poisoning, and OAuth scope elevation
- CSA MCP Security TTP matrix, Economic & Infrastructure Abuse category
