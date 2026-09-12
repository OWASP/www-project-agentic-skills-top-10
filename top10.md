---
layout: col-sidebar
title: The Top 10 Risks — Visual Overview
tags: agentic-security, top-10, overview
level: 2
type: documentation
pitch: A visual map of the 10 agentic-skill security risks
description: "Visual overview of the OWASP Agentic Skills Top 10 — a lifecycle diagram plus a card for every risk (AST01–AST10), colour-coded by severity, linking to full details."
---

# OWASP Agentic Skills Top 10 — Visual Overview

A one-screen map of all ten risks. The diagram shows **where** each risk attacks the skill lifecycle; the cards below summarise **what** each risk is and link to full details. Severity is shown by both colour **and** label, so the page is readable without relying on colour alone.

> Prefer text? See the [summary table](index.md#summary-table) or the practical [assessment checklist](checklist.md).

<div class="ast-top10" markdown="0">

<style>
.ast-top10 { --crit:#c0252b; --high:#d9701b; --med:#b88a00; --navy:#13395c;
  --ink:#1f2937; --muted:#5b6675; --line:#e3e7ee; --card:#ffffff;
  font-family: inherit; color: var(--ink); margin: 0 0 1rem; }
.ast-top10 * { box-sizing: border-box; }

.ast-figure { background:#f7f9fc; border:1px solid var(--line); border-radius:14px;
  padding:14px 16px; margin:0 0 22px; }
.ast-figure svg { width:100%; height:auto; display:block; }
.ast-figcap { font-size:.82rem; color:var(--muted); margin:6px 2px 0; text-align:center; }

.ast-legend { display:flex; flex-wrap:wrap; gap:14px; margin:0 0 18px; font-size:.85rem; }
.ast-legend span { display:inline-flex; align-items:center; gap:7px; color:var(--muted); }
.ast-dot { width:13px; height:13px; border-radius:3px; display:inline-block; }
.ast-dot.crit{background:var(--crit)} .ast-dot.high{background:var(--high)} .ast-dot.med{background:var(--med)}

.ast-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(285px,1fr)); gap:16px; }
.ast-card { position:relative; display:flex; flex-direction:column; background:var(--card);
  border:1px solid var(--line); border-left-width:5px; border-radius:12px; padding:16px 16px 14px;
  text-decoration:none; color:inherit; transition:box-shadow .15s ease, transform .15s ease; }
