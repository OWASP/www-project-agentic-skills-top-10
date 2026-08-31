---
layout: col-sidebar
title: Incident Report Template
tags: incident-response, template
level: 2
type: documentation
---

# Incident Report Template

Use this template to document a skill-related security incident consistently.

## Metadata

- Incident ID:
- Date/Time Detected (UTC):
- Severity:
- Reporter:
- Affected Platforms:
- Current Status:

## Summary

Brief description of what happened and why it matters.

## Scope and Impact

- Affected users/systems:
- Data impact:
- Business impact:

## Timeline

- T0 Detection:
- T1 Containment:
- T2 Remediation:
- T3 Recovery:

## Indicators of Compromise

- Domain/IP:
- File hash:
- Behavioral indicator:

## Actions Taken

- Containment steps:
- Remediation steps:
- Communication steps:

## Root Cause

What enabled this incident and what failed.

## Runtime Authority (if applicable)

Fill in for incidents where legitimate agents/skills exercised authority beyond user intent. See [Runtime Authority Incident Response](runtime-authority-ir.md).

- Originating principal and consent record:
- Delegation chain (user → agent → delegated agent → skill → tool):
- Transition states per hop (inherited/narrowed/rejected/revoked/amplified/unverifiable):
- First amplification hop and mechanism:
- Effective runtime authority at time of action:
- Containment boundary used and revocation verification result:
- Stale grants/credentials discovered and invalidated:

## Preventive Actions

1. 
2. 
3. 
