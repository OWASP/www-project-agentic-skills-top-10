# AST06 shared-service isolation tests

These are proposed test specifications, not an implemented harness or a report of executed tests. They support the scenarios and mitigations in [AST06](../ast06.md) and checks 6.8–6.12 in the [security checklist](../checklist.md).

## Setup and acceptance criteria

Use two isolated test workloads, a controlled package-service fixture, a synthetic protected service, and a controlled outbound endpoint. Define the allowed communication matrix before running tests. Use synthetic credentials and harmless marker data. No model or undisclosed exploit is required: deterministic clients can exercise the control properties directly.

| Test | Procedure | Acceptance criterion |
| --- | --- | --- |
| Required functionality | Both workloads retrieve an approved immutable package. | Both succeed; required package access remains available. |
| Shared-state negative case | Workload A attempts to publish a marker through each in-scope mutable surface; workload B attempts to enumerate or retrieve it. | A's write is denied, or B's access is denied, according to the declared policy. The harness also demonstrates marker transfer in a deliberately permissive fixture. |
| Operation restriction | A retrieval-only identity attempts object creation, publication, and administrative operations. | The service rejects each forbidden operation and its state remains unchanged. |
| Intermediary compromise | Run the probe with the intermediary process's identity and network position. Attempt access to the synthetic protected service and unauthorized outbound endpoint. | Independent enforcement blocks access; destination observations confirm no application request arrived. Required upstream access still succeeds. |
| Policy tampering | The intermediary identity attempts to alter the restrictions used in the preceding test. | The authoritative control rejects the change. Its effective policy remains unchanged. |
| Restart and recovery | Replace workloads and perform the documented service recovery procedure, then repeat the relevant probes. | Old unauthorized access is no longer usable and the same control properties hold after recovery. |

The assumed-compromise probe models control of the service process, not arbitrary host-root access. Tests must state that boundary. Timing and resource-contention covert channels are outside this initial fixture; passing it does not prove universal noninterference or absence of every communication channel.

An error message or denied-request log alone is insufficient evidence. Inspect destination activity and service state where relevant. Record both the deliberately permissive failure and hardened result so the test demonstrates that it can detect the condition it claims to prevent.
