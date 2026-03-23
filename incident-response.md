---
layout: col-sidebar
title: Incident Response Playbook
tags: incident-response, playbooks, operations
level: 2
type: documentation
pitch: Respond to AI agent skill security incidents effectively
description: "Detailed playbooks for responding to malicious skill incidents, including detection, containment, investigation, and recovery procedures."
---

# Incident Response Playbook

This guide provides step-by-step procedures for responding to AI agent skill security incidents, from initial detection through full recovery.

## Incident Types & Severity Levels

### Severity Classification

**CRITICAL (Red)**
- Active exploitation in production
- Mass deployment of malicious skills
- Data exfiltration confirmed
- System compromise in progress
- **Response time**: 1 hour

**HIGH (Orange)**
- Confirmed malicious skill found
- Potential widespread exposure
- Vulnerability affecting many users
- Active campaign detected
- **Response time**: 4 hours

**MEDIUM (Yellow)**
- Suspicious skill behavior detected
- Potential vulnerability identified
- Limited user impact
- Investigation needed
- **Response time**: 1 business day

**LOW (Blue)**
- Minor security finding
- No immediate risk
- Policy violation
- Documentation issue
- **Response time**: 1 week

---

## Incident Response Workflow

```
Detect
  ↓
Analyze & Classify
  ↓
Notify Stakeholders
  ↓
Contain & Mitigate
  ↓
Investigate
  ↓
Remediate
  ↓
Communicate
  ↓
Post-Incident Review
```

---

## Playbook 1: Malicious Skill Discovery

### Scenario
A malicious skill has been discovered in a registry.

### Detection Indicators
- ✓ Automated scanner flags on installation
- ✓ User reports suspicious behavior
- ✓ Manual security review finds issues
- ✓ Threat intelligence indicates compromise
- ✓ Unusual network activity detected

### Step 1: Initial Response (Immediate - 15 minutes)

#### 1.1 Confirm Detection
```bash
# Verify skill details
skill_id="suspicious-skill-123"
platform="openclap"

# Pull skill metadata
curl -s https://api.${platform}.dev/skills/${skill_id} | jq .

# Check download statistics
curl -s https://api.${platform}.dev/skills/${skill_id}/stats | jq .

# Review recent reviews/reports
curl -s https://api.${platform}.dev/skills/${skill_id}/reports | jq .
```

#### 1.2 Create Incident Ticket
```yaml
Incident: Malicious Skill Discovery
ID: INC-2026-0001
Severity: HIGH
Skill ID: suspicious-skill-123
Platform: OpenClaw
Discovered: 2026-03-22T10:30:00Z
Reported By: Security Team
Status: OPEN
```

#### 1.3 Assemble Response Team
- [ ] Security Engineer (Lead)
- [ ] Platform Administrator
- [ ] Threat Intelligence Analyst
- [ ] Communications Officer
- [ ] Legal/Compliance (if needed)

### Step 2: Analysis & Classification (30 minutes)

#### 2.1 Analyze Skill Content
```python
# Automated analysis
from ast10_scanner import SkillAnalyzer

analyzer = SkillAnalyzer()

skill_content = download_skill('suspicious-skill-123')
analysis = analyzer.comprehensive_scan(skill_content)

# Check findings
for finding in analysis.vulnerabilities:
    if finding.severity == 'critical':
        print(f"CRITICAL: {finding.description}")
        print(f"Evidence: {finding.evidence}")
```

#### 2.2 Determine Maliciousness
**Indicators of Compromise**:
- [ ] Obfuscated or encoded payloads
- [ ] Unauthorized data exfiltration attempts
- [ ] Command injection patterns
- [ ] Credential harvesting code
- [ ] Communication to known C2 servers
- [ ] Process modification/persistence
- [ ] Lateral movement attempts

#### 2.3 Classify Incident
```
Type: MALWARE
Subtype: Information Stealer
TTPs: Credential Harvesting, Data Exfiltration
Severity: CRITICAL
Estimated Impact: 12,400+ installations
```

### Step 3: Notification & Escalation (30 minutes)

#### 3.1 Notify Internal Teams
```
TO: Security Operations Center
CC: Executive Team, Legal
PRIORITY: CRITICAL

Subject: CRITICAL - Malicious Skill Found: [skill-id]

Details:
- Skill ID: suspicious-skill-123
- Downloads: 12,400+
- Type: Information Stealer
- Confidence: 95%
- Status: Under Investigation

Actions Initiated:
- Skill flagged for removal
- Platform notifications queued
- Incident response activated
```

