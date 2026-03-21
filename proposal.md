# OWASP Project Proposal: Agentic Skills Top 10 

## Project Overview

**Project Name**: OWASP Agentic Skills Top 10  
**Status**: New Project Proposal  
**License**: Creative Commons Attribution ShareAlike 4.0 (CC-BY-SA-4.0)

**Agentic Skills Top 10** documents the 10 most critical security risks in agentic AI skills across OpenClaw (SKILL.md YAML), Claude Code (skill.json), Cursor/Codex (manifest.json), and VS Code (package.json) ecosystems. Skills represent the execution layer giving agents real-world impact through platform-specific metadata \+ scripts.

**Problem**: No dedicated security guidance exists for agent skills despite their role as the primary attack surface for autonomous AI actions.

## Key Deliverables

1. **10 Risk Pages**: Description, platform-specific attack scenarios, preventive mitigations, OWASP mappings  
2. **Platform Matrix**: Metadata formats, verification hooks, scanning requirements per ecosystem  
3. **Universal Skill Format**: Proposed YAML standard mitigating AST10 (cross-platform reuse)  
4. **Cheat Sheets**: Quick-reference controls for developers, AppSec teams, GRC  
5. **Slide Deck**: Conference-ready presentation (RSA, OWASP Global AppSec)

## Project Links (Planned)

- **GitHub**: `github.com/OWASP/www-project-agentic-skills-top-10`  
- **OWASP Page**: `owasp.org/projects/agentic-skills-top-10`


## Goals & Success Metrics

| Goal | Metric | Target |
| :---- | :---- | :---- |
| **v1.0 Release** | Complete 10 risks \+ mappings | Q3 2026 |
| **OWASP Flagship** | Project review \+ approval | Q4 2026 |
| **Adoption** | Conference presentations | 3+ (RSA, OWASP) |

## Scope

### In Scope

✅ Agent skills across ALL platforms:

├── OpenClaw: SKILL.md (YAML frontmatter)

├── Claude Code: skill.json/YAML \+ scripts/

├── Cursor/Codex: manifest.json \+ handlers  

├── VS Code: package.json \+ extensions

✅ 10 risks: AST01 Malicious Skills → AST10 Cross-Platform Reuse

✅ Platform-specific scenarios \+ universal mitigations

✅ Universal skill format proposal (AST10 solution)

### Out of Scope

❌ Protocol risks (OWASP MCP Top 10\)

❌ LLM/model risks (OWASP LLM Top 10\) 

❌ Tool/scanner implementation (guidance only)

❌ Non-agentic skills/plugins

## Target Audience

| Role | Need |
| :---- | :---- |
| **AI Platform Devs** | Secure skill runtimes, marketplaces, installers |
| **AppSec Teams** | Govern skills in enterprise deployments |
| **Skill Authors** | Write safe metadata/scripts |
| **GRC** | Compliance mapping (NIST AI RMF, ISO 42001\) |

## Relationship to Existing OWASP Projects

| OWASP Project | AST10 Relationship |
| :---- | :---- |
| **LLM Top 10** | AST10 extends LLM03 Supply Chain to skills |
| **Agentic Top 10** | AST10 specializes "tools layer" beneath agents |
| **MCP Top 10** | MCP \= protocol security; AST10 \= skill content security |
| **ASVS v5** | Skill-specific verification requirements |
| **SAMM v3** | Agentic skill maturity practices |

**Layered Defense**: MCP Top 10 (protocol) → **AST10** (skills) → LLM/Agentic Top 10 (models)

## The 10 Risks (Summary)

| \# | Risk | Platforms Affected | Key Mitigation |
| :---- | :---- | :---- | :---- |
| AST01 | Malicious Skills | All | Merkle root signing |
| AST02 | Supply Chain | All | Registry transparency |
| AST03 | Over-Privileged | All | Schema validation |
| AST04 | Insecure Metadata | All | Static analysis |
| AST05 | Prompt Injection | All | Prompt sanitization |
| AST06 | Weak Isolation | All | Containerization |
| AST07 | Update Drift | All | Immutable pinning |
| AST08 | Poor Scanning | All | Multi-tool pipeline |
| AST09 | No Governance | All | Skill inventories |
| **AST10** | Cross-Platform | **All** | Universal YAML format |

## Detailed Timeline

### Phase 1: Foundation (Q2 2026\)

Week 1-2:  GitHub repo \+ project page \+ 10 risk skeletons

Week 3-4:  AST01-AST03 full writeups \+ platform matrix

Week 5-6:  AST04-AST06 \+ mappings to OWASP projects

Week 7-8:  v0.5 release \+ community review

### Phase 2: Completion (Q3 2026\)

Week 9-12: AST07-AST10 \+ universal format proposal

Week 13-14: Cheat sheets \+ slide deck \+ PDF export

Week 15-16: v1.0 RC \+ OWASP review

### Phase 3: Launch (Q4 2026\)

Week 17:   v1.0 release \+ flagship submission

Week 18+:  Conference talks \+ enterprise adoption

**Total Effort**: \~250 volunteer hours, zero budget required.

## Leadership & Governance

### Project Leads

- **Ken Huang** \- OWASP AIVSS Lead, Agentic AI Security Researcher  
  - OpenClaw threat modeling, skill security scanning research  
  - RSA/OWASP conference speaker on AI security

### Reviewers (TBD)

\[ \] OWASP AI Security Project Leads

\[ \] OpenClaw/Claude Code maintainers  

\[ \] Cursor AI security team

\[ \] OWASP ASVS/SAMM contributors

### Contribution Model

GitHub Issues: Risk suggestions, scenarios, mitigations

GitHub PRs: Content \+ platform examples

Monthly calls: OWASP Zoom (1st Thursday)

Slack: \#proj-agentic-skills-top-10

## Alignment with OWASP MCP Top 10

**MCP secures protocol risks; AST10 secures skill content:**

| AST Risk | MCP Mapping |
| :---- | :---- |
| AST01 Malicious Skills | MCP03 Tool Poisoning |
| AST02 Supply Chain | MCP04 Supply Chain Attacks |
| AST03 Privileges | MCP02 Scope Creep |
| AST10 Cross-Platform | MCP09 Shadow Servers |

**Mental Model**: "MCP \= how model talks to tools; AST10 \= what tools actually do"

## Universal Skill Format (AST10 Solution)

\---

name: example-skill

platforms: \[openclaw, claude, cursor, vscode\]

version: 1.0.0

description: "Safe example skill"

permissions:

  files: 

    \- read: \~/.config/app.json

      write: \~/.config/app.json

  network: false

requires:

  binaries: \[jq\]

risk\_tier: L1  \# L0=safe, L3=destructive

signature: "ed25519:ABC123..."

## Risks & Mitigations

| Risk | Mitigation |
| :---- | :---- |
| Scope creep | Strict in/out scope definition |
| Platform changes | Annual updates based on ecosystem evolution |
| Low adoption | Conference talks \+ OWASP flagship status |

## Next Steps

1. **Immediate**: Create `github.com/OWASP/www-project-agentic-skills-top-10`  
2. **Week 1**: Populate with v0.1 (AST01-AST03 \+ proposal)  
3. **Week 2**: OWASP project submission form  
4. **Week 4**: First community call \+ reviewer recruitment
