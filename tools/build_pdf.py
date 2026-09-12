#!/usr/bin/env python3
"""
Assemble the OWASP Agentic Skills Top 10 into a single professional PDF.

Structure:
  - Cover page (OWASP logo, title, version, license)
  - Executive summary (+ the 10-risk reference table)
  - Acknowledgements (project lead + co-leaders + contributors)
  - Table of contents (with page numbers)
  - AST01-AST10, each rendered in full from its astNN.md source file

Rendering: Markdown -> HTML (python-markdown) -> PDF (WeasyPrint).

Usage:
  python tools/build_pdf.py [--out dist/OWASP-Agentic-Skills-Top10.pdf]
"""
import argparse
import base64
import datetime
import os
import re

import markdown as md
from weasyprint import HTML

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEV_COLOR = {"Critical": "#c0252b", "High": "#d9701b", "Medium": "#b88a00", "Low": "#b88a00"}
NAVY = "#13395c"

VERSION = "v0.5"
PROJECT_LEAD = "Ken Huang"
CO_LEADERS = ["Akram Sheriff", "Aonan Guan", "Bhavya Gupta",
              "Fabio Cerullo", "Hammad Atta", "Iftach Orr"]

# Compact reference table for the executive summary.
RISK_TABLE = [
    ("AST01", "Malicious Skills", "Critical", "Signing, registry scanning"),
    ("AST02", "Supply Chain Compromise", "Critical", "Provenance, transparency logs"),
    ("AST03", "Over-Privileged Skills", "High", "Least-privilege manifests"),
    ("AST04", "Insecure Metadata", "High", "Static analysis, manifest linting"),
    ("AST05", "Unsafe Deserialization", "High", "Safe parsers, sandboxed loading"),
    ("AST06", "Weak Isolation", "High", "Containerization, sandboxing"),
    ("AST07", "Update Drift", "Medium", "Immutable pinning, hash verification"),
    ("AST08", "Poor Scanning", "Medium", "Behavioral + semantic scanning"),
    ("AST09", "No Governance", "Medium", "Inventory, audit, identity controls"),
    ("AST10", "Cross-Platform Reuse", "Medium", "Universal format, re-validation"),
]


def data_uri(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"


def parse_ast(path):
    txt = open(path, encoding="utf-8").read()
    fm = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    body = txt[fm.end():] if fm else txt
    title = re.search(r"^title:\s*(.+)$", fm.group(1), re.M) if fm else None
    title = title.group(1).strip().strip('"') if title else os.path.basename(path)
    m = re.match(r"(AST\d+)\s*[—\-:]\s*(.+)", title)
    ast_id, name = (m.group(1), m.group(2).strip()) if m else (title[:5], title)
    sev = re.search(r"\*\*Severity\*\*:\s*([A-Za-z]+)", body)
    sev = sev.group(1) if sev else "Medium"
    return ast_id, name, sev, body.strip()


def fix_links(text):
    # internal cross-references to other AST chapters -> anchors
    text = re.sub(r"\]\(\.?/?(ast\d+)\.md(#[^)]*)?\)", r"](#\1\2)", text, flags=re.I)
    # other repo .md pages -> absolute owasp.org links
    text = re.sub(r"\]\(\.?/?([a-z0-9][a-z0-9-]*)\.md(#[^)]*)?\)",
                  r"](https://owasp.org/www-project-agentic-skills-top-10/\1\2)", text)
    return text


def md2html(text):
    return md.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])


def severity_badge(sev):
    return f'<span class="badge" style="background:{SEV_COLOR.get(sev, NAVY)}">{sev.upper()}</span>'


