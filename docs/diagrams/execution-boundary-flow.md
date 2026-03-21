# Execution Boundary Flow

```text
+-----+     +-------+     +--------------+     +----------------------+
| LLM | --> | Skill | --> | Tool Request | --> | Policy Enforcement   |
+-----+     +-------+     +--------------+     | Layer                |
  ^                                             +----------------------+
  |                                                       |      |
  |                                                    ALLOW    DENY
  |                                                       |      |
  |                                                       v      v
  |                                                 +-----------+   +------------------+
  +<-------------- (decision returned) <----------- | Execution |   | Block + Trace ID |
                                                    +-----------+   +------------------+
```

The policy enforcement layer sits between workflow intent and execution. Its role is to evaluate
the request before side effects occur and return a deterministic ALLOW or DENY based on policy,
authorization, validation, and risk checks.

The decision — whether ALLOW or DENY — is returned to the calling layer so the orchestrator
can reason about the outcome: proceed with results, retry with different parameters, request
user escalation, or abort gracefully.
