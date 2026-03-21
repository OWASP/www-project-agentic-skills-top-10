---
layout: col-sidebar
title: OWASP Agentic Skills Top 10
tags: agentic-security, ai-safety, llm-security
level: 2
type: documentation
pitch: A shared vocabulary and framework to review, approve, and govern AI agent capabilities
---

# OWASP Agentic Skills Top 10

The OWASP Agentic Skills Top 10 provides organizations with a shared vocabulary and framework to review, approve, and govern AI agent capabilities. It treats skills as static artifacts that can be audited before deployment in ecosystems like OpenClaw, Claude Code, Cursor, and VS Code.

## Why We Need the Agentic Skills Top 10

As AI agents become increasingly integrated into software development and business operations, new security risks emerge that traditional security frameworks don't address. The OWASP Agentic Skills Top 10 was created to address these critical gaps:

### The Growing Threat Landscape

- **AI agents have real-world impact**: Unlike traditional software, AI agents can autonomously execute actions, access systems, and make decisions that affect production environments
- **Skills as attack vectors**: AI agent "skills" (predefined capabilities) can be exploited to perform unauthorized actions
- **Lack of governance**: Organizations deploy AI agents without proper security assessment or approval processes
- **Supply chain risks**: Third-party skills repositories introduce unknown risks into development workflows

### Why Traditional Security Fails

- **Static analysis doesn't work**: AI agents can dynamically generate and execute code based on context
- **No audit trail**: Many skills operate without logging or traceability
- **Permission creep**: Skills often request excessive permissions without justification
- **No standardization**: Each platform implements skills differently, making security assessment inconsistent

### The Business Case

- **Regulatory compliance**: Organizations need to demonstrate due diligence in AI governance
- **Risk mitigation**: Proactive assessment prevents costly security incidents
- **Trust building**: Security assessments build confidence with stakeholders and customers
- **Best practices**: Establishes industry standards for AI agent security

## What Are the Agentic Skills Top 10?

The Agentic Skills Top 10 identifies the most critical security risks associated with AI agent capabilities. Each skill represents a potential attack vector that organizations should assess before deploying AI agents.

### Risk Categories

1. **Unauthorized Access & Privilege Escalation**
   - Skills that can access restricted resources
   - Capabilities that escalate privileges beyond intended scope

2. **Data Exfiltration & Privacy Violations**
   - Skills that can read or transmit sensitive data
   - Capabilities that violate user privacy expectations

3. **Code Injection & Execution**
   - Skills that can execute arbitrary code
   - Capabilities that bypass security controls

4. **Supply Chain Compromise**
   - Skills from unverified sources
   - Capabilities that introduce unknown dependencies

5. **Autonomous Decision-Making Risks**
   - Skills that make decisions without human oversight
   - Capabilities that can cause unintended consequences

6. **Audit & Logging Bypass**
   - Skills that operate without traceability
   - Capabilities that hide their actions

7. **Permission Misconfiguration**
   - Skills with excessive permissions
   - Capabilities that don't follow least-privilege principles

8. **Platform-Specific Vulnerabilities**
   - Risks unique to specific AI agent platforms
   - Gaps in platform security controls

9. **Human-in-the-Loop Bypass**
   - Skills that circumvent human oversight
   - Capabilities that operate autonomously when they shouldn't

10. **Security Policy Evasion**
   - Skills that bypass security policies
   - Capabilities that ignore organizational constraints

## Roadmap

- **Q1**: Finalize the Version 1.0 taxonomy and publish technical analysis for the initial five risks
- **Q2**: Release the Skill Security Assessment Checklist and define automated scanning patterns for tools like Semgrep and Bandit
- **Q3**: Collaborate with platform providers to pilot mitigations for platform-specific security gaps
- **Q4**: Launch the Universal Skill Format draft to enable consistent security policy alignment across AI agent platforms

## How to Contribute

We welcome contributions from the security community! Here's how you can help:

### Getting Started

1. **Join the OWASP Slack workspace** to connect with the community and get help with any questions
2. **Review the project goals** and find areas where you can contribute
3. **Fork the repository** and clone it to your local machine

### Contribution Areas

- **Research**: Contribute analysis of new AI agent security risks
- **Documentation**: Improve existing documentation or create new guides
- **Tools**: Develop automated scanning tools for skill assessment
- **Best Practices**: Share real-world experiences and lessons learned
- **Platform Integration**: Help integrate security checks with popular AI agent platforms

### Submitting Changes

1. Make your changes and test them locally
2. Submit a pull request with a clear description of your changes
3. Ensure your changes follow the project's coding standards
4. Include tests if applicable
5. Provide a clear and concise description of the changes

### Code of Conduct

We ask that all contributors to OWASP projects abide by our [Code of Conduct](https://owasp.org/www-policy/operational/code-of-conduct). This code outlines our expectations for behavior within the project community and helps us maintain a welcoming and inclusive environment for all contributors.

## Resources

- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [License](LICENSE.md)

## Leaders

- [Ken Huang](mailto:ken.huang@owasp.org)
- [Fabio Cerullo](mailto:ken.huang@owasp.org)

---

*This project is maintained by OWASP as an Incubator Project.*