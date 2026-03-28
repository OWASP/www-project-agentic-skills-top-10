# 🚀 Official Announcement: OWASP Agentic Skills Top 10

**The First Comprehensive Security Framework for AI Agent Skills**

---

## 📢 We're Excited to Announce...

The **OWASP Agentic Skills Top 10 (AST10)** project is now officially launched! This is the first comprehensive security framework dedicated to addressing the critical security risks in AI agent skills across all major platforms.

---

## 🎯 What Is OWASP AST10?

The OWASP Agentic Skills Top 10 documents the **10 most critical security risks** in agentic AI skills, providing evidence-based mitigations and prevention strategies for:

- **OpenClaw** (SKILL.md YAML format)
- **Claude Code** (skill.json/YAML + scripts)
- **Cursor/Codex** (manifest.json + handlers)
- **VS Code** (package.json + extensions)

### Why This Matters Now

The AI agent skill ecosystem is under **active attack** as of Q1 2026:

| Threat | Impact | Evidence |
|--------|--------|----------|
| ClawHavoc Campaign | 1,184 malicious skills | Antiy CERT (Feb 2026) |
| Registry Poisoning | 36.82% skills vulnerable | Snyk ToxicSkills (Feb 2026) |
| Claude Code RCE | CVE-2025-59536/21852 | Check Point Research (Feb 2026) |
| WebSocket Hijacking | CVE-2026-28363 | Oasis Security (Feb 2026) |
| Supply Chain Attacks | 280+ leaky skills | Snyk (Feb 2026) |

---

## 📋 The 10 Critical Risks

| # | Risk | Severity | Key Mitigation |
|---|------|----------|----------------|
| AST01 | Malicious Skills | Critical | Cryptographic signing, behavioral scanning |
| AST02 | Supply Chain Compromise | Critical | Transparency logs, dependency pinning |
| AST03 | Over-Privileged Skills | High | Least-privilege manifests, runtime enforcement |
| AST04 | Insecure Metadata | High | Schema validation, provenance tracking |
| AST05 | Unsafe Deserialization | High | Safe parsers, sandboxed loading |
| AST06 | Weak Isolation | High | Containerization, process isolation |
| AST07 | Update Drift | Medium | Immutable pinning, hash verification |
| AST08 | Poor Scanning | Medium | Multi-tool pipeline, semantic analysis |
| AST09 | No Governance | Medium | Skill inventories, audit logging |
| AST10 | Cross-Platform Reuse | Medium | Universal format, platform validation |

---

## 🛠️ How to Use This Project

### For Security Teams

1. **Assess Your Posture**: Use the [Security Assessment Checklist](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/checklist.md)
2. **Review Risks**: Read the 10 AST files for platform-specific guidance
3. **Implement Controls**: Apply mitigations appropriate to your environment
4. **Monitor Threats**: Subscribe to security advisories

### For Skill Developers

1. **Follow Best Practices**: Implement least-privilege and secure coding
2. **Use Universal Format**: Adopt the cross-platform standard
3. **Sign Your Skills**: Enable cryptographic verification
4. **Test Security**: Validate in isolated environments

### For Platform Developers

1. **Registry Security**: Implement scanning and provenance tracking
2. **Runtime Isolation**: Default to sandboxed execution
3. **Audit Logging**: Enable comprehensive activity monitoring
4. **User Trust**: Require explicit confirmation for privileged operations

---

## 🚀 Quick Start

### Submit New Risk Entries

Use our **interactive web form** to submit new AST risk entries:

