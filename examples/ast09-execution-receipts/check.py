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
  python3 check.py --selftest     # run six cases and assert exit code plus named output

Exit codes:
  0  all checks pass
  1  a check failed (reasons named); returned whenever any check fails, including an
     attempt_id that does not recompute
  2  usage error (bad arguments). There is no cryptography INCOMPLETE path in this
     signature-free vector.
"""

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile

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


def _reject_duplicate_names(pairs):
    """RFC 8785 forbids duplicate property names, and json.load would silently keep the
    last, so two parsers could disagree about what this record says."""
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise ValueError("duplicate property name %s: RFC 8785 forbids duplicates"
                             % json.dumps(k))
        seen.add(k)
    return dict(pairs)


def _reject_lone_surrogates(value, where="the record"):
    """No unpaired surrogate has a UTF-8 encoding. Reject the whole document up front,
    property names included, so no later step can fail on an unprintable value."""
    if isinstance(value, str):
        if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
            raise ValueError("unpaired surrogate in %s: no UTF-8 encoding exists" % where)
    elif isinstance(value, dict):
        for k, v in value.items():
            _reject_lone_surrogates(k, "a property name")
            _reject_lone_surrogates(v, "property %s" % json.dumps(k))
    elif isinstance(value, list):
        for v in value:
            _reject_lone_surrogates(v, where)


def check_receipt(path):
    """Run every check on one receipt and return an int exit code:
    0 all pass, 1 a check failed (reasons named)."""
    try:
        with open(path, encoding="utf-8") as f:
            rec = json.load(f, object_pairs_hook=_reject_duplicate_names)
        if not isinstance(rec, dict):
            print("FAIL  top-level JSON value must be an object, got %s" % type(rec).__name__)
            return 1
        _reject_lone_surrogates(rec)
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
    if domain_errors:
        print("SKIP attempt_id recompute (preimage outside the supported domain)")
    elif all(k in rec for k in ATTEMPT_ID_PREIMAGE_FIELDS):
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


def _run_case(label, argpath, expect_exit, expect_out=(), forbid_out=()):
    res = subprocess.run([sys.executable, os.path.abspath(__file__), argpath],
                         capture_output=True, text=True)
    problems = []
    if res.returncode != expect_exit:
        problems.append("expected exit %d, got %d" % (expect_exit, res.returncode))
    if res.stderr.strip():
        problems.append("stderr is not empty; a crash is not a named failure")
    if "Traceback" in res.stderr:
        problems.append("traceback present")
    for s in expect_out:
        if s not in res.stdout:
            problems.append("missing from output: %s" % json.dumps(s))
    for s in forbid_out:
        if s in res.stdout:
            problems.append("must not appear in output: %s" % json.dumps(s))
    print("  %s  %-34s %s" % ("PASS" if not problems else "FAIL", label,
                              "" if not problems else "; ".join(problems)))
    return not problems


def selftest():
    """Run six cases as subprocesses and assert exit code, empty stderr, and named output.

    Exit code alone cannot separate a named rejection from an uncaught exception, because
    both leave the process with status 1. Each case therefore also pins a string the output
    must contain, and the tampered case pins one it must not.

    Two bundled receipts cover the pass and mismatch paths. Four hostile records are built
    in a temporary directory and removed afterwards, so the cases added here contribute no
    new files to the repository."""
    here = os.path.dirname(os.path.abspath(__file__))
    print("== self-test: exit code, empty stderr, and named output ==")
    results = []

    results.append(_run_case(
        "valid fixture", os.path.join(here, "deny-admission-receipt.json"), 0,
        expect_out=("What this checker established",)))
    results.append(_run_case(
        "tampered fixture", os.path.join(here, "deny-admission-receipt.tampered.json"), 1,
        expect_out=("No property is asserted",),
        forbid_out=("What this checker established",)))

    with tempfile.TemporaryDirectory() as tmp:
        # Written as raw text: a duplicate name cannot survive a dict, so it has to
        # reach the parser as bytes.
        dup = os.path.join(tmp, "duplicate-name.json")
        with io.open(dup, "w", encoding="utf-8") as f:
            f.write('{"attempt_id":"x","agent_id":"a","action_type":"t",'
                    '"scope":"s","scope":"s","policy_version":"p",'
                    '"decision":"DENY","timestamp_ms":1}')
        results.append(_run_case(
            "duplicate property name", dup, 1,
            expect_out=("duplicate property name",)))

        # A lone surrogate is expressible in JSON source but has no UTF-8 encoding.
        sur = os.path.join(tmp, "lone-surrogate.json")
        with io.open(sur, "w", encoding="utf-8") as f:
            f.write('{"attempt_id":"x","agent_id":"\\ud800","action_type":"t",'
                    '"scope":"s","policy_version":"p","decision":"DENY","timestamp_ms":1}')
        results.append(_run_case(
            "unpaired surrogate", sur, 1,
            expect_out=("unpaired surrogate",)))

        # A float is perfectly hashable, so this exercises the domain gate itself
        # rather than riding a crash path.
        flt = os.path.join(tmp, "float-timestamp.json")
        with io.open(flt, "w", encoding="utf-8") as f:
            f.write('{"attempt_id":"x","agent_id":"a","action_type":"t","scope":"s",'
                    '"policy_version":"p","decision":"DENY","timestamp_ms":1.5}')
        results.append(_run_case(
            "float timestamp_ms", flt, 1,
            expect_out=("must be an integer", "SKIP attempt_id recompute")))

        arr = os.path.join(tmp, "top-level-array.json")
        with io.open(arr, "w", encoding="utf-8") as f:
            f.write ('[]')
        results.append(_run_case(
            "top-level array", arr, 1,
            expect_out=("top-level JSON value must be an object",)))

    if all(results):
        print("SELF-TEST PASS")
        return 0
    print("SELF-TEST FAILED: %d of %d cases did not hold. Each case pins an exit code, an "
          "empty stderr, and named output; a case that fails only on output means the "
          "checker still exits correctly while no longer saying why."
          % (len([r for r in results if not r]), len(results)))
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
