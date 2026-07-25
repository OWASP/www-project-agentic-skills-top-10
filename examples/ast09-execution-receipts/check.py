#!/usr/bin/env python3
"""Offline checker for the AST09 denied-before-dispatch admission-receipt vector.

The AST09 Admission receipt is seven fields and carries no signature (a signature is
documented only on the Outcome receipt). The content-derived identifier is what makes an
alteration detectable, and its reach is bounded: attempt_id is a hash over FIVE of the seven
fields (agent_id, action_type, scope, policy_version, timestamp_ms). It does not commit
`decision` and it does not commit itself. Rewriting DENY to ALLOW leaves an attempt_id that
still recomputes, so this checker asserts the decision directly rather than relying on the
identifier to carry it.

Verifies, from the record bytes alone, with no runtime call and no network:

  1. the seven required fields are present
  2. decision is DENY, asserted directly because the identifier does not cover it
  3. every preimage value is inside this canonicalizer's supported domain
  4. attempt_id recomputes from the five-field preimage (RFC 8785 / JCS, then sha256)

Canonicalization domain, stated at module level because copying jcs() out of this file
without it is a real hazard: the function below is correct for THIS vector's value space,
which is four ASCII-keyed strings and one integer. It is not a general RFC 8785
implementation. It does not handle floats, non-ASCII property names requiring UTF-16
code-unit ordering, or integers outside the I-JSON safe range. Step 3 enforces that
boundary rather than assuming it.

What absence does and does not show: a DENY admission record with no outcome receipt for its
attempt_id is consistent with the action having been blocked before dispatch. It does not
establish it. That inference needs two conditions this checker does not have: an authenticated
commitment that the set of outcome receipts examined is complete for the relevant window, and an
execution profile under which every dispatch is coupled to a receipt. Without the second, a
complete set can be empty while an action executed by a path that emits nothing. This checker
reads one record and makes no completeness claim.

Standard library only. There is no signature to verify, so there is no cryptography
dependency and no INCOMPLETE path.

Usage:
  python3 check.py deny-admission-receipt.json
  python3 check.py deny-admission-receipt.tampered.json
  python3 check.py --selftest     # run both bundled receipts and assert the exit contract

Exit codes:
  0  all checks pass
  1  a check failed (reasons named); returned whenever any check fails, including an
     attempt_id that does not recompute
  2  usage error (bad arguments). There is no cryptography INCOMPLETE path in this
     signature-free vector.
"""

import hashlib
import json
import os
import subprocess
import sys

REQUIRED_FIELDS = [
    "attempt_id", "agent_id", "action_type", "scope",
    "policy_version", "decision", "timestamp_ms",
]
ATTEMPT_ID_PREIMAGE_FIELDS = [
    "agent_id", "action_type", "scope", "policy_version", "timestamp_ms",
]


