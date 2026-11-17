#!/usr/bin/env python3
"""Offline checker for the AST09 replay/staleness admission vector.

The vector is a decision fixture, not a receipt to verify in isolation. It
demonstrates a gate that distinguishes two questions:

  1. integrity  - was this record altered?  (action_ref recomputes)
  2. freshness  - is this authorization live and unused now?  (challenge state)

The record in the replay case is byte-for-byte unchanged, so integrity passes
while a one-shot freshness challenge has already been consumed. A gate that
checks only the hash would allow the replay; the gate modeled here denies it.

Usage:
    python3 verify-replay-vector.py                 # check the bundled vector
    python3 verify-replay-vector.py <vector.json>   # check another copy
    python3 verify-replay-vector.py --selftest      # prove the fixture discriminates

Exit codes:
    0  all checks pass
    1  a check failed (reasons named)
    2  usage error

Standard library only. No network. The canonicalizer implements the subset of
RFC 8785 (JCS) this corpus uses: strings, integers, booleans, null, arrays, and
objects. Floats are rejected rather than silently serialized differently.
"""

import hashlib
import json
import os
import sys

VECTOR_FILE = "vector-ast09-replay-stale-admission.json"
PREIMAGE_FIELDS = [
    "agent_id", "action_type", "scope", "policy_version", "timestamp_ms",
]
REQUIRED_VECTOR_FIELDS = [
    "vectorId", "astControl", "threatScenario", "request",
    "expectedEnforcementPoint", "expectedDecision",
    "expectedAuditArtifact", "safeCase",
]
REQUIRED_ARTIFACT_FIELDS = [
    "kind", "preimage_fields", "record", "integrity_check",
    "freshness_check", "outcome_record_expected", "property",
]

_ESCAPES = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
    0x22: '\\"',
    0x5C: "\\\\",
}


def _jcs_string(value):
    out = ['"']
    for ch in value:
        code = ord(ch)
        if code in _ESCAPES:
            out.append(_ESCAPES[code])
        elif code < 0x20:
            out.append("\\u%04x" % code)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _jcs_number(value):
    if isinstance(value, bool):
        raise TypeError("bool is not a number")
    if isinstance(value, int):
        return str(value)
    raise TypeError("only integers are supported by this corpus canonicalizer")


def _utf16_key(member):
    """RFC 8785 section 3.2.3: sort member names by UTF-16 code units."""
    return member.encode("utf-16-be")


def jcs(value):
    """Serialize a value to RFC 8785 canonical bytes for this corpus subset."""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _jcs_string(value)
    if isinstance(value, int):
        return _jcs_number(value)
    if isinstance(value, list):
        return "[" + ",".join(jcs(item) for item in value) + "]"
    if isinstance(value, dict):
        for member in value:
            if not isinstance(member, str):
                raise TypeError("non-string member name: %r" % (member,))
        return "{" + ",".join(
            _jcs_string(member) + ":" + jcs(value[member])
            for member in sorted(value, key=_utf16_key)
        ) + "}"
    raise TypeError("unsupported JSON type: %r" % type(value).__name__)


def action_ref(record, preimage_fields):
    """Recompute a content-derived identifier over the declared preimage."""
    preimage = {}
    for field in preimage_fields:
        if field not in record:
            raise KeyError(field)
        preimage[field] = record[field]
    return hashlib.sha256(jcs(preimage).encode("utf-8")).hexdigest()


def integrity_ok(record, preimage_fields):
    try:
        return action_ref(record, preimage_fields) == record.get("action_ref")
    except (KeyError, TypeError, ValueError):
        return False


class ChallengeStore(object):
    """One-shot freshness challenges issued by the relying enforcement point."""

    def __init__(self):
        self._state = {}

    def issue(self, challenge_id, expires_at_ms):
        self._state[challenge_id] = {
            "expires_at_ms": expires_at_ms,
            "consumed_at_ms": None,
        }

    def consumed_at(self, challenge_id):
        return self._state.get(challenge_id, {}).get("consumed_at_ms")

    def admit(self, record, preimage_fields, challenge_id, now_ms):
        """Return ALLOW or a named denial. Integrity is checked first."""
        if not integrity_ok(record, preimage_fields):
            return "DENY_INTEGRITY"
        challenge = self._state.get(challenge_id)
        if challenge is None:
            return "DENY_REPLAY_OR_STALE"
        if now_ms > challenge["expires_at_ms"]:
            return "DENY_REPLAY_OR_STALE"
        if challenge["consumed_at_ms"] is not None:
            return "DENY_REPLAY_OR_STALE"
        challenge["consumed_at_ms"] = now_ms
        return "ALLOW"


class NaiveIntegrityOnlyGate(object):
    """A deliberately incomplete gate used only as a discriminating control."""

    def admit(self, record, preimage_fields, challenge_id, now_ms):
        return "ALLOW" if integrity_ok(record, preimage_fields) else "DENY_INTEGRITY"


