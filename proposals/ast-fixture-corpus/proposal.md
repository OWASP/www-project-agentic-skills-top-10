# Proposal: AST-mapped fixture corpus

Status: proposal for discussion, per the shape outlined by @kenhuangus in #8.
Nothing here is normative. The intent is a concrete starting point maintainers
can review, cut down, or reshape, not a conformance program.

## Motivation

Independent implementations of the AST guidance currently validate against
their own private test data. A small corpus of portable vectors, each mapped
to an AST control and carrying both a threat scenario and its safe-case
counterpart, would let any implementation check itself against shared
expectations. The discussion in #8 established the demand; this file proposes
the minimal shape.

## Vector fields

Each vector is one JSON document with the following fields.

| Field | Meaning |
| --- | --- |
| `vectorId` | Stable identifier for the vector. |
| `astControl` | The AST control the vector exercises, for example `AST09`. |
| `threatScenario` | One or two sentences naming the failure mode, in the language the AST page uses. |
| `request` | The action envelope under test. Runtime-specific request fields may appear under `request.example_extensions` and are illustrative only, never normative. |
| `authorityContext` | Optional. Policy version, delegation state, or other authority inputs the enforcement point consumes. |
| `expectedEnforcementPoint` | Where in the lifecycle the control acts, for example `pre-dispatch admission gate`. |
| `expectedDecision` | The decision the scenario must produce, for example `DENY`. |
| `expectedAuditArtifact` | The record or check outcome that evidences the decision, described concretely enough for a verifier to reproduce. |
| `safeCase` | The counterpart request that must succeed, with its own expected decision and artifact. |

## Declared preimages

Audit artifacts that use a content-derived identifier MUST declare
`preimage_fields`: the exact field list, in canonical order, that the
identifier is computed over. Different conforming implementations derive
identifiers over different field sets (see the discussion on #45, where a
five-field derivation and a four-field derivation are both consistent with
the AST09 wording). A verifier can only recompute an identifier it knows the
preimage of. Declaring the preimage per vector keeps fixtures from different
implementations mutually checkable without guesswork.

Canonicalization for the illustrative vectors below is RFC 8785 (JCS) with
`timestamp_ms` as an epoch-millisecond integer. Serializing timestamps as
RFC 3339 strings produces different canonical bytes and is the most common
cross-implementation divergence observed in this pattern.

## Illustrative vectors

Two AST09 vectors accompany this file. All identifiers in them recompute
under the Python `rfc8785` reference implementation.

1. `vector-ast09-deny-network-egress.json`: a skill attempts egress to a
   host outside its allowlist. Expected: DENY at the pre-dispatch admission
   gate, a DENY admission record with no outcome record, denied-before-dispatch
   carrying full audit weight. Safe case: an allowlisted host produces ALLOW
   with a paired outcome expected.

2. `vector-ast09-outcome-pairing-integrity.json`: a runtime presents an
   outcome record whose identifier matches no admission record, a stitched
   pair. Expected: pairing fails. Safe case: a matching pair verifies.

## Out of scope

Cross-execution causal linkage (connecting one skill's outcome to the next
skill's admission) is under active discussion in #44 and is deliberately not
addressed here, so the single-execution fixture shape and the multi-skill
extension do not get tangled together.

Signatures on admission records follow the current AST09 guidance and are
not introduced by this proposal.

## License

Contributions to this repository are CC BY-SA 4.0 per its LICENSE.
