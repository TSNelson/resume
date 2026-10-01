# Resume operations

Operational notes that do not belong in the resume itself.

## Sources and builds

- **`resume.md` is the only content source.**
  - The front matter holds the header data: name, contact details, links, stack line, and PDF filename.
  - The body holds everything else.
- **`python build.py pdf`** writes `dist/Tor-Nelson-Resume.pdf`.
  - Print layout, US Letter, two pages.
  - Page 1 carries the header, the summary, and all of OnMission.
  - IBM Plex Sans is embedded, and the text layer is real and in reading order.
- **`python build.py site`** writes the Jekyll source to `dist/site/`:
  - `index.md`, which is `resume.md` copied verbatim. The layout reads the header data from its front matter.
  - `_config.yml` and `_layouts/default.html` from `site/`.
  - The built PDF. The page's "Download PDF" link points at this copy, so the page and its download always come from the same build. The file saves as `Tor Nelson - Resume.pdf`.
- **`python build.py all`** runs `pdf`, then `site`.
- **`python build.py check [--strict]`** runs the guards below.
- **Fonts** are vendored in `fonts/`: IBM Plex Sans latin 400/600, normal and italic, from `@fontsource/ibm-plex-sans` 5.3.0 (`npm pack`, then `package/files/`), plus `OFL.txt`. The build never fetches fonts.
- **Dependencies** are pinned in `requirements.txt`. WeasyPrint needs Pango, so build on Linux or in CI; native Windows isn't supported. `check` needs only `pypdf`, Markdown, and PyYAML, and runs anywhere.

Both media carry the same words. Formatting differs by medium:

- **Web:** the minimal theme's sidebar header, with links in their native form.
- **PDF:** a single-column print layout, with the stack line placed under the summary.

## Pipeline (`.github/workflows/publish.yml`)

`master` holds the sources. `dist/` is build output and is gitignored. Pages is served by the "GitHub Actions" source, not from a branch.

- **Preview loop:** push any branch other than `master`. CI builds, runs `check` (problems only warn), and uploads the `resume-preview` artifact with the PDF and the site source. Download it from the run page, or with `gh run download <run-id> -n resume-preview -D dist`. Nothing is published.
- **Publish loop:** merge to `master`. CI builds, runs `check --strict` (any problem fails the run), builds the Jekyll site, and deploys it to `https://tsnelson.github.io/resume/`.
- The build job is pinned to `ubuntu-24.04`, because the OS's Pango sets line breaks. Before moving it to a newer image, push a branch and compare the preview PDF with the last published one.
- The workflow runs only when `resume.md`, `build.py`, `requirements.txt`, `site/`, `fonts/`, or the workflow file changes. Use "Run workflow" to force a run.

### Guards (`build.py check`)

| Guard | Protects against |
|---|---|
| No `[URL…]`, `[TODO…]`, `[TBD…]`, or `{{` in the body | Shipping an unresolved placeholder. A stray `{{` would also be interpreted as Liquid on the web page. |
| Front matter has `name, location, phone, email, links, stack, pdf, title, layout`; every link is `https://` | A broken or partial header in either medium; insecure links |
| The PDF has 1–2 pages | Layout drift that spills onto a third page |
| The PDF text contains, in order: name, Experience, OnMission Systems, Prairie IT Services, Technical, Education | A missing or scrambled text layer, which breaks ATS parsing and copy-paste. Comparison ignores spacing and case, because the letter-spaced headings extract as `E X P E R I E N C E`. |
| Page 1 contains OnMission Systems; page 2 contains Prairie IT Services | "Page 1 carries OnMission" silently becoming false |
| `dist/site/index.md` starts with front matter; `dist/site/` contains the PDF | Publishing a page without its layout data, or with a dead download link |

### Rollback

- **Before the Pages source switch:** nothing is live, so there is nothing to roll back.
- **After the switch:** set `Settings → Pages → Source` back to branch `gh-pages`. The old site returns immediately, since that branch is untouched. Fix forward on `master`, then switch back.
- **Once the pipeline has been stable for a few publishes:** delete the `gh-pages` branch and remove this rollback path.

## Go-live checklist (Copybook launch, November 2026)

1. **Copybook link.** Replace the `[URL: Copybook link]` placeholder in the OnMission intro sentence in `resume.md`, push the branch, and confirm the preview.
2. **GitHub.** Clean up `github.com/TSNelson` before this version goes live, because the header now links to it.
   - Archive or make private the tutorial and old repositories.
   - Pin the resume repo and any agent skills that are public by then.
3. **Legacy PDF.** Delete `Tor Nelson - Resume.pdf` from the repo root on the branch (`git rm`). The page now serves its own copy, and nothing external links to the old one.
4. **Publish.** Switch `Settings → Pages → Source` to GitHub Actions, merge the branch, and do the LinkedIn update in the same session.
   - LinkedIn's headline should carry the market titles you want to be found under.
   - The About section should match this summary.

## Future swaps

- **Copybook v2 ships its MCP surface:** add an OnMission bullet stating what the surface exposes and to which clients, written from what actually shipped.
- **Docker or cloud infrastructure is used in real work:** add it to Infrastructure & operations. Coursework stays off the page.
- **ACAC is published on Substack:** consider naming and linking it in the method bullet.

## Retired: IT/infrastructure variant opening

This was the opening used on the live page through September 2026, tailored for an MSP-role ask. It is not for public use. If an IT or infrastructure req arrives, re-derive the opening against the current body; don't reuse this text as-is.

> **Automation and systems engineer.** Seven years building production automation and monitoring for a managed-services practice, implementing failure detection, self-healing remediation, and automated operations replacing manual administration across every client environment. For the last two years, the same reliability engineering discipline has guided the development of AI agent harnesses and the design of Human-AI collaboration systems, including a software development harness. The specification-first, review-gated system, with generated tests enforcing the behavioral contract, produced a production SaaS, now in final pre-launch. The through-line is: instrument the system, identify the failure modes, and build the machinery that increases reliability.

**Known error in that text:** it claims generated end-to-end tests. The suite is unit and integration tests. Correct this if the variant is ever re-derived.
