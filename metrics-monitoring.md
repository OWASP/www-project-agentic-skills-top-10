---
layout: col-sidebar
title: Security Metrics & Monitoring
tags: metrics, monitoring, observability, analytics
level: 2
type: documentation
pitch: Monitor and measure AI agent skill security posture
description: "Framework for monitoring security metrics, tracking trends, and measuring effectiveness of security controls for AI agent skills."
---

# Security Metrics & Monitoring Framework

This guide provides a comprehensive framework for monitoring, measuring, and improving AI agent skill security through data-driven metrics and analytics.

## Key Performance Indicators (KPIs)

### Security Metrics

#### 1. Vulnerability Management
```
Metric: Critical Vulnerabilities Fixed / Total
Target: 100% within 30 days
Tracking: Weekly

CVE Management:
- Published CVEs in skills: [current]
- Fixed this month: [count]
- Pending fixes: [count]
- Average fix time: [days]
```

#### 2. Malware Detection Rate
```
Metric: Malicious Skills Detected / Total Skills Published
Target: >95% detection within 30 days of publication
Tracking: Weekly

Samples:
- Total skills scanned: [count]
- Malicious detected: [count]
- False positives: [count]
- Detection accuracy: [percentage]%
```

#### 3. Security Incident Response
```
Metric: Mean Time to Respond (MTTR)
Target: <4 hours for HIGH severity
Tracking: Per incident

Response Times:
- CRITICAL: <1 hour (current avg: X min)
- HIGH: <4 hours (current avg: X min)
- MEDIUM: <1 day (current avg: X hours)
- LOW: <1 week (current avg: X days)
```

#### 4. Publisher Compliance
```
Metric: Compliant Publishers / Total Active Publishers
Target: >90%
Tracking: Monthly

Compliance Breakdown:
- Signed skills: [percentage]%
- Recent security review: [percentage]%
- Updated documentation: [percentage]%
- No vulnerabilities: [percentage]%
```

#### 5. User Security Awareness
```
Metric: Users Who Reviewed Permissions / Total Installers
Target: >70%
Tracking: Quarterly

Survey Data:
- Users reviewing permissions: [percentage]%
- Users verifying publisher: [percentage]%
- Users updating skills: [percentage]%
```

---

## Dashboard Metrics

### Executive Dashboard
**For**: Leadership, Board, Security Committee

```
┌─────────────────────────────────────────┐
│ AST10 Security Status - Executive View  │
├─────────────────────────────────────────┤
│                                         │
│ Overall Security Score: 7.8/10         │
│ ████████░░ 78%                          │
│                                         │
│ Key Metrics:                            │
│  • Active Threats: 3 (MEDIUM)          │
│  • Avg Incident Response: 2.2 hrs      │
│  • Publisher Compliance: 87%           │
│  • Skills with Issues: 0.3%            │
│                                         │
│ Trend (30-day): ↑ Improving            │
│                                         │
│ Action Items: 2                         │
│  1. Update 5 outdated policies         │
│  2. Complete Q2 security audit         │
│                                         │
└─────────────────────────────────────────┘
```

### Operations Dashboard
**For**: Security Operations, Platform Teams

```
┌──────────────────────────────────────────────┐
│ AST10 Operations - Real-Time Monitoring     │
├──────────────────────────────────────────────┤
│                                              │
│ Skills Published (24h): 127                 │
│ ├─ Scanned: 127 (100%)                     │
│ ├─ Passed: 121 (95%)                       │
│ └─ Flagged: 6 (5%)                         │
│                                              │
│ Active Incidents:                            │
│ ├─ CRITICAL: 0                              │
│ ├─ HIGH: 1 (Incident INC-2026-0042)        │
│ ├─ MEDIUM: 3                                │
│ └─ LOW: 8                                   │
│                                              │
│ Scanning Performance:                        │
│ ├─ Avg Scan Time: 2.3 sec                   │
│ ├─ Malware Detection Rate: 96.2%           │
│ └─ False Positive Rate: 0.8%               │
│                                              │
│ Platform Health:                             │
│ ├─ OpenClaw: ✓ Healthy                     │
│ ├─ Claude Code: ⚠ 2 alerts                 │
│ ├─ Cursor: ✓ Healthy                       │
│ └─ VS Code: ✓ Healthy                      │
│                                              │
└──────────────────────────────────────────────┘
```

