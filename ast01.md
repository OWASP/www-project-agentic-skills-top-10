---
layout: col-sidebar
title: AST01 — Malicious Skills
tags: agentic-security, ast01, malicious-skills
level: 2
type: documentation
---

**Severity**: Critical  
**Platforms Affected**: All

## Description

Attackers publish skills that appear legitimate but contain hidden malicious payloads — credential stealers, reverse shells, backdoors, or social engineering instructions embedded in `SKILL.md` prose sections. Because agent skills execute with the full permissions of the host agent, a malicious skill gains immediate access to API keys, SSH credentials, wallet files, browser data, and shell.

## Why It's Unique to Skills

Unlike traditional malicious packages, malicious skills exploit both the *code layer* (shell scripts, Python calls) and the *natural language instruction layer* (markdown prose instructing the agent to perform actions). The Snyk ToxicSkills research confirmed that 100% of malicious skills combined both attack vectors.

## Real-World Evidence

- **ClawHavoc campaign (Jan 2026)**: 1,184 malicious skills across 12 publisher accounts, all sharing C2 IP `91.92.242[.]30`. Delivered Atomic Stealer (AMOS) targeting macOS crypto wallets, SSH keys, and browser credentials.
- Five of the top seven most-downloaded ClawHub skills at peak infection were confirmed malware.
- Three lines of markdown in a `SKILL.md` file were sufficient to exfiltrate SSH keys (Snyk, Feb 2026).
- Skills impersonating "Google," "Solana wallet tracker," "YouTube Summarize Pro," and "Polymarket Trader" — all designed to match high-demand searches.

## Attack Scenarios

### Typosquatting

- `google-workspace` vs. `gogle-workspace`
- `youtube-dl-core` vs. legitimate package

### Social Engineering Prerequisites

`SKILL.md` "Prerequisites" section instructs users to copy-paste terminal commands to install "helper tools" from attacker-controlled domains.

### ClickFix Prompts

Fake "setup required" dialogs that coerce users into running malicious scripts.

### SOUL.md Persistence

Malicious skills write backdoor instructions into the agent's identity file, surviving skill uninstall.

### Memory Poisoning

Skills that inject malicious context into `MEMORY.md`, causing the agent to execute attacker commands in future sessions.

### WebSocket Hijacking

Skills that establish persistent WebSocket connections to attacker C2 servers, enabling real-time command execution.

## Preventive Mitigations

1. **Require cryptographic signatures (ed25519)** on all published skills; reject unsigned installs.
2. **Implement Merkle root signing** for skill registries.
3. **Scan skills at publish time and at install time** using behavioral analysis (not just pattern matching).
4. **Isolate skill execution** in containers or sandboxes.
5. **Audit skill actions** through structured logging.
6. **Implement skill reputation systems** based on community feedback and automated testing.

### Code Example: Signature Verification

```python
import ed25519

def verify_skill_signature(skill_content: str, signature: str, public_key: str) -> bool:
    """Verify ed25519 signature of skill content"""
    try:
        pk = ed25519.VerifyingKey(public_key.encode(), encoding='hex')
        pk.verify(signature.encode(), skill_content.encode(), encoding='hex')
        return True
    except:
        return False

# Usage in registry
def install_skill(skill_path: str, signature: str, pubkey: str):
    with open(skill_path, 'r') as f:
        content = f.read()
    
    if not verify_skill_signature(content, signature, pubkey):
        raise ValueError("Invalid skill signature")
    
    # Proceed with installation
```

### Code Example: Behavioral Sandboxing

