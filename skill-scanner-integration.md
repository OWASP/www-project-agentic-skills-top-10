---
layout: col-sidebar
title: Skill Scanner Integration
tags: scanner, security-tools, integration
level: 2
type: documentation
pitch: Integrate automated security scanning into your AI agent skill development
description: "Guide for integrating automated security scanning tools into AI agent skill development pipelines and registries."
---

# Skill Scanner Integration

This guide provides instructions for integrating automated security scanning into AI agent skill development and deployment pipelines.

## Overview

Automated skill scanning is essential for detecting security vulnerabilities before skills are published or installed. This page covers integration approaches for different platforms and development workflows.

## Supported Scanning Tools

### AST10-Scanner
The official OWASP AST10 scanner provides comprehensive vulnerability detection:

```bash
# Install AST10 Scanner
npm install -g @owasp/ast10-scanner

# Scan a skill file
ast10-scan skill.yaml --output report.json

# Scan with custom rules
ast10-scan skill.yaml --rules custom-rules.json --severity high
```

#### Features
- AST10 risk pattern detection
- Permission analysis
- Code injection vulnerability scanning
- Supply chain risk assessment
- MAESTRO framework compliance checking

### Platform-Specific Scanners

#### OpenClaw Scanner
```bash
# ClawHub CLI scanning
claw scan skill.md --registry clawhub

# Local development scanning
claw scan --local skill.md --sandbox
```

#### Claude Code Scanner
```bash
# Claude skill validation
claude skill validate skill.json --security

# Pre-deployment scanning
claude skill scan skill.json --comprehensive
```

#### Cursor Scanner
```bash
# Cursor extension scanning
cursor scan manifest.json --security

# Development-time scanning
cursor scan --watch manifest.json
```

#### VS Code Scanner
```bash
# VS Code extension validation
vsce validate extension.vsix --security

# Pre-publish scanning
vsce package --scan-security
```

## Integration Approaches

### CI/CD Pipeline Integration

#### GitHub Actions Example
```yaml
name: Security Scan
on:
  push:
    paths:
      - 'skills/**'
  pull_request:
    paths:
      - 'skills/**'

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install AST10 Scanner
        run: npm install -g @owasp/ast10-scanner

      - name: Scan Skills
        run: |
          find skills -name "*.md" -o -name "*.json" -o -name "*.yaml" | \
          xargs ast10-scan --output security-report.json

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: security-report.json

      - name: Fail on High Severity
        run: |
          if jq '.vulnerabilities[] | select(.severity == "high")' security-report.json | grep -q .; then
            echo "High severity vulnerabilities found!"
            exit 1
          fi
```

#### GitLab CI Example
```yaml
stages:
  - security

security_scan:
  stage: security
  image: node:18
  before_script:
    - npm install -g @owasp/ast10-scanner
  script:
    - find skills -name "*.md" -o -name "*.json" -o -name "*.yaml" | xargs ast10-scan --gitlab-report
  artifacts:
    reports:
      sast: gl-sast-report.json
  only:
    - merge_requests
```

### Pre-commit Hooks

#### Local Development Setup
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: https://github.com/owasp/ast10-scanner
    rev: v1.0.0
    hooks:
      - id: ast10-scan
        files: \.(md|json|yaml)$
        args: [--severity, high]
```

### Registry Integration

#### Automated Registry Scanning
```javascript
// Registry webhook integration
const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