#### 3.2 Notify Platform Operators
```
Affected Platforms: OpenClaw, Claude Code
Urgency: IMMEDIATE ACTION REQUIRED

The following skill has been identified as malicious:
- ID: suspicious-skill-123
- Classification: Critical Malware
- Estimated Impact: 12,400+ affected users
- Recommended Action: Immediate removal

We request:
1. Immediate skill removal from registry
2. User notifications
3. Download halt
4. User support coordination
```

### Step 4: Containment & Mitigation (1 hour)

#### 4.1 Remove Malicious Skill
```bash
# Platform-specific removal
# OpenClaw
claw skill remove suspicious-skill-123 --force --reason "CRITICAL: Malware discovered"

# Claude Code
claude skill remove suspicious-skill-123 --emergency

# Cursor
cursor skill revoke suspicious-skill-123 --immediate

# VS Code
vsce withdraw suspicious-skill-123 --force
```

#### 4.2 Issue User Alerts
**Alert Template**:
```
SECURITY ALERT: Malicious Skill Detected

A skill you may have installed has been identified as malicious:

Skill Name: [name]
Skill ID: suspicious-skill-123
Download Date: [optional]
Risk: HIGH

Actions You Should Take:
1. Uninstall the skill immediately
2. Reset any API keys or credentials
3. Check your data for unauthorized access
4. Report if you've noticed suspicious activity

Steps to Uninstall:
[Platform-specific instructions]

Questions? Contact: security@platform.dev
```

#### 4.3 Block Installation
```
Quarantine Rule:
- Skill ID: suspicious-skill-123
- Reason: Malware detection
- Scan Result: 95% confidence malicious
- Action: Block installation
- Duration: Permanent until reviewed
```

### Step 5: Investigation (2-4 hours)

#### 5.1 Detailed Analysis
```bash
# Extract skill components
unzip skill-archive.zip -d /tmp/skill-analysis

# Static analysis
ast10-scan /tmp/skill-analysis --detailed

# Check for obfuscation
entropy-check /tmp/skill-analysis
string-analysis /tmp/skill-analysis

# Network analysis
grep -r "http\|dns\|socket" /tmp/skill-analysis
```

#### 5.2 Build Indicators of Compromise
```json
{
  "iocs": [
    {
      "type": "domain",
      "value": "malicious.example.com",
      "confidence": "high"
    },
    {
      "type": "ip_address",
      "value": "192.0.2.1",
      "confidence": "high"
    },
    {
      "type": "file_hash",
      "value": "abc123def456...",
      "confidence": "very_high"
    }
  ]
}
```

#### 5.3 Determine Scope & Timeline
```
Timeline:
- 2026-01-15: Skill created
- 2026-01-20: First downloads (23 users)
- 2026-02-10: Downloaded 1,200 times
- 2026-03-01: Peak downloads (8,400 total)
- 2026-03-22: Malicious behavior reported

Affected Users: ~12,400
Geographical Distribution: Global
Platforms: OpenClaw (primary), Claude Code (secondary)
```

### Step 6: Remediation (1-3 days)

#### 6.1 User Support
```
Support Actions:
- [ ] Create FAQ page
- [ ] Set up dedicated support phone line
- [ ] Email affected users with remediation steps
- [ ] Provide credential reset assistance
- [ ] Monitor for follow-up incidents

Resources:
- Credential reset guide: [link]
- FAQ: [link]
- Emergency support: 1-800-SECURITY
```

#### 6.2 System Cleanup
For affected users:
```bash
# Step 1: Stop all agents
systemctl stop agent-service

# Step 2: Remove malicious skill
rm -rf ~/.agent/skills/suspicious-skill-123

# Step 3: Clear caches
rm -rf ~/.agent/cache/*

# Step 4: Reset credentials
generate-new-api-keys

# Step 5: Restart agents
systemctl start agent-service

# Step 6: Verify clean state
agent-security-check
```

#### 6.3 Infrastructure Hardening
```
Post-Incident Hardening:
- [ ] Increase automated scanning sensitivity
- [ ] Add skill behavior monitoring
- [ ] Implement stricter code review
- [ ] Deploy behavioral analysis
- [ ] Add user activity monitoring
- [ ] Implement 2FA for publisher accounts
```