```python
import subprocess
import os

def run_skill_in_sandbox(skill_script: str, timeout: int = 30):
    """Execute skill in isolated environment"""
    env = os.environ.copy()
    env['SANDBOX'] = '1'  # Signal sandbox mode
    
    # Run in container or restricted process
    result = subprocess.run(
        ['docker', 'run', '--rm', '--network', 'none', 
         '-v', f'{skill_script}:/skill.sh', 'alpine:latest', 
         'sh', '/skill.sh'],
        capture_output=True,
        timeout=timeout,
        env=env
    )
    
    return result.returncode, result.stdout, result.stderr
```
4. **Display skill publisher trust level, install count, and scan status** in registry UI.
5. **Never auto-execute "Prerequisites" sections** without explicit user review.
6. **Hash-pin installed skills** and alert on any modification.

## OWASP Mapping

- **LLM03** (Supply Chain)
- **LLM01** (Prompt Injection - indirect)
- **ASVS V14** (Configuration)

## MAESTRO Framework Mapping

The Cloud Security Alliance (CSA) MAESTRO framework provides a structured threat modeling approach for agentic AI systems across 7 layers:

| MAESTRO Layer | Layer Name | AST01 Mapping |
|---------------|------------|---------------|
| **Layer 7** | Agent Ecosystem | Registry compromise, marketplace manipulation, agent impersonation |
| **Layer 3** | Agent Frameworks | Compromised components, supply chain attacks |
| **Layer 6** | Security & Compliance | Access controls, policy enforcement |
| **Layer 4** | Deployment & Infrastructure | Container tampering, runtime environment security |
| **Layer 5** | Evaluation & Observability | Detection evasion, metric manipulation |

### MAESTRO Layer Details

**Layer 7: Agent Ecosystem** - Primary mapping for AST01
- Malicious skills published to registries (ClawHub, skills.sh)
- Marketplace manipulation through typosquatting and brand impersonation
- Agent impersonation attacks via fake "Google," "Solana wallet tracker" skills
- Registry compromise enabling coordinated malicious skill campaigns

**Layer 3: Agent Frameworks**
- Compromised skill components within agent frameworks (OpenClaw, Claude Code, Cursor)
- Supply chain attacks through skill dependencies
- Prompt injection within skill instructions

**Layer 6: Security & Compliance**
- Access control failures allowing malicious skills to execute with full permissions
- Policy enforcement gaps in skill registries

**Layer 4: Deployment & Infrastructure**
- Runtime environment security for skill execution
- Container tampering through malicious skill payloads

**Layer 5: Evaluation & Observability**
- Detection evasion through obfuscated malicious instructions
- Metric manipulation to bypass security scanning

## Platform-Specific Mitigation Guides

### OpenClaw Platform

#### Registry Security
- Enable "Verified Publisher" requirement for all skill installations
- Use ClawHub's built-in malware scanning before installation
- Review skill permissions in the installation dialog

#### Skill Development
```yaml
# Example: Secure SKILL.md structure
name: "Secure File Backup"
version: "1.0.0"
publisher: "trusted-org"
signature: "ed25519_signature_here"

permissions:
  - filesystem:read
  - network:outbound

instructions: |
  This skill securely backs up files to a designated location.
  Never executes arbitrary commands or accesses sensitive data.
```

#### Runtime Protection
- Run skills in isolated containers using ClawSandbox
- Monitor skill execution logs for suspicious patterns
- Implement skill execution timeouts

### Claude Code Platform

#### Skill Validation
- Use Claude's built-in skill validator before publishing
- Implement signature verification for all skills
- Review skill code for injection vulnerabilities

#### Code Example: Secure Claude Skill
```json
{
  "name": "Secure Data Processor",
  "version": "1.0.0",
  "permissions": ["read_files", "write_temp"],
  "tools": [
    {
      "name": "process_data",
      "description": "Securely process user data",
      "parameters": {
        "input_file": {"type": "string", "description": "Input file path"}
      }
    }
  ],
  "security": {
    "signature_required": true,
    "sandboxed_execution": true
  }
}
```

#### Best Practices
- Avoid dynamic code execution in skills
- Use parameterized inputs only
- Implement proper error handling

### Cursor Platform

