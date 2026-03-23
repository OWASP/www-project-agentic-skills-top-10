---
layout: col-sidebar
title: Community & Contribution Guide
tags: contributing, community, involvement
level: 2
type: documentation
pitch: Get involved with OWASP AST10 community and contribute
description: "Guidelines for contributing to OWASP Agentic Skills Top 10 project, including research, documentation, tools, and community roles."
---

# Community & Contribution Guide

The OWASP Agentic Skills Top 10 project thrives through community participation. This guide explains how you can contribute to improving AI agent skill security.

## Ways to Contribute

### 1. Security Research & Analysis

**What We Need**:
- Vulnerability analyses of published skills
- Threat modeling and attack scenarios
- Security testing methodologies
- Incident documentation

**How to Contribute**:
```markdown
1. Research a security aspect of AI agent skills
2. Document your findings in a GitHub issue
3. Create a pull request with your analysis
4. Participate in peer review

# Example Research Contribution
- Topic: "Zero-Day Vulnerability in SKILL.md Parsing"
- Format: GitHub discussion or pull request
- Include: Technical details, test cases, remediation
```

**Recognition**:
- Author credit in documentation
- Featured researcher profile
- Speaking opportunities at OWASP events

### 2. Documentation Improvements

**What We Need**:
- Clearer explanations of risks
- Additional code examples
- Platform-specific guides
- Translation to other languages

**How to Contribute**:
```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/www-project-agentic-skills-top-10.git

# Create a branch for your improvements
git checkout -b improve/documentation

# Make improvements
# - Update existing docs
# - Add examples
# - Fix typos
# - Clarify explanations

# Commit and push
git commit -m "Improve documentation for [topic]"
git push origin improve/documentation

# Create pull request
```

**Documentation Standards**:
- Follow existing markdown format
- Include code examples where applicable
- Add cross-references to related risks
- Update table of contents if adding sections

### 3. Tool Development

**What We Need**:
- Security scanning tools
- Automated assessment frameworks
- CLI utilities
- Browser extensions

**Featured Tools**:

#### AST10 Scanner
```bash
# Contribute to scanner development
git clone https://github.com/OWASP/ast10-scanner
cd ast10-scanner

# Add new detection rules
vim rules/ast01_detection.py

# Add test cases
vim tests/test_ast01.py

# Submit pull request
```

#### Skill Validator
```javascript
// Contribute to web-based validator
// Location: /tools/skill-validator
// Technologies: React, TypeScript, TailwindCSS

// Add new validation rule
export const validateSkillPermissions = (skill) => {
  // Implementation
}

// Add unit test
describe('validateSkillPermissions', () => {
  it('should detect over-privileged skills', () => {
    // Test case
  })
})
```

### 4. Training & Educational Content

**What We Need**:
- Tutorial videos
- Workshop materials
- Certification courses
- Interactive learning modules

**Create Video Tutorials**:
```
Topics needed:
1. "Getting Started with Secure Skill Development"
2. "AST10 Risk Identification Walkthrough"
3. "Setting Up CI/CD Security Scanning"
4. "Platform Comparison: Choosing Your Ecosystem"

Format:
- 5-15 minute videos
- Screen recorded with narration
- Subtitles for accessibility
- Code examples included
```

**Workshop Materials**:
- Hands-on labs with sample skills
- Security audit guided exercises
- Remediation workshops
- Certification exam prep

### 5. Community Support

**What We Need**:
- Answer questions in discussions
- Help with security reviews
- Mentor new contributors
- Facilitate community events

**Support Roles**:
- **Discussion Moderator**: Help answer questions, direct to resources
- **Code Reviewer**: Review pull requests, suggest improvements
- **Event Organizer**: Organize local meetups or webinars
- **Ambassador**: Promote AST10 in your network

## Contribution Process

### Step-by-Step Guide

#### 1. Identify Contribution
```
- Check GitHub issues for open items
- Propose new research in discussions
- Review roadmap for planned work
```

#### 2. Set Up Development Environment
```bash
# Clone repository
git clone https://github.com/OWASP/www-project-agentic-skills-top-10.git
cd www-project-agentic-skills-top-10

# Create feature branch
git checkout -b feature/your-contribution-name

# Set up locally
# For documentation: No setup needed
# For tools: See individual tool documentation
```