### Step 7: Communication (Ongoing)

#### 7.1 Public Statement (Template)
```markdown
# Security Incident: Malicious Skill Removal

## What Happened
On March 22, 2026, our security team identified a malicious skill
in the OpenClaw registry designed to steal user credentials.

## Impact
- 12,400 installations
- 0 confirmed credential thefts detected
- All affected installations removed

## Actions Taken
- Immediately removed skill from all registries
- Notified all users
- Enhanced detection systems
- Provided remediation guidance

## What You Should Do
1. Check if you installed "suspicious-skill-123"
2. Uninstall if present
3. Reset credentials as precaution
4. Keep software updated

## Timeline
[Detailed timeline of discovery and response]

## Questions?
Contact: security@platform.dev
```

#### 7.2 Status Updates
- Hour 1: Initial notification
- Hour 4: Removal complete notification
- Day 1: Detailed incident report
- Week 1: Post-incident review complete
- Month 1: Preventive measures deployed

### Step 8: Post-Incident Review (1 week)

#### 8.1 Blameless Postmortem
```markdown
# Incident Postmortem: Malicious Skill INC-2026-0001

## Timeline
[Detailed timeline with all actions]

## Detection Analysis
- How did we detect it?
- Could we have detected earlier?
- What were the warning signs?

## Response Analysis
- What worked well?
- What could be improved?
- Was communication effective?

## Root Cause
[Understanding of how malicious skill was published]

## Preventive Actions
1. [Action to prevent recurrence]
2. [Action to detect faster]
3. [Action to contain better]

## Lessons Learned
[Key insights from incident]
```

#### 8.2 Process Improvements
```
Improvements Implemented:
- [ ] Automated behavioral analysis for all skills
- [ ] Real-time threat intelligence integration
- [ ] Enhanced code review procedures
- [ ] Publisher account security hardening
- [ ] User notification automation
- [ ] Faster skill removal workflows
```

---

## Playbook 2: Data Breach via Skill

### Scenario
A skill has been used to exfiltrate sensitive user data.

### Response Priorities
1. **Immediate** (15 min): Stop data flow, notify affected users
2. **Urgent** (1 hour): Contain scope, preserve evidence
3. **Short-term** (1 day): Notify authorities, support users
4. **Medium-term** (1 week): Full investigation, remediation
5. **Long-term** (1 month): Prevention, lessons learned

### Critical Actions
```bash
# 1. Stop exfiltration
firewall-rule --block destination=attacker-ip --priority=critical

# 2. Isolate affected systems
agent shutdown --affected-users=[list]

# 3. Preserve logs
backup-logs --critical-only /data/incidents/inc-2026-0001

# 4. Revoke compromised credentials
revoke-credentials --all-affected-users

# 5. Notify users
send-incident-notification --template=data_breach --recipients=[list]
```

### Regulatory Compliance
- [ ] Notify regulators within required timeframe (typically 72 hours)
- [ ] Consult legal team
- [ ] Prepare regulatory notifications
- [ ] Document all steps for audit

---

## Playbook 3: Supply Chain Attack Detection

### Scenario
Compromised dependencies could propagate malware.

### Detection Process
```
1. Scan dependency tree
2. Check each dependency's integrity
3. Verify signatures
4. Check for known vulnerabilities
5. Analyze behavioral changes
```

### Response
```
1. Isolate affected versions
2. Notify dependent skills
3. Provide patched versions
4. Update threat intelligence
5. Communicate to users
```

---

## Escalation Contacts

### Internal Escalation
- Level 1: Security Team Lead
- Level 2: CISO
- Level 3: Executive Team / Board

### External Notification
- Platforms: security@platform.dev
- Media: press@owasp.org
- Users: support@platform.dev

### Incident Support
- 24/7 Incident Hotline: [Number]
- Email: incidents@owasp.org
- Chat: #incidents on Slack

---

## Resources & Templates

- [Incident Report Template](incident-template.md)
- [User Notification Template](user-notification.md)
- [Public Statement Template](public-statement.md)
- [Remediation Guide](remediation-guide.md)

---

*Playbooks updated: March 2026. Review quarterly and after each major incident.*