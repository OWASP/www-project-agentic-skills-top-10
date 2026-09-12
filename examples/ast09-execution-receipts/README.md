# AST09 denied-before-dispatch: execution-receipt vector

A runnable, vendor-neutral test vector for the AST09 "Execution Receipts: Implementation
Guidance" section. It demonstrates the denied-before-dispatch case: a single DENY admission
record, offline-verifiable from its own bytes, with no outcome receipt and no runtime call.

## No-signature design

The AST09 Admission receipt is the seven documented fields and carries no signature (a signature
is documented only on the Outcome receipt). This vector therefore contains no signature and no
keypair. Tamper detection is the content-derived identifier: `attempt_id` is a hash over the
admission content, so altering any preimage field makes the stored `attempt_id` fail to recompute.

## Files

- `deny-admission-receipt.json`: a valid DENY admission record with exactly the seven documented
  fields (`attempt_id`, `agent_id`, `action_type`, `scope`, `policy_version`, `decision`,
  `timestamp_ms`).
- `deny-admission-receipt.tampered.json`: the same record with `scope` altered, so the
  content-derived `attempt_id` no longer recomputes.
- `check.py`: a standalone offline checker (standard library only).

## What it demonstrates

The AST09 Key Property that denied-before-dispatch carries equal audit weight: a DENY admission
record with no outcome receipt for its `attempt_id` evidences the action was blocked before
dispatch. The checker validates the record from the bytes alone, with no call to any runtime:
the seven required fields are present, decision is DENY, and `attempt_id` recomputes from the
content preimage, which is the sole tamper-detection mechanism in a signature-free admission record.

## Run

```
python3 check.py deny-admission-receipt.json           # ALL CHECKS PASS, exit 0
python3 check.py deny-admission-receipt.tampered.json  # FAIL (attempt_id), exit 1
python3 check.py --selftest                            # asserts valid exit 0, tampered exit 1
```

## Field derivation

`attempt_id` is the lowercase sha256 hex over the RFC 8785 (JCS) canonical bytes of
`{agent_id, action_type, scope, policy_version, timestamp_ms}`, which is one derivation consistent
with the guidance's "content-derived identifier" wording and not a normative requirement (any
deterministic content-derived scheme that lets a verifier recompute the identifier and detect a
dropped or altered record satisfies the property). The `agent_id` is synthetic and `timestamp_ms`
is a fixed deterministic value, not a wall-clock read.

## Claim boundary

The checker proves record integrity and decision binding, meaning the record is intact and the
DENY decision is carried in a record whose identifier is bound to the requested scope and policy
version; it does not prove that the policy decision itself was correct, which is a separate question.

## License

Contributions to this repo are CC BY-SA 4.0 per its LICENSE.
