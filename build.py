#!/usr/bin/env python3
"""Render resume.md to both media from one content source, and guard the result.

    python build.py pdf              -> dist/<pdf>  (print layout)
    python build.py site             -> dist/site/  (Jekyll source: index.md, layout, config, PDF)
    python build.py all              -> pdf, then site
    python build.py check [--strict] -> guards; --strict fails the build, otherwise warns

Content lives only in resume.md (front matter = header data, body = everything
else). Formatting lives only here and in the layout: same words, per-medium form.
"""
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml

HERE = Path(__file__).parent
SRC = HERE / "resume.md"
DIST = HERE / "dist"
SITE_SRC = HERE / "site"
FONT_DIR = HERE / "fonts"

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
PLACEHOLDER = re.compile(r"\[(URL|TODO|TBD)[^\]]*\]|\{\{")
REQUIRED_KEYS = ["name", "location", "phone", "email", "links", "stack", "pdf", "title", "layout"]


def load():
    text = SRC.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        sys.exit("resume.md: missing front matter")
    return yaml.safe_load(m.group(1)), m.group(2)


# ---------------------------------------------------------------- PDF --

PRINT_CSS = """
@font-face { font-family: Plex; font-weight: 400; font-style: normal; src: url('{fd}/ibm-plex-sans-latin-400-normal.woff2'); }
@font-face { font-family: Plex; font-weight: 400; font-style: italic; src: url('{fd}/ibm-plex-sans-latin-400-italic.woff2'); }
@font-face { font-family: Plex; font-weight: 600; font-style: normal; src: url('{fd}/ibm-plex-sans-latin-600-normal.woff2'); }
@font-face { font-family: Plex; font-weight: 600; font-style: italic; src: url('{fd}/ibm-plex-sans-latin-600-italic.woff2'); }

@page {
  size: letter;
  margin: 0.55in 0.68in 0.6in 0.68in;
  @bottom-right {
    content: "Tor Nelson · " counter(page) " of " counter(pages);
    font-family: Plex; font-size: 7.5pt; color: #8a8f94;
  }
}
@page :first { @bottom-right { content: none; } }

:root { --ink: #1b1d1f; --muted: #5b6168; --accent: #1f4b6e; --rule: #c9ced3; }
html { font-family: Plex, sans-serif; font-size: 9.8pt; line-height: 1.4; color: var(--ink); }
body { margin: 0; }
a { color: inherit; text-decoration: none; }
strong { font-weight: 600; }

header { margin-bottom: 9pt; }
header h1 { font-size: 21pt; font-weight: 600; letter-spacing: -0.01em; color: var(--accent); margin: 0 0 2pt 0; line-height: 1.1; }
header .contact { font-size: 8.8pt; color: var(--muted); margin: 0; }
header .contact span.item { white-space: nowrap; }
header .contact .sep { margin: 0 4pt; color: var(--rule); }

.summary p { margin: 0 0 5pt 0; }
.stack { font-size: 8.6pt; color: var(--muted); margin: 0 0 4pt 0; }
.stack strong { color: var(--ink); }

h2 {
  font-size: 8.4pt; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--accent); border-bottom: 0.6pt solid var(--rule);
  padding-bottom: 2pt; margin: 12pt 0 6pt 0;
  break-after: avoid;
}
h3 { font-size: 10.3pt; font-weight: 600; margin: 9pt 0 0 0; break-after: avoid; }
h3 em { font-weight: 400; font-style: normal; color: var(--muted); font-size: 9pt; }
p.meta { font-size: 8.6pt; color: var(--muted); margin: 0 0 4pt 0; break-after: avoid; }
p.meta strong { font-weight: 400; }
p { margin: 0 0 4pt 0; orphans: 3; widows: 3; }
p.intro { break-inside: avoid; }

ul { margin: 3pt 0 0 0; padding-left: 11pt; }
li { margin: 0 0 3.2pt 0; break-inside: avoid; }
li::marker { color: var(--accent); }

.technical p { margin: 0 0 3pt 0; }
"""


