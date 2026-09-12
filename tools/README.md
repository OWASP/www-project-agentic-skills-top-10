# Tools

## `build_pptx.py` — Top 10 slide deck generator

Builds a professional **12-slide** PowerPoint deck for the OWASP Agentic Skills
Top 10:

1. **Overview** — all ten risks on one slide, colour-coded by severity.
2. **AST01–AST10** — one slide per risk, with an *issues → mitigations* diagram.
3. **Summary** — severity distribution and key takeaways.

The OWASP logo (`assets/images/owasp-logo.png`) appears on every slide.

Content is parsed live from the `astNN.md` source files (severity, description,
attack scenarios, preventive mitigations), so the deck stays in sync with the
documentation.

### Build locally

```bash
pip install "python-pptx==1.0.2" "Pillow>=10,<14"
python tools/build_pptx.py --out dist/OWASP-Agentic-Skills-Top10.pptx
```

### Build in CI

The [`Build Top 10 PPTX`](../.github/workflows/build-pptx.yml) workflow runs on:

- any push to `main` that touches `ast*.md`, the generator, the logo, or the
  workflow itself;
- a manual **Run workflow** (`workflow_dispatch`);
- a published **Release** (the deck is attached to the release assets).

Every run uploads the deck as the **`OWASP-Agentic-Skills-Top10-pptx`** artifact,
downloadable from the workflow run's *Artifacts* section.

## `build_pdf.py` — full Top 10 PDF document

Assembles the entire Top 10 into a single professional PDF:

1. **Cover page** — OWASP logo, title, version, licence.
2. **Executive summary** — narrative plus the 10-risk reference table.
3. **Acknowledgements** — project lead and co-leaders.
4. **Table of contents** — with page numbers.
5. **AST01–AST10** — each chapter rendered in full from its `astNN.md` file.

Rendering: Markdown → HTML (`python-markdown`) → PDF (`WeasyPrint`).

### Build locally

```bash
# system libraries (Debian/Ubuntu): libpango, cairo, gdk-pixbuf, dejavu fonts
pip install "weasyprint==69.0" "markdown>=3.6,<4"
python tools/build_pdf.py --out dist/OWASP-Agentic-Skills-Top10.pdf
```

### Build in CI

The [`Build Top 10 PDF`](../.github/workflows/build-pdf.yml) workflow runs on the
same triggers as the deck workflow (push to `main`, manual dispatch, release) and
uploads the **`OWASP-Agentic-Skills-Top10-pdf`** artifact; releases also get the
PDF attached as an asset.

## Versioned releases

Both generators carry a document version (`VERSION`, currently **v0.5**), shown on
the PDF cover and in the deck footer. Override it with `--doc-version`:

```bash
python tools/build_pdf.py  --doc-version v0.6 --out dist/OWASP-Agentic-Skills-Top10-v0.6.pdf
python tools/build_pptx.py --doc-version v0.6 --out dist/OWASP-Agentic-Skills-Top10-v0.6.pptx
```

For the v1 publication cycle, the merged draft is reviewed in Google Docs and
generated PDF/PPTX snapshots should not be committed to `docs/`. The generators
remain available for local drafts, release automation, or future publication
workflows after the v1 review process returns to repository-managed artifacts.
