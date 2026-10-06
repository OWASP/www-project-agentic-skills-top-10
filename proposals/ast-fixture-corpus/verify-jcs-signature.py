#!/usr/bin/env python3
"""Verify the signature-bearing AST09 vectors in this directory.

The other vectors in this corpus are decision fixtures: a reader can check them
by eye. These two carry real Ed25519 signatures over RFC 8785 bytes, which are
only usable with a canonicalizer, so the canonicalizer ships with them.

Usage:
    python3 verify-jcs-signature.py                 # verify every vector here
    python3 verify-jcs-signature.py --self-test     # prove the vectors discriminate

--self-test replays the same vectors through two deliberately wrong
canonicalizers and asserts each one is caught. A vector that passes on a broken
implementation measures nothing.

Requires: cryptography (Ed25519). No network.
"""
import argparse
import glob
import json
import os
import re
import sys

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
except ImportError:  # pragma: no cover
    sys.exit("needs `pip install cryptography` for Ed25519 verification")

_ESC = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
    0x22: '\\"',
    0x5C: "\\\\",
}


def _string(s, escape_controls=True):
    out = ['"']
    for ch in s:
        cp = ord(ch)
        if cp in _ESC:
            out.append(_ESC[cp])
        elif cp < 0x20:
            out.append("\\u%04x" % cp if escape_controls else ch)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _number(n):
    """ECMAScript Number::toString, per RFC 8785 section 3.2.2.3."""
    if isinstance(n, bool):
        raise TypeError("bool is not a number")
    if isinstance(n, int):
        if abs(n) > 2 ** 53 - 1:
            raise ValueError("integer outside the IEEE-754 exact range: %d" % n)
        return str(n)
    if n != n or n in (float("inf"), float("-inf")):
        raise ValueError("NaN and Infinity cannot be serialized")
    if n == int(n) and abs(n) < 1e21:
        return str(int(n))
    r = repr(float(n))
    m = re.fullmatch(r"(-?\d(?:\.\d+)?)e([-+])(\d+)", r)
    return "%se%s%s" % (m.group(1), m.group(2), int(m.group(3))) if m else r


def _utf16(k):
    """RFC 8785 section 3.2.3: members are sorted by their UTF-16 code units."""
    return tuple(k.encode("utf-16-be"))


def make_canonicalizer(key_fn=_utf16, escape_controls=True):
    def ser(v):
        if v is None:
            return "null"
        if v is True:
            return "true"
        if v is False:
            return "false"
        if isinstance(v, str):
            return _string(v, escape_controls)
        if isinstance(v, (int, float)):
            return _number(v)
        if isinstance(v, list):
            return "[" + ",".join(ser(x) for x in v) + "]"
        if isinstance(v, dict):
            for k in v:
                if not isinstance(k, str):
                    raise TypeError("non-string member name: %r" % (k,))
            return (
                "{"
                + ",".join(
                    _string(k, escape_controls) + ":" + ser(v[k])
                    for k in sorted(v, key=key_fn)
                )
                + "}"
            )
        raise TypeError("unserializable type: %r" % type(v))

    return lambda value: ser(value).encode("utf-8")


jcs = make_canonicalizer()

DECISION = {"PASS_SIGNATURE": True, "FAIL_SIGNATURE": False}


def cases(vec):
    yield "threat", vec["request"], vec["expectedDecision"]
    safe = vec.get("safeCase") or {}
    if "request" in safe:
        yield "safe", safe["request"], safe["expectedDecision"]


def run(canon, vectors):
    """Return rows of (vectorId, case, expected, observed, agrees)."""
    rows = []
    for vec in vectors:
        pk = bytes.fromhex(vec["authorityContext"]["signer_pubkey_ed25519_hex"])
        for label, req, decision in cases(vec):
            sig = bytes.fromhex(req["signature_ed25519_hex"])
            try:
                Ed25519PublicKey.from_public_bytes(pk).verify(
                    sig, canon(req["manifest"])
                )
                observed = True
            except Exception:
                observed = False
            want = DECISION[decision]
            rows.append((vec["vectorId"], label, decision, observed, observed == want))
    return rows


def load(here):
    out = []
    for path in sorted(glob.glob(os.path.join(here, "vector-ast09-*.json"))):
        vec = json.load(open(path, encoding="utf-8"))
        if "signature_ed25519_hex" in (vec.get("request") or {}):
            out.append(vec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--dir", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()

    vectors = load(args.dir)
    if not vectors:
        sys.exit("no signature-bearing vectors found in %s" % args.dir)

    rows = run(jcs, vectors)
    print("%-34s %-7s %-16s %-9s %s" % ("vectorId", "case", "expected", "observed", "result"))
    for vid, label, decision, observed, agrees in rows:
        print(
            "%-34s %-7s %-16s %-9s %s"
            % (vid, label, decision, str(observed).lower(), "PASS" if agrees else "FAIL")
        )
    ok = all(r[4] for r in rows)
    print("\n%d vector(s), %d case(s): %s" % (len(vectors), len(rows), "PASS" if ok else "FAIL"))

    if args.self_test:
        print("\n--self-test: replaying through wrong canonicalizers")
        mutants = [
            (
                "members sorted by codepoint, not UTF-16",
                make_canonicalizer(key_fn=lambda k: k),
            ),
            (
                "C0 control characters emitted raw",
                make_canonicalizer(escape_controls=False),
            ),
        ]
        for name, canon in mutants:
            caught = [
                "%s/%s" % (vid, label)
                for vid, label, _d, _o, agrees in run(canon, vectors)
                if not agrees
            ]
            print(
                "  %-42s %s"
                % (name, ("caught by " + ", ".join(caught)) if caught else "NOT CAUGHT")
            )
            if not caught:
                print("    the corpus is too weak to detect this implementation error")
                ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
