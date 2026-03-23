---
layout: col-sidebar
title: Skill Development Best Practices
tags: best-practices, development, security-guidelines
level: 2
type: documentation
pitch: Best practices for developing secure AI agent skills
description: "Comprehensive guidance for developing secure, maintainable AI agent skills across all platforms with security-first architecture."
---

# Skill Development Best Practices

This guide provides comprehensive best practices for developing secure, maintainable AI agent skills across OpenClaw, Claude Code, Cursor, and VS Code platforms.

## Security-First Architecture

### 1. Principle of Least Privilege

**Design Pattern**: Request only the minimum permissions needed for your skill to function.

```yaml
# WRONG - Over-privileged skill
permissions:
  - full_system_access
  - network:all
  - filesystem:write

# CORRECT - Minimal permissions
permissions:
  - filesystem:read:/documents
  - network:outbound:https://api.example.com
  - user:identity
```

**Implementation Checklist**:
- [ ] List all required permissions before development
- [ ] Remove unused permissions before publishing
- [ ] Use specific paths instead of wildcards
- [ ] Implement runtime permission checks

### 2. Input Validation & Sanitization

**Defense Pattern**: Validate all user inputs at multiple layers.

```python
import re
from typing import Optional

class SecureSkill:
    def __init__(self):
        self.max_input_length = 1024
        self.forbidden_commands = ['rm', 'dd', 'format', 'del']
    
    def validate_file_path(self, path: str) -> bool:
        """Validate file path to prevent directory traversal"""
        # Prevent path traversal attacks
        normalized = os.path.normpath(path)
        if ".." in normalized:
            return False
        
        # Check against allowed directories
        allowed_dirs = ['/documents', '/projects']
        return any(normalized.startswith(d) for d in allowed_dirs)
    
    def sanitize_command(self, cmd: str) -> Optional[str]:
        """Sanitize shell commands"""
        for forbidden in self.forbidden_commands:
            if re.search(rf'\b{forbidden}\b', cmd, re.IGNORECASE):
                return None
        
        # Additional validation
        if len(cmd) > self.max_input_length:
            return None
        
        return cmd.strip()
    
    def process_user_input(self, user_input: str) -> bool:
        """Multi-layer input validation"""
        # Layer 1: Length check
        if len(user_input) > self.max_input_length:
            raise ValueError("Input too long")
        
        # Layer 2: Character validation
        if not re.match(r'^[a-zA-Z0-9\s\-_\.]+$', user_input):
            raise ValueError("Invalid characters")
        
        # Layer 3: Semantic validation
        return True
```

### 3. Error Handling & Information Disclosure

**Security Pattern**: Don't leak sensitive information in error messages.

```python
# WRONG - Information disclosure
def process_file(filename):
    try:
        with open(filename) as f:
            return process(f)
    except Exception as e:
        return f"Error: {e}"  # Reveals system paths, internals

# CORRECT - Safe error handling
def process_file(filename):
    try:
        validate_file_path(filename)
        with open(filename) as f:
            return process(f)
    except FileNotFoundError:
        logger.warning(f"File not found: {filename}")
        return "Unable to process file"
    except Exception as e:
        logger.error(f"Processing error", exc_info=True)
        return "An error occurred processing your request"
```

### 4. Secure Data Storage

**Implementation Pattern**: Never store sensitive data in plaintext.

```python
import secrets
import json
from cryptography.fernet import Fernet

class SecureStorage:
    def __init__(self):
        self.cipher_key = os.environ.get('SKILL_CIPHER_KEY')
        if not self.cipher_key:
            raise ValueError("SKILL_CIPHER_KEY not configured")
        self.cipher = Fernet(self.cipher_key.encode())
    
    def store_credential(self, credential_type: str, value: str):
        """Encrypt and store credentials securely"""
        encrypted = self.cipher.encrypt(value.encode())
        
        storage = {
            'type': credential_type,
            'data': encrypted.decode(),
            'timestamp': datetime.now().isoformat(),
            'salt': secrets.token_hex(16)
        }
        
        # Store to secure location
        self._save_to_vault(credential_type, storage)
    
    def retrieve_credential(self, credential_type: str):
        """Retrieve and decrypt credentials"""
        storage = self._load_from_vault(credential_type)
        return self.cipher.decrypt(storage['data'].encode()).decode()
```

## Development Workflow

### Quality Assurance Process

```
┌─────────────────────────────────────────────┐
│ 1. Design & Planning                        │
│   - Security requirements                   │
│   - Permission scope                        │
│   - Data flow diagram                       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 2. Secure Implementation                    │
│   - Code review checklist                   │
│   - Input validation testing                │
│   - Permission minimization                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 3. Security Testing                         │
│   - Unit tests for input validation         │
│   - Integration tests                       │
│   - Static analysis scanning                │
│   - Penetration testing                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 4. Code Review                              │
│   - Security review                         │
│   - Permission audit                        │
│   - Documentation check                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ 5. Publication & Monitoring                 │
│   - Sign skill with ed25519                 │
│   - Publish to registry                     │
│   - Monitor for abuse                       │
└─────────────────────────────────────────────┘
```

