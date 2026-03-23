---
layout: col-sidebar
title: Training & Certification Program
tags: training, certification, education
level: 2
type: documentation
pitch: Learn AI agent skill security with structured training courses
description: "Structured training modules and certification pathways for AI agent skill security professionals, from beginner to expert levels."
---

# AST10 Training & Certification Program

This program provides structured learning paths for understanding and securing AI agent skills, from beginner to expert levels.

## Course Catalog

### Level 1: Fundamentals (2-3 hours)

#### 1.1 Introduction to AI Agent Skills
**Target Audience**: Security practitioners, AI developers

**Learning Objectives**:
- What are AI agent skills and why they matter
- Current threat landscape (2026 statistics)
- Real-world incident examples
- Business impact of skill security

**Topics**:
- Agent architecture and skill execution layer
- Platform overview (OpenClaw, Claude Code, Cursor, VS Code)
- AST10 framework introduction
- Case studies: ClawHavoc, ToxicSkills research

**Assessment**:
- 10-question quiz (70% passing)
- Discuss one case study

**Estimated Time**: 45 minutes
**Format**: Video + interactive content

---

#### 1.2 Understanding the 10 Risks
**Target Audience**: All security roles

**Learning Objectives**:
- Understand each of the 10 AST risks
- Recognize real-world examples
- Identify risk severity
- Understand business context

**Topics Breakdown**:

| Risk | Key Concept | Example |
|------|------------|---------|
| AST01 | Malicious Skills | ClawHavoc campaign |
| AST02 | Supply Chain | Compromised dependencies |
| AST03 | Over-Privileged | Unnecessary filesystem access |
| AST04 | Insecure Metadata | Brand impersonation |
| AST05 | Insufficient Input Validation | Command injection |
| AST06 | Improper Error Handling | Info disclosure |
| AST07 | Insecure Storage | Plaintext credentials |
| AST08 | Poor Scanning | Malware not detected |
| AST09 | Lack of Monitoring | Attacks go unnoticed |
| AST10 | MAESTRO Misalignment | Security architecture gaps |

**Assessment**:
- Match risks to scenarios (5 questions)
- Identify risk in code (2 code examples)

**Estimated Time**: 60 minutes
**Format**: Interactive lessons + case studies

---

#### 1.3 Risk Assessment Basics
**Target Audience**: Security auditors, developers

**Learning Objectives**:
- Use the risk assessment tool
- Evaluate skill security posture
- Generate risk reports
- Understand remediation priorities

**Hands-On Exercise**:
```
1. Access interactive risk assessment tool
2. Evaluate 3 sample skills
3. Generate reports for each
4. Analyze results and identify patterns
```

**Assessment**:
- Complete assessment of provided skill
- Interpret risk report
- Recommend 3 mitigations

**Estimated Time**: 45 minutes
**Format**: Interactive tool + exercises

---

### Level 2: Intermediate (4-6 hours)

#### 2.1 Secure Skill Development
**Target Audience**: Skill developers

**Learning Objectives**:
- Design secure skills from the start
- Implement secure coding practices
- Perform security review
- Test for vulnerabilities

**Topics**:
1. Security-First Design (30 min)
   - Threat modeling
   - Permission design
   - Data flow analysis

2. Secure Implementation (60 min)
   - Input validation patterns
   - Error handling strategies
   - Secure data storage
   - Code examples in Python, JavaScript, YAML

3. Testing & Verification (45 min)
   - Unit testing security scenarios
   - Integration testing
   - Automated security scanning
   - Static analysis tools

4. Code Review (30 min)
   - Security review checklist
   - Peer review process
   - Common vulnerabilities to spot

**Hands-On Labs**:
```bash
Lab 1: Vulnerable Skill Analysis
- Provided: Skill with 3 security issues
- Task: Identify vulnerabilities
- Submit: Fixed version

Lab 2: Secure Implementation
- Provided: Skill requirements
- Task: Implement securely
- Submit: Code + documentation

Lab 3: Security Testing
- Provided: Skill + test framework
- Task: Write security tests
- Submit: Test suite
```

**Assessment**:
- Complete coding exercise
- Pass code review checklist
- 80% on knowledge quiz

**Estimated Time**: 6 hours
**Format**: Video lessons + hands-on labs

