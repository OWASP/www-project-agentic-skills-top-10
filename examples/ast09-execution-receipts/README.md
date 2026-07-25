# AST09 denied-before-dispatch: execution-receipt vector

A runnable, vendor-neutral test vector for the AST09 "Execution Receipts: Implementation
Guidance" section. It demonstrates the denied-before-dispatch case: a single DENY admission
record, offline-verifiable from its own bytes, with no outcome receipt and no runtime call.

## No-signature design

The AST09 Admission receipt is the seven documented fields and carries no signature (a signature
is documented only on the Outcome receipt). This vector therefore contains no signature and no
keypair.

What the content-derived `attempt_id` gives, and what it does not: altering any preimage field
makes the stored `attempt_id` fail to recompute, so an alteration is detectable by a verifier that
holds the identifier from a source other than the record itself. A party who can rewrite the record
can also rewrite the identifier, so this is not tamper evidence against the record's own writer.
With no signature on the Admission receipt, no stronger property is available from these bytes
alone.

## Files

- `deny-admission-receipt.json`: a valid DENY admission record with exactly the seven documented
  fields (`attempt_id`, `agent_id`, `action_type`, `scope`, `policy_version`, `decision`,
  `timestamp_ms`).
- `deny-admission-receipt.tampered.json`: the same record with `scope` altered, so the
  content-derived `attempt_id` no longer recomputes.
- `check.py`: a standalone offline checker (standard library only).

## What it demonstrates

The AST09 Key Property that denied-before-dispatch carries equal audit weight: a DENY admission
record is an auditable artifact in its own right, whether or not execution followed. Absence of an
outcome receipt for its `attempt_id` is consistent with the action having been blocked before
dispatch; it does not establish it. That inference needs two conditions: an authenticated
commitment that the set of outcome receipts examined is complete for the relevant window, and an
execution profile under which every dispatch is coupled to a receipt. Without the second, a
complete set can be empty while an action executed by a path that emits nothing. The checker validates the record from the bytes alone, with no call to any runtime:
the seven required fields are present, decision is DENY, and `attempt_id` recomputes from the
content preimage, which is the only integrity check available in a signature-free admission record,
subject to the limits stated above.

## Run

```
python3 check.py deny-admission-receipt.json           # ALL CHECKS PASS, exit 0
python3 check.py deny-admission-receipt.tampered.json  # FAIL (attempt_id), exit 1
python3 check.py --selftest                            # six cases: exit, stderr, named output
```

## Field derivation

`attempt_id` is the lowercase sha256 hex over the RFC 8785 (JCS) canonical bytes of
`{agent_id, action_type, scope, policy_version, timestamp_ms}`, which is one derivation consistent
with the guidance's "content-derived identifier" wording and not a normative requirement (any
deterministic content-derived scheme that lets a verifier recompute the identifier satisfies the
derivation property; a mismatch shows inconsistency between the stored identifier and the fields
it commits, while detecting that a record was omitted belongs to the record set). The `agent_id`
is synthetic and `timestamp_ms` is a fixed deterministic value, not a wall-clock read.

This five-field derivation commits agent_id, action_type, scope, policy_version and timestamp_ms,
and nothing else: it does not commit `decision` and it does not commit itself. It cannot serve as a pairing key, because a party
recomputing the identifier from the executed request would need `policy_version`, which the
executing party need not know. The four-field derivation in `proposals/ast-fixture-corpus` is a
pairing key for exactly that reason. Both fit the guidance's "content-derived identifier" wording.
They are not interchangeable.

## Claim boundary

The checker demonstrates that the record is internally consistent and that the DENY decision is
carried in a record whose identifier commits to the requested scope and policy version. It does not
show that the record is tamper evident against its own writer, that the action was not executed by
some path that produced no receipt, or that the policy decision itself was correct.

## License

Contributions to this repo are CC BY-SA 4.0 per its LICENSE.
