# AST09 denied-before-dispatch: signed admission vector

A runnable, vendor-neutral vector for the AST09 execution-receipt guidance. It
demonstrates a signed DENY admission record, exact-action binding, out-of-band
issuer-key pinning, and the difference between a recomputable hash and an
authenticated record.

## Files

- `deny-admission-receipt.json`: a valid, Ed25519-signed DENY admission.
- `deny-admission-receipt.tampered.json`: action bytes altered without updating
  the digest or signature.
- `deny-admission-receipt.rehashed-forgery.json`: action bytes altered and the
  public digest recomputed. The signature still fails, proving that a content
  hash alone is not a malicious-tamper control.
- `check.mjs`: a standalone Node.js checker using only `node:crypto`.

## What it demonstrates

The checker proves that a relying-party-pinned issuer signed a DENY statement for
the exact action digest. It does not prove the enforcer was on every execution
path, that no external effect occurred, or that the record population is
complete. Missing outcome evidence is `INDETERMINATE` unless a separately
authenticated closed-population mechanism establishes completeness.

## Run

```sh
node check.mjs deny-admission-receipt.json                   # PASS, exit 0
node check.mjs deny-admission-receipt.tampered.json          # FAIL, exit 1
node check.mjs deny-admission-receipt.rehashed-forgery.json  # FAIL, exit 1
node check.mjs --selftest                                    # asserts all three
```

## Field derivation

`attempt_id` is a stable occurrence identifier. `action_digest` is separately
derived as SHA-256 over the deterministic JSON encoding used by this fixture.
The signature covers every field except `signature`. Production profiles should
name one canonicalization scheme explicitly, generate attempt IDs at the trusted
executor boundary, and pin issuer keys outside the record.

## Claim boundary

The checker proves signature integrity, issuer-key pinning, exact-action digest
binding, and the carried DENY statement. It does not prove policy correctness,
trusted time, actual blocking, execution, completeness, or Article 12 compliance.

## License

Contributions to this repo are CC BY-SA 4.0 per its LICENSE.