def jcs(value):
    """RFC 8785 (JCS) canonical form for this data (strings, one integer, objects,
    ASCII keys): keys sorted, no insignificant whitespace, UTF-8, integers as decimal."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def check_receipt(path):
    """Run every check on one receipt and return an int exit code:
    0 all pass, 1 a check failed (reasons named)."""
    try:
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
    except Exception as e:
        print("FAIL  could not read or parse %s: %s" % (path, e))
        return 1

    failures = []

    # 1. exactly the seven required fields present (and no extras such as a signature)
    missing = [k for k in REQUIRED_FIELDS if k not in rec]
    extra = [k for k in rec if k not in REQUIRED_FIELDS]
    if missing:
        failures.append("missing required field(s): %s" % ", ".join(missing))
    if extra:
        failures.append("unexpected field(s) for an admission receipt: %s" % ", ".join(extra))
    print("%s seven required fields present%s%s" % (
        "OK  " if not missing and not extra else "FAIL",
        "" if not missing else " (missing: %s)" % ", ".join(missing),
        "" if not extra else " (unexpected: %s)" % ", ".join(extra)))

    # 2. decision is DENY
    decision = rec.get("decision")
    ok_decision = decision == "DENY"
    if not ok_decision:
        failures.append("decision is %r, expected DENY" % decision)
    print("%s decision is DENY (got %r)" % ("OK  " if ok_decision else "FAIL", decision))

    # 3. preimage values inside this canonicalizer's supported domain (see module docstring)
    domain_errors = []
    for k in ATTEMPT_ID_PREIMAGE_FIELDS:
        if k not in rec:
            continue
        v = rec[k]
        if k == "timestamp_ms":
            if isinstance(v, bool) or not isinstance(v, int):
                domain_errors.append("%s must be an integer" % k)
            elif abs(v) > 2 ** 53 - 1:
                domain_errors.append("%s is outside the I-JSON safe integer range" % k)
        elif not isinstance(v, str):
            domain_errors.append("%s must be a string (got %s)" % (k, type(v).__name__))
    failures.extend(domain_errors)
    print("%s preimage values inside the supported canonicalization domain%s" % (
        "OK  " if not domain_errors else "FAIL",
        "" if not domain_errors else " (%s)" % "; ".join(domain_errors)))

    # 4. attempt_id recomputes from the five-field preimage. Reach is bounded; see module docstring.
    if all(k in rec for k in ATTEMPT_ID_PREIMAGE_FIELDS):
        preimage = {k: rec[k] for k in ATTEMPT_ID_PREIMAGE_FIELDS}
        expected = sha256_hex(jcs(preimage))
        ok_attempt = rec.get("attempt_id") == expected
        if not ok_attempt:
            failures.append("attempt_id does not recompute (stored %s..., recomputed %s...)"
                            % (str(rec.get("attempt_id"))[:16], expected[:16]))
        print("%s attempt_id recomputes from content preimage" % ("OK  " if ok_attempt else "FAIL"))
    else:
        failures.append("attempt_id cannot be recomputed (preimage fields missing)")
        print("FAIL attempt_id recompute (preimage fields missing)")

    # Denied-before-dispatch property. The assertion is made only when every check
    # passed; attempt_id prints on both paths because it is a diagnostic, not a claim.
    print()
    if not failures:
        print("What this checker established: the record encodes a DENY admission")
        print("decision and passed every check above. No property beyond those checks")
        print("is asserted.")
        print("Absence of an outcome receipt for this attempt_id is consistent with")
        print("the action having been blocked before dispatch. It does not establish")
        print("it. That needs two conditions this checker does not have: an")
        print("authenticated commitment that the examined receipt set is complete for")
        print("the window, and an execution profile under which every dispatch emits a")
        print("receipt. Without the second, a complete set can be empty while an")
        print("action ran by a path that emits nothing.")
    else:
        print("No property is asserted for a record whose checks did not pass.")
    print("attempt_id: %s" % rec.get("attempt_id"))

    # Honest, single exit code. Any named failure is exit 1; a full pass is exit 0.
    # There is no signature and therefore no INCOMPLETE path. Never exit 0 with any
    # check failed.
    if failures:
        print("\nFAIL: %d check(s) failed:" % len(failures))
        for reason in failures:
            print("  - " + reason)
        rc = 1
    else:
        print("\nALL CHECKS PASS")
        rc = 0
    return rc


def selftest():
    """Run both bundled receipts as subprocesses and assert the exit-code contract:
    exit 0 on the valid receipt, exit 1 on the tampered receipt. Fail loudly (nonzero)
    if either is wrong. Uses real subprocess exit codes, so it tests exactly what a
    shell sees."""
    here = os.path.dirname(os.path.abspath(__file__))
    me = os.path.abspath(__file__)
    cases = [("deny-admission-receipt.json", 0), ("deny-admission-receipt.tampered.json", 1)]
    print("== self-test: exit-code contract ==")
    all_ok = True
    for fname, expect in cases:
        res = subprocess.run([sys.executable, me, os.path.join(here, fname)],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        got = res.returncode
        ok = got == expect
        all_ok = all_ok and ok
        print("  %s  %-38s expected exit %d, got exit %d" % ("PASS" if ok else "FAIL", fname, expect, got))
    if all_ok:
        print("SELF-TEST PASS")
        return 0
    print("SELF-TEST FAILED: the exit-code contract is violated "
          "(the valid receipt must exit 0 and the tampered receipt must exit 1).")
    return 1


def main():
    args = sys.argv[1:]
    if args == ["--selftest"]:
        return selftest()
    if len(args) != 1 or args[0].startswith("-"):
        print("usage: python3 check.py <receipt.json>", file=sys.stderr)
        print("       python3 check.py --selftest", file=sys.stderr)
        return 2
    return check_receipt(args[0])


if __name__ == "__main__":
    sys.exit(main())