app.post('/webhook/skill-published', async (req, res) => {
  const { skillId, skillUrl } = req.body;

  try {
    // Download skill
    await downloadSkill(skillUrl, `/tmp/${skillId}`);

    // Run security scan
    exec(`ast10-scan /tmp/${skillId} --output /tmp/${skillId}-report.json`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Scan failed: ${error}`);
        // Reject skill or flag for review
        rejectSkill(skillId, 'Security scan failed');
        return;
      }

      // Check results
      const report = JSON.parse(fs.readFileSync(`/tmp/${skillId}-report.json`));
      if (report.vulnerabilities.some(v => v.severity === 'critical')) {
        rejectSkill(skillId, 'Critical vulnerabilities detected');
      } else {
        approveSkill(skillId);
      }
    });

    res.status(200).send('Scan initiated');
  } catch (error) {
    res.status(500).send('Scan failed');
  }
});

app.listen(3000);
```

## Custom Scanner Development

### Basic Scanner Template
```python
import yaml
import json
import re
from typing import List, Dict

class SkillScanner:
    def __init__(self):
        self.vulnerabilities = []

    def scan_skill(self, skill_path: str) -> List[Dict]:
        """Scan a skill file for vulnerabilities"""
        self.vulnerabilities = []

        # Load skill content
        with open(skill_path, 'r') as f:
            if skill_path.endswith('.md'):
                content = f.read()
                self.scan_markdown(content)
            elif skill_path.endswith('.json'):
                data = json.load(f)
                self.scan_json(data)
            elif skill_path.endswith('.yaml') or skill_path.endswith('.yml'):
                data = yaml.safe_load(f)
                self.scan_yaml(data)

        return self.vulnerabilities

    def scan_markdown(self, content: str):
        """Scan markdown skill files"""
        # AST01: Malicious instructions
        if re.search(r'rm -rf|format|del /f', content, re.IGNORECASE):
            self.add_vulnerability('AST01', 'high', 'Potentially destructive commands detected')

        # AST03: Over-privileged
        if 'sudo' in content or 'admin' in content.lower():
            self.add_vulnerability('AST03', 'medium', 'Privilege escalation patterns detected')

        # AST05: Input validation
        if 'eval(' in content or 'exec(' in content:
            self.add_vulnerability('AST05', 'high', 'Code injection vulnerabilities detected')

    def scan_json(self, data: Dict):
        """Scan JSON skill files"""
        # Check permissions
        if 'permissions' in data:
            perms = data['permissions']
            if isinstance(perms, list) and 'full_access' in perms:
                self.add_vulnerability('AST03', 'high', 'Excessive permissions requested')

    def scan_yaml(self, data: Dict):
        """Scan YAML skill files"""
        # Similar checks as JSON
        pass

    def add_vulnerability(self, ast_id: str, severity: str, description: str):
        """Add a vulnerability finding"""
        self.vulnerabilities.append({
            'id': ast_id,
            'severity': severity,
            'description': description,
            'timestamp': datetime.now().isoformat()
        })

# Usage
scanner = SkillScanner()
results = scanner.scan_skill('skill.md')
print(json.dumps(results, indent=2))
```

## Scanner Output Formats

### JSON Report Format
```json
{
  "scan_metadata": {
    "scanner_version": "1.0.0",
    "scan_timestamp": "2026-03-22T10:00:00Z",
    "skill_path": "skill.md"
  },
  "vulnerabilities": [
    {
      "id": "AST01",
      "severity": "high",
      "description": "Malicious command patterns detected",
      "line_number": 15,
      "code_snippet": "rm -rf /",
      "recommendation": "Remove destructive commands"
    }
  ],
  "summary": {
    "total_vulnerabilities": 1,
    "critical": 0,
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
```

### SARIF Format (for CI/CD)
```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "AST10 Scanner",
          "version": "1.0.0"
        }
      },
      "results": [
        {
          "ruleId": "AST01",
          "level": "error",
          "message": {
            "text": "Malicious skills detected"
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "skill.md"
                },
                "region": {
                  "startLine": 15
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

## Best Practices

### Scanner Implementation
1. **False Positive Management**: Implement confidence scoring
2. **Performance Optimization**: Use efficient parsing and pattern matching
3. **Regular Updates**: Keep vulnerability signatures current
4. **Comprehensive Coverage**: Scan all skill formats and platforms

### Integration Guidelines
1. **Non-blocking Scans**: Don't break development workflows
2. **Clear Reporting**: Provide actionable remediation guidance
3. **Version Control**: Track scanner versions and rule updates
4. **Community Contribution**: Allow custom rule submissions

### Security Considerations
1. **Safe Execution**: Run scanners in isolated environments
2. **Data Protection**: Handle skill content securely
3. **Access Control**: Limit scanner access to necessary systems
4. **Audit Logging**: Log all scan activities

## Available Tools and Resources

- **AST10 Scanner**: [GitHub Repository](https://github.com/OWASP/ast10-scanner)
- **ClawHub Security Tools**: [Documentation](https://clawhub.dev/security)
- **VS Code Security Linting**: [Marketplace](https://marketplace.visualstudio.com)

## Contributing

To contribute new scanning rules or improve existing scanners:

1. Fork the AST10 Scanner repository
2. Add your rule or improvement
3. Submit a pull request with test cases
4. Ensure backward compatibility

---

*Regular updates to scanning tools and integration guides. Last updated: March 2026*</content>
<parameter name="filePath">c:\Users\kenhu\www-project-agentic-skills-top-10\skill-scanner-integration.md