### Developer Dashboard
**For**: Skill Developers, Security Team

```
┌────────────────────────────────────────┐
│ My Skill Security Status                │
├────────────────────────────────────────┤
│                                        │
│ Published Skills: 12                   │
│ ├─ All Compliant: 10                  │
│ ├─ Minor Issues: 2                    │
│ └─ Critical Issues: 0                 │
│                                        │
│ Latest Scans:                          │
│ ├─ 2026-03-22 10:15: PASS ✓           │
│ ├─ 2026-03-21 14:30: PASS ✓           │
│ ├─ 2026-03-20 09:00: WARN (2 issues)  │
│ └─ 2026-03-19 16:45: PASS ✓           │
│                                        │
│ Security Training Status:              │
│ ├─ Completed Courses: 3/5             │
│ ├─ Certification: AST10-SE Analyst    │
│ └─ Expires: 2027-03-22                │
│                                        │
│ Recommendations:                       │
│ 1. Update deprecated library in skill  │
│ 2. Review and adjust permissions      │
│                                        │
└────────────────────────────────────────┘
```

---

## Monitoring Infrastructure

### Collection Points

```
┌─ Skill Registry ────────────────────────┐
│ Events:                                  │
│ • Skill published                       │
│ • Skill updated                         │
│ • Skill removed                         │
│ • Download count                        │
│ • User reports                          │
└────────────────────────────────────────┘
       │
       ↓
┌─ Security Scanners ─────────────────────┐
│ AST10-Scanner findings:                 │
│ • Vulnerability detections              │
│ • Malware classifications              │
│ • Permission analysis                  │
│ • Supply chain assessment              │
└────────────────────────────────────────┘
       │
       ↓
┌─ Runtime Monitoring ────────────────────┐
│ Agent execution tracking:               │
│ • Skill invocations                     │
│ • Permission usage                      │
│ • Network activity                      │
│ • File system access                    │
│ • Performance metrics                   │
└────────────────────────────────────────┘
       │
       ↓
┌─ Analytics Platform ────────────────────┐
│ Aggregation & Analysis:                 │
│ • Trend analysis                        │
│ • Anomaly detection                     │
│ • Risk scoring                          │
│ • Correlation analysis                  │
└────────────────────────────────────────┘
       │
       ↓
┌─ Visualization & Alerting ──────────────┐
│ Dashboards & Notifications:             │
│ • Real-time dashboards                  │
│ • Automated alerts                      │
│ • Reports & trends                      │
│ • Escalation workflows                  │
└────────────────────────────────────────┘
```

### Data Collection
```python
import metrics

class SkillMetricsCollector:
    def __init__(self):
        self.metrics = metrics.MetricsClient()
    
    def record_skill_event(self, event_type, skill_id, metadata):
        """Record skill lifecycle events"""
        self.metrics.increment(
            'skill.events',
            tags={'type': event_type, 'skill_id': skill_id}
        )
        self.metrics.gauge(
            'skill.downloads',
            metadata.get('download_count'),
            tags={'skill_id': skill_id}
        )
    
    def record_scan_result(self, scan_result):
        """Record security scan results"""
        self.metrics.increment(
            'scans.total',
            tags={'status': scan_result.status}
        )
        self.metrics.histogram(
            'scans.duration_ms',
            scan_result.duration_ms
        )
        
        for finding in scan_result.findings:
            self.metrics.increment(
                'findings',
                tags={'severity': finding.severity}
            )
    
    def record_incident(self, incident):
        """Record security incidents"""
        self.metrics.increment(
            'incidents',
            tags={'severity': incident.severity}
        )
        self.metrics.histogram(
            'incident.response_time_minutes',
            incident.response_time
        )
```

---

## Alerting Rules

### Critical Alerts
```
Alert: MaliciousSkillDetected
Condition: Malware confidence > 90%
Action: 
  - CRITICAL incident created
  - Skill immediately flagged
  - Security team paged
  - Incident response activated
```

### High Severity Alerts
```
Alert: UnexpectedPermissions
Condition: Skill requests unusual permission combination
Action:
  - HIGH incident created
  - Manual review queued
  - Publisher notified
  - Enhanced monitoring enabled
```