.ast-card:hover { box-shadow:0 6px 20px rgba(19,57,92,.13); transform:translateY(-2px); }
.ast-card.crit{ border-left-color:var(--crit) } .ast-card.crit .ast-ico,.ast-card.crit .ast-id{color:var(--crit)}
.ast-card.high{ border-left-color:var(--high) } .ast-card.high .ast-ico,.ast-card.high .ast-id{color:var(--high)}
.ast-card.med { border-left-color:var(--med)  } .ast-card.med  .ast-ico,.ast-card.med  .ast-id{color:var(--med)}
.ast-top { display:flex; align-items:center; gap:11px; }
.ast-ico svg { width:30px; height:30px; display:block; }
.ast-id { font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.ast-pill { margin-left:auto; font-size:.66rem; font-weight:700; letter-spacing:.04em; text-transform:uppercase;
  color:#fff; padding:3px 9px; border-radius:999px; }
.ast-pill.crit{background:var(--crit)} .ast-pill.high{background:var(--high)} .ast-pill.med{background:var(--med)}
.ast-title { font-size:1.04rem; font-weight:700; color:var(--navy); margin:11px 0 6px; line-height:1.25; }
.ast-desc { font-size:.88rem; line-height:1.45; color:var(--muted); margin:0 0 12px; flex:1; }
.ast-more { font-size:.82rem; font-weight:700; color:var(--navy); }
.ast-card:hover .ast-more { text-decoration:underline; }
</style>

<div class="ast-figure" role="img" aria-label="Skill lifecycle from Author and Publish through Detect and Govern, showing which AST risks attack at each phase.">
<svg viewBox="0 0 1000 250" xmlns="http://www.w3.org/2000/svg" font-family="inherit">
  <text x="500" y="22" text-anchor="middle" font-size="16" font-weight="700" fill="#13395c">Where each risk attacks the skill lifecycle</text>

  <rect x="20"  y="42" width="179" height="50" rx="10" fill="#13395c"/>
  <rect x="215" y="42" width="179" height="50" rx="10" fill="#13395c"/>
  <rect x="410" y="42" width="179" height="50" rx="10" fill="#13395c"/>
  <rect x="605" y="42" width="179" height="50" rx="10" fill="#13395c"/>
  <rect x="800" y="42" width="179" height="50" rx="10" fill="#13395c"/>
  <g fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">
    <text x="109" y="72">Author &amp; Publish</text>
    <text x="304" y="72">Distribute &amp; Install</text>
    <text x="499" y="72">Load &amp; Permission</text>
    <text x="694" y="72">Execute &amp; Isolate</text>
    <text x="889" y="72">Detect &amp; Govern</text>
  </g>

  <g fill="none" stroke="#94a3b8" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
    <path d="M203 61 l9 6 l-9 6"/>
    <path d="M398 61 l9 6 l-9 6"/>
    <path d="M593 61 l9 6 l-9 6"/>
    <path d="M788 61 l9 6 l-9 6"/>
  </g>

  <g font-size="11.5" font-weight="700" fill="#ffffff">
    <rect x="24" y="110" width="171" height="24" rx="6" fill="#d9701b"/><text x="34" y="126">AST04 · Insecure Metadata</text>
    <rect x="24" y="142" width="171" height="24" rx="6" fill="#c0252b"/><text x="34" y="158">AST02 · Supply Chain</text>
    <rect x="219" y="110" width="171" height="24" rx="6" fill="#c0252b"/><text x="229" y="126">AST01 · Malicious Skills</text>
    <rect x="219" y="142" width="171" height="24" rx="6" fill="#b88a00"/><text x="229" y="158">AST07 · Update Drift</text>
    <rect x="414" y="110" width="171" height="24" rx="6" fill="#d9701b"/><text x="424" y="126">AST05 · External Instructions</text>
    <rect x="414" y="142" width="171" height="24" rx="6" fill="#d9701b"/><text x="424" y="158">AST03 · Over-Privileged</text>
    <rect x="609" y="110" width="171" height="24" rx="6" fill="#d9701b"/><text x="619" y="126">AST06 · Weak Isolation</text>
    <rect x="804" y="110" width="171" height="24" rx="6" fill="#b88a00"/><text x="814" y="126">AST08 · Poor Scanning</text>
    <rect x="804" y="142" width="171" height="24" rx="6" fill="#b88a00"/><text x="814" y="158">AST09 · No Governance</text>
    <rect x="804" y="174" width="171" height="24" rx="6" fill="#b88a00"/><text x="814" y="190">AST10 · Cross-Platform</text>
  </g>

  <g font-size="12" fill="#5b6675">
    <rect x="338" y="222" width="13" height="13" rx="3" fill="#c0252b"/><text x="357" y="233">Critical</text>
    <rect x="430" y="222" width="13" height="13" rx="3" fill="#d9701b"/><text x="449" y="233">High</text>
    <rect x="505" y="222" width="13" height="13" rx="3" fill="#b88a00"/><text x="524" y="233">Medium</text>
  </g>
</svg>
<div class="ast-figcap">The same skill can be attacked at multiple phases — these are the primary points where each risk lands.</div>
</div>

<div class="ast-legend">
  <span><i class="ast-dot crit"></i> Critical</span>
  <span><i class="ast-dot high"></i> High</span>
  <span><i class="ast-dot med"></i> Medium</span>
</div>

<div class="ast-grid">

<a class="ast-card crit" href="/www-project-agentic-skills-top-10/ast01.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8a4 4 0 0 1 4 4v2a4 4 0 0 1-8 0v-2a4 4 0 0 1 4-4z"/><path d="M10 8 8.5 6.5M14 8l1.5-1.5M8 12H4M20 12h-4M8 16l-2 1.5M16 16l2 1.5"/></svg></span>
    <span class="ast-id">AST01</span><span class="ast-pill crit">Critical</span>
  </div>
  <div class="ast-title">Malicious Skills</div>
  <div class="ast-desc">Skills that look legitimate but hide credential stealers, reverse shells, or prose instructions that hijack the agent.</div>
  <div class="ast-more">Read AST01 →</div>
</a>

<a class="ast-card crit" href="/www-project-agentic-skills-top-10/ast02.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 13.5a3.5 3.5 0 0 0 5 0l2-2a3.5 3.5 0 0 0-5-5l-1 1"/><path d="M13.5 10.5a3.5 3.5 0 0 0-5 0l-2 2a3.5 3.5 0 0 0 5 5l1-1"/></svg></span>
    <span class="ast-id">AST02</span><span class="ast-pill crit">Critical</span>
  </div>
  <div class="ast-title">Supply Chain Compromise</div>
  <div class="ast-desc">Registries without provenance let attackers mass-upload, take over accounts, and poison distribution channels.</div>
  <div class="ast-more">Read AST02 →</div>
</a>

<a class="ast-card high" href="/www-project-agentic-skills-top-10/ast03.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="12" r="3.2"/><path d="M11.2 12H20M17 12v3M20 12v2.5"/></svg></span>
    <span class="ast-id">AST03</span><span class="ast-pill high">High</span>
  </div>
  <div class="ast-title">Over-Privileged Skills</div>
  <div class="ast-desc">Skills granted far more access than they need — weaponisable by prompt injection into a huge blast radius.</div>
  <div class="ast-more">Read AST03 →</div>
</a>

<a class="ast-card high" href="/www-project-agentic-skills-top-10/ast04.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4h-7L3 14l7 7 10-10V4z"/><circle cx="16.3" cy="7.7" r="1.3"/></svg></span>
    <span class="ast-id">AST04</span><span class="ast-pill high">High</span>
  </div>
  <div class="ast-title">Insecure Metadata</div>
  <div class="ast-desc">Unvalidated, unsigned metadata enables brand impersonation, understated permissions, and poisoned search.</div>
  <div class="ast-more">Read AST04 →</div>
</a>

<a class="ast-card high" href="/www-project-agentic-skills-top-10/ast05.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 13v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h6"/></svg></span>
    <span class="ast-id">AST05</span><span class="ast-pill high">High</span>
  </div>
  <div class="ast-title">Untrusted External Instructions</div>
  <div class="ast-desc">Skills that point the agent at external docs trust mutable, unpinnable content that can be rug-pulled into malicious instructions.</div>
  <div class="ast-more">Read AST05 →</div>
</a>

<a class="ast-card high" href="/www-project-agentic-skills-top-10/ast06.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3"/><path d="M10.5 9l3 3-3 3"/></svg></span>
    <span class="ast-id">AST06</span><span class="ast-pill high">High</span>
  </div>
  <div class="ast-title">Weak Isolation</div>
  <div class="ast-desc">Skills run in the agent's full security context — with no sandbox, every skill is a potential full-system compromise.</div>
  <div class="ast-more">Read AST06 →</div>
</a>

<a class="ast-card med" href="/www-project-agentic-skills-top-10/ast07.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 0 1 13.7-5.6L20 8"/><path d="M20 4v4h-4"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 16"/><path d="M4 20v-4h4"/></svg></span>
    <span class="ast-id">AST07</span><span class="ast-pill med">Medium</span>
  </div>
  <div class="ast-title">Update Drift</div>
  <div class="ast-desc">Without pinning or verification, skills silently drift to vulnerable — or freshly malicious — versions.</div>
  <div class="ast-more">Read AST07 →</div>
</a>

<a class="ast-card med" href="/www-project-agentic-skills-top-10/ast08.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6"/><path d="M20 20l-3.8-3.8"/></svg></span>
    <span class="ast-id">AST08</span><span class="ast-pill med">Medium</span>
  </div>
  <div class="ast-title">Poor Scanning</div>
  <div class="ast-desc">Natural-language-plus-code blends defeat signature scanners, so malicious skills pass every automated check.</div>
  <div class="ast-more">Read AST08 →</div>
</a>

<a class="ast-card med" href="/www-project-agentic-skills-top-10/ast09.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg></span>
    <span class="ast-id">AST09</span><span class="ast-pill med">Medium</span>
  </div>
  <div class="ast-title">No Governance</div>
  <div class="ast-desc">No inventory, approval, audit, or revocation — a shadow-AI layer that security teams cannot see or control.</div>
  <div class="ast-more">Read AST09 →</div>
</a>

<a class="ast-card med" href="/www-project-agentic-skills-top-10/ast10.html">
  <div class="ast-top">
    <span class="ast-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="9" height="6" rx="1.2"/><rect x="12" y="13" width="9" height="6" rx="1.2"/><path d="M12 8h3.5a2 2 0 0 1 2 2v1.5M12 16H8.5a2 2 0 0 1-2-2v-1.5"/></svg></span>
    <span class="ast-id">AST10</span><span class="ast-pill med">Medium</span>
  </div>
  <div class="ast-title">Cross-Platform Reuse</div>
  <div class="ast-desc">Porting skills across platforms drops the source format's security metadata, opening exploitable gaps.</div>
  <div class="ast-more">Read AST10 →</div>
</a>

</div>
</div>

---

## Full details

Each risk has a dedicated page with attack scenarios, preventive mitigations, OWASP and MAESTRO mappings, and platform-specific guidance:

| # | Risk | Severity |
|---|------|----------|
| [AST01](ast01.md) | Malicious Skills | Critical |
| [AST02](ast02.md) | Supply Chain Compromise | Critical |
| [AST03](ast03.md) | Over-Privileged Skills | High |
| [AST04](ast04.md) | Insecure Metadata | High |
| [AST05](ast05.md) | Untrusted External Instructions | High |
| [AST06](ast06.md) | Weak Isolation | High |
| [AST07](ast07.md) | Update Drift | Medium |
| [AST08](ast08.md) | Poor Scanning | Medium |
| [AST09](ast09.md) | No Governance | Medium |
| [AST10](ast10.md) | Cross-Platform Reuse | Medium |

For the full project overview see the [home page](index.md); for a hands-on audit use the [security checklist](checklist.md).