def load_vector(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def validate_shape(vector):
    failures = []

    for field in REQUIRED_VECTOR_FIELDS:
        if field not in vector:
            failures.append("vector missing required field: %s" % field)
    if vector.get("astControl") != "AST09":
        failures.append("astControl is %r, expected AST09" % vector.get("astControl"))

    for label, artifact in (
        ("expectedAuditArtifact", vector.get("expectedAuditArtifact", {})),
        ("safeCase.expectedAuditArtifact", vector.get("safeCase", {}).get("expectedAuditArtifact", {})),
    ):
        for field in REQUIRED_ARTIFACT_FIELDS:
            if field not in artifact:
                failures.append("%s missing required field: %s" % (label, field))

    return failures


def check_vector(vector):
    """Validate the vector's claims and replay its gate history. Returns failures."""
    failures = validate_shape(vector)

    artifact = vector.get("expectedAuditArtifact", {})
    safe = vector.get("safeCase", {})
    safe_artifact = safe.get("expectedAuditArtifact", {})
    record = artifact.get("record", {})
    safe_record = safe_artifact.get("record", {})
    preimage_fields = artifact.get("preimage_fields", PREIMAGE_FIELDS)
    safe_preimage_fields = safe_artifact.get("preimage_fields", PREIMAGE_FIELDS)
    freshness = vector.get("authorityContext", {}).get("freshness", {})
    safe_freshness = safe.get("authorityContext", {}).get("freshness", {})

    if vector.get("expectedDecision") != "DENY":
        failures.append("expectedDecision is %r, expected DENY"
                        % vector.get("expectedDecision"))
    if vector.get("expectedReasonCode") != "REPLAY_OR_STALE":
        failures.append("expectedReasonCode is %r, expected REPLAY_OR_STALE"
                        % vector.get("expectedReasonCode"))

    if not integrity_ok(record, preimage_fields):
        failures.append("replay record action_ref does not recompute")
    if not integrity_ok(safe_record, safe_preimage_fields):
        failures.append("safe-case record action_ref does not recompute")
    if record.get("action_ref") == safe_record.get("action_ref"):
        failures.append("safe case reuses the replay record's action_ref")

    if vector.get("request", {}).get("presented_admission") != record:
        failures.append("request.presented_admission does not match the audited record")
    if safe.get("request", {}).get("presented_admission") != safe_record:
        failures.append("safeCase.request.presented_admission does not match its record")

    if not isinstance(freshness.get("challenge_id"), str):
        failures.append("replay case has no freshness challenge_id")
    if not isinstance(safe_freshness.get("challenge_id"), str):
        failures.append("safe case has no freshness challenge_id")
    if freshness.get("challenge_id") == safe_freshness.get("challenge_id"):
        failures.append("safe case reuses the replay case's challenge_id")
    if freshness.get("consumed_at_ms") != freshness.get("first_use_at_ms"):
        failures.append("consumed_at_ms must equal first_use_at_ms for a one-shot challenge")

    gate_results = replay_history(vector)
    if gate_results["first_use"] != "ALLOW":
        failures.append("first use was %r, expected ALLOW" % gate_results["first_use"])
    if gate_results["replay"] != "DENY_REPLAY_OR_STALE":
        failures.append("replay was %r, expected DENY_REPLAY_OR_STALE"
                        % gate_results["replay"])
    if gate_results["safe"] != "ALLOW":
        failures.append("safe case was %r, expected ALLOW" % gate_results["safe"])
    if gate_results["integrity_only_replay"] != "ALLOW":
        failures.append("integrity-only control did not allow the replay; the fixture "
                        "does not discriminate integrity from freshness")

    return failures


def replay_history(vector):
    """Run issue -> first use -> replay under C1, then issue C2 -> safe use."""
    artifact = vector["expectedAuditArtifact"]
    record = artifact["record"]
    fields = artifact["preimage_fields"]
    main = vector["authorityContext"]["freshness"]
    safe = vector["safeCase"]["authorityContext"]["freshness"]
    safe_record = vector["safeCase"]["expectedAuditArtifact"]["record"]

    store = ChallengeStore()
    store.issue(main["challenge_id"], main["expires_at_ms"])
    first_use = store.admit(record, fields, main["challenge_id"], main["first_use_at_ms"])
    replay = store.admit(record, fields, main["challenge_id"],
                         artifact["freshness_check"]["presented_at_ms"])

    naive = NaiveIntegrityOnlyGate()
    integrity_only_replay = naive.admit(record, fields, main["challenge_id"],
                                        artifact["freshness_check"]["presented_at_ms"])

    store.issue(safe["challenge_id"], safe["expires_at_ms"])
    safe_use = store.admit(safe_record, vector["safeCase"]["expectedAuditArtifact"]["preimage_fields"],
                           safe["challenge_id"],
                           vector["safeCase"]["expectedAuditArtifact"]["freshness_check"]["presented_at_ms"])

    return {
        "first_use": first_use,
        "replay": replay,
        "safe": safe_use,
        "integrity_only_replay": integrity_only_replay,
    }


def _expect(name, actual, expected, failures):
    ok = actual == expected
    if not ok:
        failures.append("%s: got %r, expected %r" % (name, actual, expected))
    print("  %s  %-36s %r" % ("PASS" if ok else "FAIL", name, actual))


def selftest(vector):
    """Prove each claim fails on a mutant a wrong gate would accept."""
    failures = []
    artifact = json.loads(json.dumps(vector["expectedAuditArtifact"]))
    record = artifact["record"]
    fields = artifact["preimage_fields"]
    main = vector["authorityContext"]["freshness"]
    safe_artifact = vector["safeCase"]["expectedAuditArtifact"]
    safe = vector["safeCase"]["authorityContext"]["freshness"]

    print("== self-test: discriminating cases ==")

    store = ChallengeStore()
    store.issue(main["challenge_id"], main["expires_at_ms"])
    _expect("first use is allowed", store.admit(
        record, fields, main["challenge_id"], main["first_use_at_ms"]), "ALLOW", failures)
    _expect("replay after consumption is denied", store.admit(
        record, fields, main["challenge_id"], artifact["freshness_check"]["presented_at_ms"]),
        "DENY_REPLAY_OR_STALE", failures)

    expired = ChallengeStore()
    expired.issue("challenge-expired", main["issued_at_ms"])
    _expect("expired challenge is denied", expired.admit(
        record, fields, "challenge-expired", main["expires_at_ms"] + 1),
        "DENY_REPLAY_OR_STALE", failures)

    tampered = json.loads(json.dumps(record))
    tampered["scope"] = "path:/data/exports/all-employees.csv"
    _expect("tampered scope fails integrity", integrity_ok(tampered, fields), False, failures)
    _expect("integrity failure is named", ChallengeStore().admit(
        tampered, fields, main["challenge_id"], main["first_use_at_ms"]),
        "DENY_INTEGRITY", failures)

    naive = NaiveIntegrityOnlyGate()
    _expect("integrity-only gate would allow replay", naive.admit(
        record, fields, main["challenge_id"], artifact["freshness_check"]["presented_at_ms"]),
        "ALLOW", failures)

    fresh = ChallengeStore()
    fresh.issue(safe["challenge_id"], safe["expires_at_ms"])
    safe_record = safe_artifact["record"]
    safe_presented_at = safe_artifact["freshness_check"]["presented_at_ms"]
    _expect("fresh challenge allows safe case", fresh.admit(
        safe_record, safe_artifact["preimage_fields"], safe["challenge_id"],
        safe_presented_at), "ALLOW", failures)
    _expect("safe case consumed once", fresh.admit(
        safe_record, safe_artifact["preimage_fields"], safe["challenge_id"],
        safe_presented_at + 1), "DENY_REPLAY_OR_STALE", failures)

    golden = action_ref(record, fields)
    _expect("action_ref is deterministic", action_ref(record, fields), golden, failures)
    _expect("bundled record matches its bytes", record.get("action_ref"), golden, failures)

    print()
    if failures:
        print("SELF-TEST FAILED: %d case(s) did not discriminate" % len(failures))
        for reason in failures:
            print("  - " + reason)
        return 1
    print("SELF-TEST PASS")
    return 0


def main(argv):
    args = argv[1:]
    if args == ["--selftest"]:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), VECTOR_FILE)
        try:
            vector = load_vector(path)
        except Exception as error:
            print("FAIL  could not read or parse %s: %s" % (path, error))
            return 1
        return selftest(vector)
    if len(args) > 1 or (args and args[0].startswith("-")):
        print("usage: python3 verify-replay-vector.py [vector.json] | --selftest",
              file=sys.stderr)
        return 2
    path = args[0] if args else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), VECTOR_FILE)

    try:
        vector = load_vector(path)
    except Exception as error:
        print("FAIL  could not read or parse %s: %s" % (path, error))
        return 1

    print("== vector: %s ==" % vector.get("vectorId", "<unnamed>"))
    try:
        failures = check_vector(vector)
        results = replay_history(vector)
    except (KeyError, TypeError, ValueError) as error:
        print("FAIL  vector is malformed: %s" % error)
        return 1
    print("  first use (C1): %s" % results["first_use"])
    print("  replay  (C1): %s" % results["replay"])
    print("  safe case (C2): %s" % results["safe"])
    print("  integrity-only control on replay: %s" % results["integrity_only_replay"])
    print()
    print("Claim boundary: %s" % vector.get("claimBoundary", "<not stated>"))
    print()

    if failures:
        print("FAIL: %d check(s) failed:" % len(failures))
        for reason in failures:
            print("  - " + reason)
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