### Medium Severity Alerts
```
Alert: VulnerabilityFound
Condition: CVE published affecting skill dependency
Action:
  - MEDIUM incident created
  - Affected publishers notified
  - Patch available communication sent
  - Tracking enabled
```

### Low Severity Alerts
```
Alert: ComplianceGap
Condition: Publisher documentation outdated (>90 days)
Action:
  - LOW priority ticket created
  - Publisher sent reminder email
  - Tracking enabled
```

---

## Trend Analysis

### Quarterly Report Example
```
Q1 2026 Security Report
========================

Executive Summary:
- 1,247 new skills published
- 12 malicious skills detected (0.96%)
- 23 security incidents resolved
- 87% publisher compliance

Trend Analysis:
- Malware Detection: ↑ 15% (improved detection)
- Response Time: ↓ 25% (faster response)
- Publisher Compliance: ↑ 5% (better education)
- User Awareness: ↑ 12% (more training)

Key Findings:
1. Supply chain attacks increasing (trend analysis)
2. Permission escalation most common vulnerability
3. Platform A has 3x more issues than B
4. Certain publisher type has 5x incident rate

Recommendations:
1. Increase supply chain scanning
2. Add permission validation warnings
3. Platform A needs hardening
4. New publisher education program
```

---

## Anomaly Detection

### Machine Learning Models
```
Model 1: Skill Behavior Analysis
- Detects unusual permission patterns
- Identifies obfuscation techniques
- Flags suspicious code structures
- Accuracy: 94.2%

Model 2: Publisher Assessment  
- Analyzes publisher history
- Detects risky publisher patterns
- Predicts future incidents
- Accuracy: 87.6%

Model 3: Network Traffic Analysis
- Detects unusual outbound connections
- Identifies data exfiltration
- Flags C2 communication
- Accuracy: 96.1%
```

### Alert Confidence Scoring
```
Score: 0-100 (higher = more confidence)

85-100: CRITICAL - Immediate action
70-84:  HIGH - Urgent investigation  
50-69:  MEDIUM - Schedule review
25-49:  LOW - Monitor
0-24:   INFO - Log only

Examples:
- Skill connects to known C2: 98/100 → CRITICAL
- Suspicious permission combo: 62/100 → MEDIUM
- Rare library usage: 35/100 → LOW
```

---

## Reporting

### Automated Reports

#### Daily Security Summary
```
Date: 2026-03-22
Skills Published: 127
Security Scans: 127 (100%)
Passed: 121 (95.3%)
Issues Found: 6 (4.7%)
Malware Detected: 0 (0%)
Incidents Opened: 2
Incidents Closed: 1
```

#### Weekly Trends
```
New Malicious Skills: 3 (↓ 40% from previous week)
Publisher Violations: 5 (↑ 25%)
User Complaints: 12 (↓ 15%)
Security Training: 34 enrolled (↑ 5%)
```

#### Monthly Report
- 30-day trends
- Emerging threats
- Successful mitigations
- Performance metrics
- Recommendations

---

## Continuous Improvement

### Metrics Review Cycle
```
Weekly:
  - Alert review  
  - Incident metrics
  - Detection rates

Monthly:
  - Dashboard review
  - Trend analysis
  - Alert tuning

Quarterly:
  - Full metric assessment
  - Model retraining
  - Strategy adjustment

Annually:
  - Goals review
  - Program evaluation
  - Long-term trends
```

### Benchmarking
```
Industry Benchmarks (2026):
- Malware detection rate: 85-95%
- Incident response time: 2-6 hours
- Publisher compliance: 70-85%
- False positive rate: 1-3%

Our Performance:
- Detection rate: 96.2% ✓
- Response time: 2.1 hours ✓
- Compliance: 87% ✓
- False positives: 0.8% ✓

Status: Above industry average
```

---

## Tools & Platforms

### Recommended Stacks
```
Collection:
- Prometheus (metrics)
- Elasticsearch (logs)
- Jaeger (tracing)

Analysis:
- Splunk / ELK
- Grafana
- Datadog

Alerting:
- PagerDuty
- Opsgenie
- Slack

Visualization:
- Grafana
- Kibana
- Splunk
```

---

*Metrics framework updated: March 2026. Review quarterly with leadership.*