#### 3. Make Your Contribution
```bash
# Make improvements to files
# Test thoroughly
# Add documentation
# Update references
```

#### 4. Submit for Review
```bash
# Commit changes
git add .
git commit -m "Description of contribution

- Details of what was added/changed
- Links to related issues
- Any testing performed"

# Push to your fork
git push origin feature/your-contribution-name

# Create pull request on GitHub
# - Link related issues
# - Describe changes clearly
# - Tag reviewers if known
```

#### 5. Participate in Review
```
- Respond to reviewer feedback
- Make requested changes
- Answer clarifying questions
- Update based on suggestions
```

#### 6. Merge & Recognition
```
- PR gets approved and merged
- You're added to contributors list
- Your contribution appears in release notes
- Recognition in community announcements
```

## Code of Conduct

All contributors agree to:

1. **Be Respectful**: Treat all community members with respect
2. **Constructive Criticism**: Provide feedback that helps improve
3. **Inclusivity**: Welcome contributors from all backgrounds
4. **Security Focus**: Prioritize security and user safety
5. **Transparency**: Be open about limitations and trade-offs

## Contribution Areas

### High Priority (Looking for Contributors Now)

- [ ] Spanish translation of documentation
- [ ] Python skill scanner implementation
- [ ] Interactive platform comparison tool
- [ ] Incident response playbooks
- [ ] Video tutorials (Basic to Advanced)
- [ ] Hands-on security labs
- [ ] API SDK for additional languages (Go, Rust)

### Medium Priority

- [ ] Additional case studies (post-2026)
- [ ] Platform-specific deep dives
- [ ] Custom rule development guide
- [ ] Skill audit checklist tools
- [ ] Security training certification

### Community-Driven

- [ ] Research on emerging threats
- [ ] New risk discovery and analysis
- [ ] Tool integrations
- [ ] Community-submitted best practices

## Recognition & Rewards

### Contributors List
All contributors are recognized in:
- GitHub Contributors page
- Project documentation
- Monthly community highlights
- Annual OWASP reports

### Speaking Opportunities
- Present at OWASP AppSec conferences
- Lead workshops and training sessions
- Guest appearances on podcast
- Author guest articles

### Certification Pathway
Contributing significantly can lead to:
- OWASP AST10 Security Analyst Certification
- Featured Expert status
- Speaking engagement opportunities
- Career advancement in security

## Community Channels

### GitHub
- **Issues**: Report bugs, suggest features
- **Discussions**: Ask questions, share ideas
- **Pull Requests**: Submit contributions
- **Releases**: Follow project updates

### Contact
- **Email**: security@owasp.org/ast10
- **Twitter**: @OWASP
- **Slack**: OWASP Community Slack
- **Forum**: OWASP Project Forum

## Contributors Hall of Fame

### Active Contributors (2026)

#### Research Contributors
- Thanks to Snyk researchers for ToxicSkills data
- Check Point Research for ClawHavoc analysis
- Antiy CERT for threat intelligence

#### Documentation Contributors
- [Your name here - get started today!]

#### Tool Developers
- Community developers of AST10-Scanner
- Security researchers building detection tools

-----

## Getting Help

### For Questions
```
1. Check existing GitHub discussions
2. Ask in GitHub Discussions tab
3. Contact project leads
4. Post in community forums
```

### For Technical Issues
```
1. Check documentation/troubleshooting
2. Search closed GitHub issues
3. Open new issue with details
4. Contact maintainers if needed
```

### For Security Issues
```
1. DO NOT post publicly
2. Email: security@owasp.org
3. Include details but no sensitive info
4. Follow responsible disclosure
```

---

## Start Contributing Today!

**New to contributing?**
1. Look at "good first issue" label on GitHub
2. Start with documentation improvements
3. Submit your first pull request
4. Join the community!

**Ready to dive deeper?**
1. Review open research topics
2. Propose new security analysis
3. Develop security tools
4. Become a community mentor

**Questions?**
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
- Join [GitHub Discussions](https://github.com/OWASP/www-project-agentic-skills-top-10/discussions)
- Email: contributors@owasp.org

Welcome to the OWASP AST10 community! 🛡️

---

*Last updated: March 2026*