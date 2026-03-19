# Reference Enforcement Pattern

The following pseudocode illustrates a centralized admission controller at the execution boundary.

```python
from dataclasses import dataclass
from typing import Literal


@dataclass
class RequestContext:
    caller_id: str
    role: str
    session_capabilities: set[str]
    policy_version: str
    trace_id: str


@dataclass
class ToolRequest:
    tool_name: str
    capability: str
    object_id: str | None
    arguments: dict


@dataclass
class Decision:
    result: Literal["ALLOW", "DENY"]
    reason: str
    trace_id: str
    policy_version: str


class ToolRegistry:
    def __init__(self, tools: dict):
        self.tools = tools

    def is_registered(self, tool_name: str) -> bool:
        return tool_name in self.tools

    def get(self, tool_name: str) -> dict | None:
        return self.tools.get(tool_name)


class OwnershipService:
    def caller_owns(self, caller_id: str, object_id: str | None) -> bool:
        # Permissive default: when no object_id is provided, ownership is not
        # evaluated. Deployments that require an explicit target for destructive
        # operations should override this to deny when object_id is absent.
        if object_id is None:
            return True
        return lookup_ownership(caller_id, object_id)


class RoleService:
    def has_required_role(self, caller_role: str, required_role: str | None) -> bool:
        if required_role is None:
            return True
        return role_allows(caller_role, required_role)


class ArgumentValidator:
    def validate(self, tool_config: dict, arguments: dict) -> bool:
        return arguments_match_policy(tool_config, arguments)


class RiskEvaluator:
    def evaluate(self, request: ToolRequest, context: RequestContext) -> str:
        return classify_request_risk(request, context)  # "low", "medium", "high"


class AdmissionController:
    RISK_DENY_THRESHOLD = "high"

    def __init__(
        self,
        registry: ToolRegistry,
        ownership: OwnershipService,
        roles: RoleService,
        validator: ArgumentValidator,
        risk: RiskEvaluator,
    ):
        self.registry = registry
        self.ownership = ownership
        self.roles = roles
        self.validator = validator
        self.risk = risk

    def _emit(self, decision: Decision) -> Decision:
        audit_log(decision)
        return decision

    def evaluate(self, request: ToolRequest, context: RequestContext) -> Decision:
        if not self.registry.is_registered(request.tool_name):
            return self._emit(Decision("DENY", "TOOL_NOT_REGISTERED", context.trace_id, context.policy_version))

        tool_config = self.registry.get(request.tool_name)

        if request.capability not in context.session_capabilities:
            return self._emit(Decision("DENY", "CAPABILITY_NOT_AUTHORIZED", context.trace_id, context.policy_version))

        if not self.ownership.caller_owns(context.caller_id, request.object_id):
            return self._emit(Decision("DENY", "OBJECT_OWNERSHIP_FAILED", context.trace_id, context.policy_version))

        required_role = tool_config.get("required_role")
        if not self.roles.has_required_role(context.role, required_role):
            return self._emit(Decision("DENY", "ROLE_NOT_AUTHORIZED", context.trace_id, context.policy_version))

        if not self.validator.validate(tool_config, request.arguments):
            return self._emit(Decision("DENY", "ARGUMENT_VALIDATION_FAILED", context.trace_id, context.policy_version))

        risk_level = self.risk.evaluate(request, context)
        if risk_level == self.RISK_DENY_THRESHOLD:
            return self._emit(Decision("DENY", "REQUEST_RISK_TOO_HIGH", context.trace_id, context.policy_version))
        if risk_level == "medium":
            return self._emit(Decision("ALLOW", "POLICY_CHECKS_PASSED_ELEVATED_RISK", context.trace_id, context.policy_version))

        return self._emit(Decision("ALLOW", "POLICY_CHECKS_PASSED", context.trace_id, context.policy_version))
```

Helper functions such as `lookup_ownership`, `role_allows`, `arguments_match_policy`,
`classify_request_risk`, and `audit_log` are placeholders representing implementation-specific
policy logic. Every decision — ALLOW or DENY — is emitted through `audit_log` to ensure a
complete, tamper-evident trail.

The risk deny threshold is exposed as a class-level constant (`RISK_DENY_THRESHOLD`) so
deployments can adjust it. Requests classified as `"medium"` risk are allowed but tagged with
a distinct reason (`POLICY_CHECKS_PASSED_ELEVATED_RISK`) so downstream consumers can apply
additional controls such as human-in-the-loop confirmation or enhanced monitoring.

This pattern is intentionally simple. The key property is not the specific implementation,
but the presence of a centralized execution gate that can make deterministic decisions before
side effects occur.