---

#### 2.2 Platform-Specific Security
**Target Audience**: Skill developers for specific platforms

**Courses**:

**2.2a OpenClaw Security** (2 hours)
- SKILL.md structure and best practices
- Permission model deep dive
- ClawHub publishing process
- Security review requirements

**2.2b Claude Code Security** (2 hours)
- skill.json configuration
- Capability-based security
- Integration with Claude
- Anthropic marketplace guidelines

**2.2c Cursor Security** (2 hours)
- manifest.json structure
- Cursor IDE integration
- Performance considerations
- Cursor Registry publishing

**2.2d VS Code Security** (2 hours)
- package.json configuration
- Extension security model
- Workspace trust
- VS Code Marketplace guidelines

**Estimated Time**: 2 hours per platform
**Format**: Video tutorials + platform-specific labs

---

#### 2.3 Security Scanning & Automation
**Target Audience**: DevSecOps, platform operators

**Learning Objectives**:
- Implement automated security scanning
- Set up CI/CD pipelines
- Configure alerting and monitoring
- Generate compliance reports

**Topics**:
1. AST10-Scanner Setup (30 min)
   - Installation and configuration
   - Running scans
   - Interpreting reports

2. CI/CD Integration (60 min)
   - GitHub Actions workflow
   - GitLab CI/CD
   - Custom integrations
   - Pre-commit hooks

3. Monitoring & Response (45 min)
   - Security alerting
   - Incident response
   - Trend analysis
   - Metrics dashboards

**Hands-On Labs**:
```bash
Lab 1: Scanner Setup
- Install AST10-Scanner
- Configure for your platform
- Scan sample skills

Lab 2: CI/CD Pipeline
- Create GitHub Actions workflow
- Configure security gates
- Test with sample skills

Lab 3: Metrics & Alerting
- Set up monitoring
- Configure alerts
- Generate reports
```

**Assessment**:
- Successful pipeline setup
- Scan multiple skills
- Configure alerts
- 75%+ on monitoring quiz

**Estimated Time**: 2.5 hours
**Format**: Video tutorials + hands-on labs

---

### Level 3: Advanced (8-10 hours)

#### 3.1 Threat Modeling for Agent Skills
**Target Audience**: Security architects

**Learning Objectives**:
- Perform threat modeling for skills
- Identify novel attack vectors
- Design defense strategies
- Document security architecture

**Topics**:
1. STRIDE Methodology (45 min)
   - Spoofing attacks on skills
   - Tampering with skill execution
   - Repudiation in skill logs
   - Information disclosure
   - Denial of service
   - Elevation of privilege

2. Attack Trees (45 min)
   - Building attack trees for skills
   - Identifying root causes
   - Prioritizing mitigations

3. Security Architecture (60 min)
   - Designing secure skill pipelines
   - Defense-in-depth strategies
   - Incident response design

**Case Studies**:
- Threat model for ClawHavoc-like attacks
- Defense strategies against supply chain attacks
- Zero-day skill exploitation prevention

**Assessment**:
- Complete threat model for skill
- Create attack tree
- Design mitigation strategy
- Present findings

**Estimated Time**: 3 hours
**Format**: Lectures + group exercises

---

#### 3.2 Advanced Vulnerability Research
**Target Audience**: Security researchers

**Learning Objectives**:
- Discover new vulnerability types
- Develop proof-of-concept exploits
- Responsibly disclose findings
- Contribute to threat intelligence

**Topics**:
1. Vulnerability Discovery (90 min)
   - Static analysis techniques
   - Dynamic analysis
   - Fuzzing skills
   - Code review expertise

2. Exploit Development (90 min)
   - Building exploits safely
   - Testing in sandbox
   - Proof-of-concept documentation
   - Responsible disclosure

3. Threat Intelligence (45 min)
   - Contributing findings
   - Working with platforms
   - Publication and citation

**Research Project**:
- Identify vulnerability class
- Develop discovery method
- Create PoC
- Write paper/disclosure
- Present findings

**Assessment**:
- Complete research project
- Security review of work
- Presentation
- Peer feedback

**Estimated Time**: 4 hours (plus project)
**Format**: Workshops + guided research

---

#### 3.3 Architecture & Governance
**Target Audience**: Platform architects, governance leads