### Pre-Publish Checklist

- [ ] All inputs are validated and sanitized
- [ ] Error messages don't leak sensitive info
- [ ] No hardcoded credentials or API keys
- [ ] Sensitive data is encrypted at rest
- [ ] Permissions are minimized
- [ ] Security review completed
- [ ] Tests cover security scenarios
- [ ] Static analysis passes
- [ ] Documentation is complete
- [ ] Signature keys are secure

## Platform-Specific Guidelines

### OpenClaw Skills

**Best Practice**: Use SKILL.md structure with clear sections.

```yaml
# skill.md
---
name: "Data Analyzer"
version: "1.0.0"
publisher: "trusted-publisher"
permissions:
  - filesystem:read:/data
  - network:outbound
---

## Description
Analyzes data files and generates reports.

## Security Considerations
- Only processes files in /data directory
- Does not execute arbitrary code
- All external requests use HTTPS

## Installation
Install from trusted sources only.

## Usage
```{instruction}
Analyze data with validation: \`data_analyzer --validate --input <file>\`
```
```

### Claude Code Skills

**Best Practice**: Leverage Claude's built-in security features.

```json
{
  "name": "secure-tool",
  "version": "1.0.0",
  "tools": [
    {
      "name": "process_data",
      "description": "Process user data securely",
      "parameters": {
        "data_path": {
          "type": "string",
          "description": "Path to data file",
          "pattern": "^/allowed/paths/.*$"
        }
      }
    }
  ],
  "security": {
    "require_user_confirmation": ["filesystem:write", "network:outbound"],
    "sandbox": true,
    "resource_limits": {
      "memory_mb": 512,
      "timeout_seconds": 30
    }
  }
}
```

### Cursor & VS Code Extensions

**Best Practice**: Implement workspace trust verification.

```json
{
  "name": "secure-extension",
  "version": "1.0.0",
  "engine": {
    "vscode": "^1.70.0"
  },
  "permissions": ["workspace"],
  "security": {
    "requireWorkspaceTrust": true,
    "requireSignature": true,
    "supportedEnvironments": ["desktop"]
  }
}
```

## Code Review Checklist

### Security Review Template

```markdown
# Security Code Review Checklist

## Authentication & Authorization
- [ ] All user inputs are validated
- [ ] Authorization checks are in place
- [ ] Least privilege principle is followed
- [ ] No hardcoded credentials

## Input Validation
- [ ] All inputs validated for type and length
- [ ] Injection attacks prevented
- [ ] Path traversal attacks prevented
- [ ] Command injection attacks prevented

## Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Encrypted in transit (HTTPS)
- [ ] No data logging of sensitive info
- [ ] Proper data retention policies

## Error Handling
- [ ] Errors logged securely
- [ ] No sensitive info in error messages
- [ ] Graceful failure modes
- [ ] User-friendly error messages

## Dependencies
- [ ] All dependencies reviewed
- [ ] No known vulnerabilities
- [ ] Pinned versions used
- [ ] Supply chain verified

## Security Testing
- [ ] Unit tests for security paths
- [ ] Integration tests complete
- [ ] Security scanning passed
- [ ] Manual testing performed
```

## Performance & Sustainability

### Monitoring Best Practices

```python
import logging
import metrics

class SkillMonitoring:
    def __init__(self):
        self.logger = logging.getLogger('skill-monitor')
        
    def log_execution(self, skill_name, duration, success):
        """Log skill execution metrics"""
        metrics.histogram(
            'skill.execution.duration_ms',
            duration,
            tags={'skill': skill_name, 'success': success}
        )
        
    def track_security_event(self, event_type, details):
        """Track security-relevant events"""
        self.logger.warning(
            f"Security event: {event_type}",
            extra={'details': details, 'timestamp': datetime.now()}
        )
        metrics.increment(
            'skill.security_events',
            tags={'event_type': event_type}
        )
```

## Building Community Trust

### Transparency Best Practices

1. **Clear Documentation**
   - Document all permissions explicitly
   - Explain why each permission is needed
   - Provide code examples

2. **Regular Updates**
   - Keep dependencies current
   - Apply security patches promptly
   - Publish changelog entries

3. **Community Engagement**
   - Respond to issues quickly
   - Accept security contributions
   - Provide security contact info

4. **Certification Compliance**
   - Pass security audits
   - Maintain OWASP AST10 compliance
   - Display trust badges

---

*Last updated: March 2026*