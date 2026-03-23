---
layout: col-sidebar
title: API Documentation
tags: api, documentation, integration
level: 2
type: documentation
pitch: Programmatic access to OWASP AST10 data and tools
description: "RESTful API documentation for accessing OWASP AST10 security data, risk assessments, and integration tools."
---

# OWASP AST10 API Documentation

The OWASP AST10 API provides programmatic access to security data, risk assessment tools, and integration capabilities for AI agent skill security.

## Base URL
```
https://api.owasp.org/ast10/v1
```

## Authentication

All API requests require authentication using API keys. Get your API key from the [OWASP AST10 Dashboard](https://owasp.org/ast10/dashboard).

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.owasp.org/ast10/v1/risks
```

## Endpoints

### Risk Data

#### GET /risks
Retrieve all AST10 security risks.

**Response:**
```json
{
  "data": [
    {
      "id": "AST01",
      "title": "Malicious Skills",
      "severity": "Critical",
      "description": "Attackers publish skills that appear legitimate but contain hidden malicious payloads...",
      "platforms": ["All"],
      "maestro_mapping": {
        "layer_7": "Agent Ecosystem",
        "layer_3": "Agent Frameworks"
      },
      "mitigations": [
        "Require cryptographic signatures",
        "Implement Merkle root signing",
        "Isolate skill execution"
      ]
    }
  ],
  "meta": {
    "total": 10,
    "version": "1.0"
  }
}
```

#### GET /risks/{id}
Get detailed information about a specific risk.

**Parameters:**
- `id`: Risk ID (AST01-AST10)

**Response:**
```json
{
  "data": {
    "id": "AST01",
    "title": "Malicious Skills",
    "severity": "Critical",
    "description": "...",
    "attack_scenarios": [
      {
        "name": "Typosquatting",
        "description": "...",
        "indicators": ["..."],
        "mitigation": "..."
      }
    ],
    "code_examples": {
      "signature_verification": "...",
      "behavioral_sandboxing": "..."
    },
    "references": [
      "Snyk ToxicSkills",
      "Check Point Research"
    ]
  }
}
```

### Threat Intelligence

#### GET /threats
Get current threat intelligence data.

**Query Parameters:**
- `since`: ISO 8601 timestamp for filtering recent threats
- `severity`: Filter by severity (low, medium, high, critical)
- `platform`: Filter by platform

**Response:**
```json
{
  "data": [
    {
      "id": "THREAT-2026-001",
      "title": "ClawHavoc Campaign",
      "severity": "high",
      "description": "Coordinated attack on AI agent skill registries",
      "platforms_affected": ["OpenClaw", "Claude Code"],
      "indicators": [
        {
          "type": "domain",
          "value": "clawhavoc.net",
          "confidence": 0.95
        }
      ],
      "first_seen": "2026-01-03T00:00:00Z",
      "last_seen": "2026-01-28T00:00:00Z",
      "mitigation_status": "contained"
    }
  ],
  "meta": {
    "total": 15,
    "updated": "2026-03-22T12:00:00Z"
  }
}
```

#### GET /threats/stats
Get threat statistics and trends.

**Response:**
```json
{
  "data": {
    "total_threats": 47,
    "active_campaigns": 3,
    "platform_distribution": {
      "OpenClaw": 18,
      "Claude Code": 15,
      "Cursor": 8,
      "VS Code": 6
    },
    "severity_breakdown": {
      "critical": 5,
      "high": 12,
      "medium": 20,
      "low": 10
    },
    "trends": {
      "last_30_days": 23,
      "last_7_days": 8
    }
  }
}
```

### Risk Assessment

#### POST /assess
Perform automated risk assessment on a skill.

**Request Body:**
```json
{
  "skill_content": "YAML or JSON skill definition",
  "skill_format": "yaml|json|markdown",
  "platform": "OpenClaw|Claude Code|Cursor|VS Code",
  "options": {
    "include_recommendations": true,
    "severity_threshold": "medium"
  }
}
```

**Response:**
```json
{
  "data": {
    "overall_risk_score": 65.5,
    "risk_level": "medium",
    "vulnerabilities": [
      {
        "id": "AST01",
        "severity": "high",
        "description": "Potential malicious code patterns detected",
        "line_number": 15,
        "recommendation": "Review and remove suspicious commands"
      },
      {
        "id": "AST03",
        "severity": "medium",
        "description": "Excessive permissions requested",
        "recommendation": "Minimize required permissions"
      }
    ],
    "mitigation_plan": [
      "Implement input validation",
      "Reduce skill permissions",
      "Add security scanning to CI/CD"
    ]
  },
  "processing_time_ms": 245
}
```

#### GET /assess/history
Get assessment history for your organization.

**Query Parameters:**
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset
- `status`: Filter by assessment status

### Scanner Integration

#### POST /scan
Submit a skill for comprehensive security scanning.

**Request Body:**
```json
{
  "skill_url": "https://example.com/skill.yaml",
  "callback_url": "https://your-app.com/webhook/scan-complete",
  "scan_options": {
    "rules": ["AST01", "AST03", "AST05"],
    "timeout": 300,
    "sandbox": true
  }
}
```

**Response:**
```json
{
  "data": {
    "scan_id": "scan_1234567890",
    "status": "queued",
    "estimated_completion": "2026-03-22T12:05:00Z",
    "scan_url": "https://api.owasp.org/ast10/v1/scans/scan_1234567890"
  }
}
```

#### GET /scans/{scan_id}
Get scan results.

**Response:**
```json
{
  "data": {
    "scan_id": "scan_1234567890",
    "status": "completed",
    "started_at": "2026-03-22T12:00:00Z",
    "completed_at": "2026-03-22T12:02:15Z",
    "results": {
      "vulnerabilities_found": 2,
      "critical": 0,
      "high": 1,
      "medium": 1,
      "low": 0,
      "details": [...]
    },
    "report_url": "https://api.owasp.org/ast10/v1/scans/scan_1234567890/report"
  }
}
```

### Webhooks

#### Scan Completion Webhook
When a scan completes, we'll POST to your callback URL:

```json
{
  "event": "scan.completed",
  "scan_id": "scan_1234567890",
  "status": "completed",
  "results_summary": {
    "vulnerabilities_found": 2,
    "highest_severity": "high"
  },
  "report_url": "https://api.owasp.org/ast10/v1/scans/scan_1234567890/report"
}
```

### Rate Limits

- **Free Tier**: 100 requests/hour, 1,000/month
- **Professional**: 1,000 requests/hour, 100,000/month
- **Enterprise**: Unlimited (contact sales)

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

### Error Handling

All errors follow this format:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request body is invalid",
    "details": {
      "field": "skill_content",
      "issue": "cannot be empty"
    }
  }
}
```

Common error codes:
- `INVALID_REQUEST`: Malformed request
- `UNAUTHORIZED`: Invalid or missing API key
- `RATE_LIMITED`: Rate limit exceeded
- `NOT_FOUND`: Resource not found
- `INTERNAL_ERROR`: Server error

### SDKs and Libraries

#### JavaScript/Node.js
```javascript
const { AST10Client } = require('@owasp/ast10-sdk');

const client = new AST10Client({
  apiKey: 'your-api-key'
});

// Assess a skill
const assessment = await client.assessSkill(skillContent);
console.log(`Risk score: ${assessment.overall_risk_score}`);

// Get threat intelligence
const threats = await client.getThreats({ severity: 'high' });
```

#### Python
```python
from ast10_sdk import AST10Client

client = AST10Client(api_key='your-api-key')

# Assess skill
assessment = client.assess_skill(skill_content)
print(f"Risk score: {assessment['overall_risk_score']}")

# Get risks
risks = client.get_risks()
```

#### Go
```go
package main

import (
    "github.com/owasp/ast10-sdk-go"
)

func main() {
    client := ast10.NewClient("your-api-key")
    
    assessment, err := client.AssessSkill(skillContent)
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("Risk score: %.1f\n", assessment.OverallRiskScore)
}
```

### Changelog

#### v1.1.0 (March 2026)
- Added threat intelligence endpoints
- Enhanced risk assessment with ML-based scoring
- Added webhook support for scan completion

#### v1.0.0 (January 2026)
- Initial release with core AST10 endpoints
- Basic risk assessment and scanning
- Rate limiting and authentication

### Support

- **Documentation**: [Full API Reference](https://api.owasp.org/ast10/docs)
- **Community Forum**: [OWASP AST10 Discussions](https://github.com/OWASP/www-project-agentic-skills-top-10/discussions)
- **Issue Tracking**: [GitHub Issues](https://github.com/OWASP/www-project-agentic-skills-top-10/issues)
- **Email Support**: api-support@owasp.org

---

*API documentation is versioned. Current version: v1.1.0. Last updated: March 2026*</content>
<parameter name="filePath">c:\Users\kenhu\www-project-agentic-skills-top-10\api-documentation.md