**Learning Objectives**:
- Design secure skill ecosystems
- Implement governance frameworks
- Plan incident response
- Build compliance programs

**Topics**:
1. Ecosystem Architecture (60 min)
   - Registry design
   - Approval workflows
   - Scanning infrastructure
   - Isolation strategies

2. Governance & Policy (75 min)
   - Publisher certification
   - Content policies
   - Dispute resolution
   - Community guidelines

3. Incident Response (60 min)
   - Malware detection
   - Rapid response
   - Skill removal
   - Post-incident analysis

4. Compliance & Audit (45 min)
   - Compliance frameworks
   - Audit procedures
   - Certification maintenance

**Capstone Project**:
Design complete security governance for skill platform

**Assessment**:
- Architecture design document
- Governance policy document
- Incident response plan
- Presentation to peers

**Estimated Time**: 4 hours + capstone (2 weeks)
**Format**: Lectures + capstone project

---

## Certification Tracks

### AST10 Security Analyst (Practitioner)
**Requirements**:
- ✅ Level 1 courses (3 courses)
- ✅ Level 2.1: Secure Development (2 hours)
- ✅ Pass assessment: 80%+
- ✅ Submit: one security audit report

**Qualifies for**:
- Security auditing
- Risk assessment
- Skill review
- Vulnerability reporting

**Credential**: AST10-SA (Analyst)

---

### AST10 Security Engineer (Developer)
**Requirements**:
- ✅ All of Analyst requirements, plus:
- ✅ Level 2: Complete (2.1, 2.2, 2.3)
- ✅ Pass assessments: 85%+
- ✅ Submit: Secure skill project (peer reviewed)

**Qualifies for**:
- Skill development
- Technology consulting
- Training and mentoring
- Platform development

**Credential**: AST10-SE (Engineer)

---

### AST10 Security Architect (Advanced)
**Requirements**:
- ✅ All of Engineer requirements, plus:
- ✅ Level 3: Complete (3.1, 3.2, 3.3)
- ✅ Pass capstone: 90%+ with distinction
- ✅ Publish: Security research or architecture design
- ✅ Mentor: 2+ junior developers

**Qualifies for**:
- Architecture and design
- Threat modeling
- Governance and policy
- Research and publication
- Conference speaking

**Credential**: AST10-SA (Architect)

---

## Getting Started

### Recommended Paths by Role

#### Security Practitioners
```
Week 1: Level 1 (Fundamentals)
  - Course 1.1: Introduction (45 min)
  - Course 1.2: 10 Risks (60 min)
  - Course 1.3: Assessment (45 min)

Week 2: AST10-SA Certification
  - Course 2.1: Secure Development (60 min overview)
  - Security audit project
  - Assessment & certification
```

#### Skill Developers
```
Week 1-2: Level 1 (Fundamentals)
  - All Level 1 courses
  - Risk assessment exercises

Week 3-4: Level 2 (Intermediate)
  - Course 2.1: Secure Development (full)
  - Platform-specific course (2.2a-2.2d)
  - Hands-on labs

Week 5: AST10-SE Certification
  - Develop and audit secure skill
  - Code review and certification
```

#### Platform Operators
```
Week 1: Level 1 (Fundamentals)
Week 2: Level 2.3 (CI/CD Integration)
Week 3-4: Level 3.3 (Governance)
Result: Architecture and governance capability
```

### Enrollment

1. **Register** at [OWASP Learning Platform](https://learn.owasp.org)
2. **Complete** recommended path for your role
3. **Pass** assessments (70%+ for Analyst, 85%+ for Engineer, 90%+ for Architect)
4. **Submit** project work
5. **Receive** credential and certificate

### Cost

- **Level 1 Courses**: Free (public learning)
- **Level 2 Courses**: $99 per course (OWASP member: $49)
- **Level 3 Courses**: $199 per course (OWASP member: $99)
- **Certification Exam**: $49 (Analyst), $99 (Engineer), $199 (Architect)

OWASP members receive 50% discount on all paid courses.

---

## Continuing Education

Once certified, maintain credential by:
- Completing annual refresher (2 hours)
- Staying current with emerging threats
- Participating in community
- Publishing research or contributions

---

*Training program updated March 2026. New courses added regularly.*