**👉 [Submit New Risk Entry](https://owasp.github.io/www-project-agentic-skills-top-10/assets/new-ast-form.html)**

The form generates properly formatted markdown and provides multiple submission options:
- Direct GitHub file creation
- Create GitHub Issue
- Download and manual PR

### Browse Documentation

- **🌐 Website**: [https://owasp.github.io/www-project-agentic-skills-top-10/](https://owasp.github.io/www-project-agentic-skills-top-10/)
- **📖 Full Documentation**: [README.md](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/README.md)
- **📋 Risk Details**: [index.md](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/index.md)
- **🔍 Security Checklist**: [checklist.md](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/checklist.md)
- **🔧 Universal Format**: [universal-skill-format.md](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/universal-skill-format.md)

---

## 🤝 How to Contribute

We welcome contributions from the security community!

### Ways to Contribute

- **🐛 Report Issues**: Found a security risk or documentation error?
- **✨ Add Content**: New examples, mitigations, or research
- **🔧 Code Examples**: Provide secure coding patterns
- **🌐 Translations**: Help localize the guide
- **📊 Research**: Share threat intelligence or analysis

### Getting Started

1. **Read Guidelines**: Check [CONTRIBUTING.md](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/CONTRIBUTING.md)
2. **Fork & Clone**: Work on your own branch
3. **Use Templates**: Issue and PR templates provided
4. **Test Changes**: Run validation scripts
5. **Submit PR**: Follow the contribution workflow

### Submit New Risks

Use the [New AST Form](https://owasp.github.io/www-project-agentic-skills-top-10/assets/new-ast-form.html) to submit new risk entries with proper formatting.

---

## 📅 Community

### Stay Updated

Sign up to receive updates about the OWASP Agentic Skills Top 10 project:

**📋 [Sign Up for Updates](https://docs.google.com/document/d/1WIAMIZnH5kivRGF7QDhOFNO3zPs9y5MxjmTf1hcZ9Ms/edit?tab=t.0)** *(Google Document)*

### Communication Channels

- **🐙 GitHub**: [Issues](https://github.com/OWASP/www-project-agentic-skills-top-10/issues) and [Discussions](https://github.com/OWASP/www-project-agentic-skills-top-10/discussions)
- **📧 Contact**: Reach out via GitHub Issues for questions or suggestions

---

## 📊 Project Status

**Status**: Active Development → Launch Preparation  
**Version**: 1.0 (2026 Edition)  
**License**: CC BY-SA 4.0  

### Timeline

| Phase | Status | Deliverables |
|-------|--------|-------------|
| Foundation | ✅ Complete | Repo, OWASP page, AST01-10 drafts |
| Content Expansion | ✅ Complete | Examples, code samples, references |
| UX & Community | ✅ Complete | Templates, checklists, interactive elements |
| Maintenance Setup | ✅ Complete | Automation, governance, procedures |
| Launch Preparation | 🔄 In Progress | Final polish, validation, promotion |

---

## 📚 Resources

### Documentation
- **[Full Website](https://owasp.github.io/www-project-agentic-skills-top-10/)**: Complete documentation
- **[Risk Details](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/top10.md)**: All 10 risks in one document
- **[Security Checklist](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/checklist.md)**: Assessment and remediation guide
- **[Universal Format](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/universal-skill-format.md)**: Cross-platform standard specification

### Research & References
- **Snyk ToxicSkills** (Feb 2026): Comprehensive skill ecosystem audit
- **Check Point Research**: Claude Code vulnerability analysis
- **Antiy CERT**: ClawHavoc campaign analysis
- **CSA MAESTRO**: 7-layer threat model for agentic AI

### Tools & Automation
- **[Validation Script](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/validate.sh)**: Content quality checker
- **[Maintenance Guide](https://github.com/OWASP/www-project-agentic-skills-top-10/blob/main/MAINTENANCE.md)**: Long-term project procedures
- **GitHub Actions**: Automated testing and deployment

---

## 🎯 Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| Adoption | Registries implementing Universal Format | 2+ major registries |
| Community | Contributors, active discussions | 50+ contributors |
| Impact | Referenced in OWASP Top 10, industry standards | Industry recognition |
| Quality | Link validity, comprehensive coverage | 100% coverage |

---

## 📞 Contact

**Project Lead**: Ken Huang — OWASP AIVSS Lead, Agentic AI Security Researcher

- **📧 Email**: ken.huang@owasp.org
- **🐙 GitHub**: [@kenhuang](https://github.com/kenhuang)
- **🔗 LinkedIn**: [Ken Huang](https://linkedin.com/in/kenhuang)

For questions, suggestions, or to get involved:
- Open an [issue](https://github.com/OWASP/www-project-agentic-skills-top-10/issues) on GitHub
- Submit a [pull request](https://github.com/OWASP/www-project-agentic-skills-top-10/pulls) with your contribution
- [Sign up for updates](https://docs.google.com/document/d/1WIAMIZnH5kivRGF7QDhOFNO3zPs9y5MxjmTf1hcZ9Ms/edit?tab=t.0) to stay informed

---

## 🙏 Acknowledgments

This project is made possible by the contributions of the security community and the support of the OWASP Foundation.

Special thanks to:
- The OWASP community for project hosting and governance
- Security researchers who disclosed vulnerabilities responsibly
- Contributors who help improve the documentation and mitigations
- Platform developers working to improve skill security

---

## 📜 License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to share and adapt this material for any purpose, provided you give appropriate credit, provide a link to the license, indicate if changes were made, and distribute your contributions under the same license.

---

**Let's build a more secure AI agent ecosystem together!** 🛡️🤖

*OWASP Agentic Skills Top 10 - Protecting the AI Agent Ecosystem*

---

*Last Updated: March 27, 2026*