def pdf(meta, body):
    from weasyprint import HTML  # imported here so `site` and `check` work without it

    # Body -> HTML; the date line directly under each role becomes .meta.
    html_body = markdown.markdown(body, extensions=["sane_lists"])
    html_body = re.sub(r"</h3>\s*<p>", '</h3>\n<p class="meta">', html_body)
    # The role's intro paragraph travels with its heading, never split from it.
    html_body = re.sub(r'(<p class="meta">.*?</p>)\s*<p>', r'\1\n<p class="intro">', html_body)

    # Split: summary (before first h2) | sections. Wrap Technical for its own spacing.
    first_h2 = html_body.index("<h2>")
    summary, rest = html_body[:first_h2], html_body[first_h2:]
    rest = re.sub(r"(<h2>Technical</h2>)(.*?)(?=<h2>)", r'<div class="technical">\1\2</div>', rest, flags=re.S)

    sep = '<span class="sep">·</span>'
    item = lambda x: f'<span class="item">{x}</span>'
    line1 = sep.join(item(x) for x in
        [meta["location"], meta["phone"], f'<a href="mailto:{meta["email"]}">{meta["email"]}</a>'])
    line2 = sep.join(item(f'<a href="{l["url"]}">{l["text"]}</a>') for l in meta["links"])
    contact = f"{line1}<br>{line2}"
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{meta['title']}</title>
<meta name="author" content="{meta['name']}">
<style>{PRINT_CSS.replace('{fd}', FONT_DIR.as_uri())}</style></head><body>
<header><h1>{meta['name']}</h1><p class="contact">{contact}</p></header>
<section class="summary">{summary}<p class="stack"><strong>Working stack:</strong> {meta['stack']}</p></section>
{rest}
</body></html>"""
    DIST.mkdir(exist_ok=True)
    out = DIST / meta["pdf"]
    HTML(string=doc, base_url=str(HERE)).write_pdf(out)
    print(f"wrote {out}")


# --------------------------------------------------------------- SITE --

def site(meta, body):
    built_pdf = DIST / meta["pdf"]
    if not built_pdf.exists():
        sys.exit(f"{built_pdf} not built; run `python build.py pdf` first")
    out = DIST / "site"
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(SITE_SRC, out)  # _config.yml, _layouts/default.html
    # The page is the source itself: same file, same words.
    shutil.copy(SRC, out / "index.md")
    # The PDF ships with the page, so the download always matches it.
    shutil.copy(built_pdf, out / built_pdf.name)
    print(f"wrote {out}/ (index.md, _config.yml, _layouts/default.html, {built_pdf.name})")


# -------------------------------------------------------------- CHECK --

def squash(text):
    """PDF text without whitespace, casefolded: letter-spaced headings extract as
    'E X P E R I E N C E', so compare on content, not spacing or case."""
    return re.sub(r"\s+", "", text).casefold()


def check(strict):
    from pypdf import PdfReader

    problems = []
    text = SRC.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(text)
    if not m:
        problems.append("resume.md: missing front matter")
        meta, body, body_line = {}, text, 1
    else:
        meta, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
        body_line = text[:m.start(2)].count("\n") + 1

    # Placeholders: nothing unresolved ships, and a stray {{ would be Liquid on the web page.
    for i, line in enumerate(body.split("\n"), start=body_line):
        for hit in PLACEHOLDER.finditer(line):
            problems.append(f"resume.md:{i}: unresolved placeholder {hit.group(0)!r}")

    # Front matter: both media read the header from it.
    missing = [k for k in REQUIRED_KEYS if not meta.get(k)]
    if missing:
        problems.append(f"resume.md: front matter missing {', '.join(missing)}")
    for link in meta.get("links") or []:
        url = (link or {}).get("url", "")
        if not url.startswith("https://"):
            problems.append(f"resume.md: link {url!r} is not https://")

    # PDF: length, a real text layer in reading order, and page 1 carrying OnMission.
    pdf_name = meta.get("pdf")
    built_pdf = DIST / pdf_name if pdf_name else None
    if not built_pdf or not built_pdf.exists():
        problems.append(f"dist/{pdf_name or '<pdf>'}: PDF not built")
    else:
        pages = [squash(p.extract_text() or "") for p in PdfReader(built_pdf).pages]
        if not 1 <= len(pages) <= 2:
            problems.append(f"{built_pdf.name}: {len(pages)} pages, expected 1-2")
        whole, pos = "".join(pages), 0
        for marker in [meta.get("name", ""), "Experience", "OnMission Systems",
                       "Prairie IT Services", "Technical", "Education"]:
            found = whole.find(squash(marker), pos)
            if not marker or found < 0:
                problems.append(f"{built_pdf.name}: text layer missing {marker!r} in reading order")
                break
            pos = found + 1
        if pages and "onmissionsystems" not in pages[0]:
            problems.append(f"{built_pdf.name}: page 1 does not contain 'OnMission Systems'")
        if len(pages) >= 2 and "prairieitservices" not in pages[1]:
            problems.append(f"{built_pdf.name}: page 2 does not contain 'Prairie IT Services'")

    # Site: the Jekyll source is complete and the page has front matter.
    index = DIST / "site" / "index.md"
    if not index.exists() or not index.read_text(encoding="utf-8").startswith("---\n"):
        problems.append("dist/site/index.md: missing or does not start with front matter")
    if not pdf_name or not (DIST / "site" / pdf_name).exists():
        problems.append(f"dist/site/{pdf_name}: PDF missing from site")

    level = "error" if strict else "warning"
    for p in problems:
        print(f"::{level}::{p}")
    print(f"check{' --strict' if strict else ''}: {len(problems)} problem(s)")
    return 1 if problems and strict else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    target = args[0] if args else "all"
    if target == "check":
        sys.exit(check(strict="--strict" in args[1:]))
    if target not in ("pdf", "site", "all"):
        sys.exit("usage: build.py [pdf|site|all|check [--strict]]")
    meta, body = load()
    if target in ("pdf", "all"):
        pdf(meta, body)
    if target in ("site", "all"):
        site(meta, body)