def build_html(risks, logo):
    today = os.environ.get("BUILD_DATE") or datetime.date.today().strftime("%B %Y")

    # ----- cover -----
    cover = f"""
    <section class="cover">
      <img class="cover-logo" src="{logo}" alt="OWASP"/>
      <div class="cover-kicker">OWASP &middot; Incubator Project</div>
      <h1 class="cover-title">Agentic Skills Top&nbsp;10</h1>
      <div class="cover-sub">The 10 most critical security risks for AI agent skills &mdash;
        and how to mitigate them</div>
      <div class="cover-rule"></div>
      <div class="cover-meta">
        {VERSION} &nbsp;&middot;&nbsp; {today}<br/>
        Licensed under CC BY-SA 4.0<br/>
        owasp.org/www-project-agentic-skills-top-10
      </div>
    </section>"""

    # ----- executive summary -----
    rows = ""
    for rid, name, sev, mit in RISK_TABLE:
        rows += (f'<tr><td class="rid">{rid}</td><td>{name}</td>'
                 f'<td>{severity_badge(sev)}</td><td>{mit}</td></tr>')
    exec_summary = f"""
    <section class="page">
      <h1 class="sec-h">Executive summary</h1>
      <p>Agent <em>skills</em> are the behaviour layer of modern AI agents: reusable units
      that tell an agent what to do and grant it the tools to do it. While the industry has
      focused on securing large language models and the Model Context Protocol (MCP) tool
      layer, the skill layer in between has become a fast-growing and under-protected attack
      surface. Skills execute with the host agent's full privileges, blend natural-language
      instructions with executable code, and are distributed through registries that largely
      lack the provenance controls of mature package ecosystems.</p>
      <p>The consequences are already visible in the wild: coordinated malicious-skill
      campaigns, credential-leaking skills, registry compromise, and prompt-injection-driven
      privilege abuse. This document catalogues the ten most critical risks, each with
      attack scenarios, preventive mitigations, and mappings to OWASP and the CSA MAESTRO
      framework.</p>
      <p>The ten risks span the full skill lifecycle &mdash; authoring, publishing,
      distribution, installation, loading, execution, and governance. Two are rated
      <strong>Critical</strong>, four <strong>High</strong>, and four <strong>Medium</strong>.
      No single control is sufficient; effective defence composes signing, provenance,
      least-privilege manifests, sandboxing, scanning, and governance.</p>
      <table class="risk-table">
        <thead><tr><th>#</th><th>Risk</th><th>Severity</th><th>Key mitigation</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>"""

    # ----- acknowledgements -----
    coleads = "".join(f"<li>{n}</li>" for n in CO_LEADERS)
    acks = f"""
    <section class="page">
      <h1 class="sec-h">Acknowledgements</h1>
      <p>This document is the work of the OWASP Agentic Skills Top&nbsp;10 project leadership
      and the wider OWASP community. We are grateful to the project lead and co-leaders for
      their research, writing, and stewardship.</p>
      <div class="ack-block">
        <h3>Project lead</h3>
        <ul class="ack-list"><li>{PROJECT_LEAD}</li></ul>
        <h3>Co-leaders</h3>
        <ul class="ack-list cols">{coleads}</ul>
      </div>
      <p>Our thanks also go to every contributor who submitted issues, pull requests,
      real-world evidence, code examples, and reviews &mdash; and to the security researchers
      whose published work this document builds on. Contributions are welcome at
      <strong>owasp.org/www-project-agentic-skills-top-10</strong>.</p>
    </section>"""

    # ----- table of contents -----
    toc_items = ""
    for rid, name, sev, _ in RISK_TABLE:
        dot = SEV_COLOR.get(sev, NAVY)
        toc_items += (f'<li><span class="toc-dot" style="background:{dot}"></span>'
                      f'<a href="#{rid.lower()}">{rid} &mdash; {name}</a></li>')
    toc = f"""
    <section class="page">
      <h1 class="sec-h">Contents</h1>
      <ul class="toc">{toc_items}</ul>
    </section>"""

    # ----- per-risk chapters -----
    chapters = ""
    for rid, name, sev, body in risks:
        html_body = md2html(fix_links(body))
        chapters += f"""
        <section class="chapter sev" id="{rid.lower()}" style="--sev:{SEV_COLOR.get(sev, NAVY)}">
          <div class="chapter-head">
            <div class="chapter-id">{rid}</div>
            <h1 class="chapter-title">{name}</h1>
            {severity_badge(sev)}
          </div>
          {html_body}
        </section>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"/>
<style>{CSS}</style></head>
<body>{cover}{exec_summary}{acks}{toc}{chapters}</body></html>"""