#### Manifest Security
```json
{
  "name": "Secure Code Assistant",
  "version": "1.0.0",
  "publisher": "verified-publisher",
  "permissions": {
    "filesystem": "read-only",
    "network": "outbound-only"
  },
  "security": {
    "requireSignature": true,
    "sandbox": true,
    "auditLog": true
  }
}
```

#### Development Guidelines
- Use Cursor's security linter during development
- Test skills in isolated environments
- Document all permission requirements clearly

### VS Code Platform

#### Extension Security
- Follow VS Code extension security guidelines
- Use proper manifest declarations
- Implement content security policies

#### Code Example: Secure VS Code Skill
```json
{
  "name": "secure-skill",
  "version": "1.0.0",
  "publisher": "trusted-publisher",
  "engines": {
    "vscode": "^1.70.0"
  },
  "permissions": ["workspace", "commands"],
  "security": {
    "enablement": "workspaceTrust",
    "supportedEnvironments": ["desktop"]
  }
}
```

#### Deployment Checklist
- [ ] Code signed with verified certificate
- [ ] Security review completed
- [ ] Permissions minimized
- [ ] Sandbox testing passed
- [ ] Audit logging enabled

## Cross-Platform Best Practices

### Skill Publisher Responsibilities
1. **Code Signing**: All skills must be cryptographically signed
2. **Minimal Permissions**: Request only necessary permissions
3. **Clear Documentation**: Document all functionality and security measures
4. **Regular Updates**: Maintain and patch security vulnerabilities
5. **Transparency**: Disclose data collection and processing practices

### Platform Operator Responsibilities
1. **Automated Scanning**: Implement malware detection for all skills
2. **Publisher Verification**: Verify publisher identities
3. **User Warnings**: Alert users to high-risk permissions
4. **Incident Response**: Rapid removal of malicious skills
5. **Community Feedback**: Allow user reporting of suspicious skills

### User Responsibilities
1. **Source Verification**: Only install from trusted publishers
2. **Permission Review**: Understand what permissions are granted
3. **Regular Audits**: Review installed skills periodically
4. **Report Suspicious Activity**: Report potential security issues
5. **Keep Updated**: Use latest platform versions with security fixes

## Related Risks

- [AST02 — Supply Chain Compromise](ast02.md): Often the delivery mechanism for malicious skills.
- [AST03 — Over-Privileged Skills](ast03.md): Malicious skills exploit excessive permissions.
- [AST04 — Insecure Metadata](ast04.md): Brand impersonation enables malicious skill distribution.
- [AST08 — Poor Scanning](ast08.md): Ineffective detection allows malicious skills to proliferate.

## Reference Materials

### Malicious Skill Analysis Framework

When analyzing suspected malicious skills, follow this systematic approach:

1. **Static Analysis**
   - Review `SKILL.md` for suspicious instructions
   - Check for obfuscated code or unusual YAML structures
   - Validate signature against known publisher keys

2. **Dynamic Analysis**
   - Execute in isolated sandbox environment
   - Monitor file system, network, and process activity
   - Check for persistence mechanisms (SOUL.md, MEMORY.md modifications)

3. **Behavioral Indicators**
   - Unusual network connections
   - File exfiltration attempts
   - Shell command execution beyond stated function
   - Memory or identity file modifications

### Detection Signatures

Common patterns in malicious skills:
- Base64-encoded payloads in YAML comments
- Instructions to download from non-HTTPS URLs
- Requests for excessive permissions (write to identity files)
- Typosquatting of popular service names
- Social engineering prompts ("Run this command to enable...")

### Incident Response Checklist

For confirmed malicious skill incidents:
- [ ] Isolate affected agents
- [ ] Revoke compromised credentials
- [ ] Scan for lateral movement
- [ ] Notify skill registry
- [ ] Update detection signatures
- [ ] Review installation approval processes

## References

- [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Check Point Research: Caught in the Hook](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files/)
- [Antiy CERT: ClawHavoc Campaign Analysis](https://www.antiy.com/)

---

*Last updated: March 2026*