CSS = r"""
@page {
  size: A4;
  margin: 2.1cm 1.8cm 1.9cm;
  @top-right { content: "OWASP Agentic Skills Top 10"; font-size: 8pt; color: #9aa3b0; }
  @bottom-center { content: counter(page); font-size: 9pt; color: #6b7280; }
  @bottom-right { content: "owasp.org/www-project-agentic-skills-top-10";
                  font-size: 7pt; color: #b6bdc8; }
}
@page cover { margin: 0;
  @top-right { content: normal; } @bottom-center { content: normal; }
  @bottom-right { content: normal; } }

* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", "Helvetica Neue", Arial, sans-serif;
  color: #1f2937; font-size: 10.2pt; line-height: 1.5; }
h1, h2, h3 { color: #13395c; line-height: 1.25; }
a { color: #13395c; text-decoration: none; }
code, pre { font-family: "DejaVu Sans Mono", Consolas, monospace; }
p { margin: .5em 0; }

/* cover */
.cover { page: cover; height: 297mm; padding: 34mm 26mm; position: relative;
  border-top: 14mm solid #13395c; }
.cover-logo { height: 17mm; margin-top: 6mm; }
.cover-kicker { margin-top: 40mm; letter-spacing: .22em; text-transform: uppercase;
  font-size: 10pt; color: #d9701b; font-weight: 700; }
.cover-title { font-size: 40pt; margin: 4mm 0 0; color: #13395c; line-height: 1.05; }
.cover-sub { font-size: 14pt; color: #5b6675; margin-top: 6mm; max-width: 150mm; }
.cover-rule { width: 60mm; height: 4px; background: #c0252b; margin: 12mm 0; }
.cover-meta { position: absolute; bottom: 26mm; font-size: 10.5pt; color: #5b6675;
  line-height: 1.7; }

/* generic front-matter pages */
.page { page-break-before: always; }
.sec-h { font-size: 22pt; border-bottom: 2px solid #e3e7ee; padding-bottom: 3mm;
  margin: 0 0 6mm; }

/* exec summary table */
.risk-table { width: 100%; border-collapse: collapse; margin-top: 6mm; font-size: 9.4pt; }
.risk-table th { background: #13395c; color: #fff; text-align: left; padding: 5px 8px; }
.risk-table td { border-bottom: .5px solid #e3e7ee; padding: 5px 8px; vertical-align: middle; }
.risk-table td.rid { font-weight: 700; color: #13395c; white-space: nowrap; }
.badge { color: #fff; font-size: 7.4pt; font-weight: 700; letter-spacing: .04em;
  padding: 2px 7px; border-radius: 9px; }

/* acknowledgements */
.ack-block { margin: 5mm 0; }
.ack-list { list-style: none; padding: 0; margin: 2mm 0 6mm; }
.ack-list li { padding: 2px 0; font-size: 11pt; }
.ack-list.cols { column-count: 2; }
.ack-block h3 { margin: 4mm 0 1mm; font-size: 12pt; color: #d9701b; }

/* table of contents */
.toc { list-style: none; padding: 0; font-size: 11.5pt; }
.toc li { padding: 2.4mm 0; border-bottom: .5px dotted #d8dee8; }
.toc-dot { display: inline-block; width: 9px; height: 9px; border-radius: 2px;
  margin-right: 8px; vertical-align: middle; }
.toc a::after { content: " " leader('.') " " target-counter(attr(href), page);
  color: #5b6675; }

/* chapters */
.chapter { page-break-before: always; }
.chapter-head { border-left: 5px solid var(--sev); padding: 1mm 0 3mm 5mm;
  margin-bottom: 5mm; }
.chapter-id { font-size: 11pt; font-weight: 700; letter-spacing: .1em; color: var(--sev); }
.chapter-title { font-size: 25pt; margin: 1mm 0 2mm; }
.chapter h2 { font-size: 14pt; margin: 6mm 0 2mm; border-bottom: 1px solid #eef1f5;
  padding-bottom: 1.5mm; }
.chapter h3 { font-size: 11.5pt; margin: 4mm 0 1mm; color: #1f2937; }
.chapter table { width: 100%; border-collapse: collapse; margin: 3mm 0; font-size: 9pt; }
.chapter th { background: #f1f4f9; text-align: left; padding: 4px 7px;
  border: .5px solid #e3e7ee; }
.chapter td { padding: 4px 7px; border: .5px solid #e3e7ee; vertical-align: top; }
.chapter pre { background: #f6f8fa; border: .5px solid #e3e7ee; border-radius: 5px;
  padding: 7px 9px; font-size: 8.2pt; line-height: 1.4; white-space: pre-wrap;
  word-wrap: break-word; }
.chapter code { background: #f1f4f9; padding: 1px 4px; border-radius: 3px; font-size: 9pt; }
.chapter pre code { background: none; padding: 0; }
.chapter hr { border: none; border-top: 1px solid #e3e7ee; margin: 5mm 0; }
.chapter ul, .chapter ol { margin: 2mm 0 2mm 5mm; }
.chapter li { margin: 1mm 0; }
"""


def build(out_path):
    logo_path = os.path.join(REPO, "assets", "images", "owasp-logo.png")
    logo = data_uri(logo_path) if os.path.exists(logo_path) else ""

    risks = []
    for i in range(1, 11):
        p = os.path.join(REPO, f"ast{i:02d}.md")
        if os.path.exists(p):
            risks.append(parse_ast(p))
    assert len(risks) == 10, f"expected 10 AST files, found {len(risks)}"

    html = build_html(risks, logo)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    HTML(string=html, base_url=REPO).write_pdf(out_path)
    print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes)")


def main():
    global VERSION
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "dist", "OWASP-Agentic-Skills-Top10.pdf"))
    ap.add_argument("--doc-version", dest="ver", default=VERSION)
    args = ap.parse_args()
    VERSION = args.ver
    build(args.out)


if __name__ == "__main__":
    main()
