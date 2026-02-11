# CLI Documentation Auto-Generation: Research and Recommendation

## Executive Statement

**Objective:** Replace the manually-maintained "Formal CLI docs" section in the README with auto-generated documentation produced in a GitHub Actions workflow and uploaded as an artifact.

**Functional Requirements:**

- FR1: Generate documentation from the Click CLI defined in `cc_news_analyzer/cli.py` (root group `cli` with commands `count-records`, `get-index`, `get-warc`)
- FR2: Output should be Markdown or plain text (no HTML site needed)
- FR3: Run as a step in GitHub Actions (no interactive input)
- FR4: Minimal dependency footprint -- a well-maintained library is preferred over DIY, but zero-dependency DIY is acceptable
- FR5: Future upgrade path to GitHub Pages is desirable but not required now

**Stakeholder Answers:**

- Format: Either plain text or Markdown -- simplest solution preferred
- Dependency: Prefers a library, but ultimately chose the DIY approach for zero-dependency simplicity

---

## Table of Contents

1. [click-man](#1-click-man)
2. [sphinx-click](#2-sphinx-click)
3. [md-click](#3-md-click)
4. [mkdocs-click](#4-mkdocs-click)
5. [DIY (Click introspection script)](#5-diy-click-introspection-script)
6. [Summary and Recommendation](#summary)

---

## 1. click-man

Generates **man pages** (roff/troff format) from Click CLI apps. One man page per command.

- **Meets FR1:** Yes -- walks Click command tree automatically
- **Meets FR2:** No -- outputs man page (roff) format, not Markdown or plain text. Can be rendered via `man`, but not directly readable as `.md`
- **Meets FR3:** Yes -- CLI command, easy to run in CI
- **Meets FR4:** Yes -- single dependency
- **Meets FR5:** No -- man pages don't translate to GitHub Pages

**Stability and Adoption:**

- GitHub: 203 stars, 43 forks (click-contrib/click-man)
- PyPI: v0.5.1 (Apr 2025), ~1,400 downloads/week, ~8,572/month
- License: MIT
- Active maintenance: Yes, recent releases
- Known issues: Man page formatting broken on Debian 12 (#59); non-portable blank lines (#11)

**Verdict: REJECT** -- Output format (roff) does not match the requirement for Markdown or plain text.

---

## 2. sphinx-click

Sphinx extension that auto-documents Click apps via a `.. click::` directive.

- **Meets FR1:** Yes -- walks command tree, documents all options/arguments
- **Meets FR2:** Partial -- generates reStructuredText for Sphinx, which then renders to HTML. Does not produce standalone Markdown
- **Meets FR3:** Yes -- can run in CI
- **Meets FR4:** No -- heavyweight. Requires Sphinx + sphinx-click + RST/conf.py setup
- **Meets FR5:** Yes -- excellent for GitHub Pages later

**Stability and Adoption:**

- GitHub: 220 stars, 59 forks (click-contrib/sphinx-click)
- PyPI: v6.2.0 (Dec 2025), ~134,465 downloads/week, ~509,538/month
- License: MIT
- Active maintenance: Yes, very active
- Backed by the click-contrib org

**Verdict: REJECT** -- Overkill for the current need. Requires Sphinx infrastructure for what is currently a "just give me markdown" requirement. Good future candidate if the project later needs a full docs site.

---

## 3. md-click

CLI tool that walks a Click app and generates one `.md` file per command/subcommand.

- **Meets FR1:** Yes -- walks command tree recursively
- **Meets FR2:** Yes -- generates Markdown files directly
- **Meets FR3:** Yes -- CLI command, easy to run in CI
- **Meets FR4:** Concern -- single dependency, but abandoned
- **Meets FR5:** Yes -- Markdown files can serve as GitHub Pages source

**Stability and Adoption:**

- GitHub: 12 stars, 14 forks (RiveryIO/md-click)
- PyPI: v1.0.1 (Mar 2021) -- **no updates in ~5 years**
- License: BSD-3
- Active maintenance: **No** -- last release was 2021, no recent commits
- Built on Python 3.8-era tooling

**Verdict: REJECT** -- Project is effectively abandoned. Only 12 stars, no updates since 2021. Risk of breaking with newer Click or Python versions.

---

## 4. mkdocs-click

MkDocs Markdown extension that generates documentation for Click apps inline within MkDocs pages.

- **Meets FR1:** Yes -- walks command tree, documents everything
- **Meets FR2:** Yes -- generates Markdown (designed for it)
- **Meets FR3:** Yes -- can run in CI via `mkdocs build`
- **Meets FR4:** Partial -- requires MkDocs infrastructure (mkdocs.yml, docs/ folder, theme), but lighter than Sphinx
- **Meets FR5:** Yes -- excellent GitHub Pages path (mkdocs gh-deploy)

**Stability and Adoption:**

- GitHub: 148 stars, 21 forks (mkdocs/mkdocs-click) -- under the official mkdocs org
- PyPI: v0.9.0 (Apr 2025)
- License: Apache-2.0
- Active maintenance: Yes
- Originally developed by Datadog, now maintained under the mkdocs org
- Style options: `plain` (header-based) or `table` (tabular options)

**Verdict: FINALIST** -- Best library option if you want structured Markdown and a clear path to GitHub Pages. However, it requires the MkDocs framework even if you just want a Markdown file, which adds more infrastructure than strictly needed right now.

---

## 5. DIY: Click Introspection Script

A small (~40-50 line) Python script that uses Click's built-in `get_help(ctx)` method to walk the command tree and emit the help text for every command. Output can be plain text or formatted as Markdown.

```python
# Example: generate_docs.py
import click
from cc_news_analyzer.cli import cli

def dump_help(cmd, ctx_parent=None, prog_name="cc-news"):
    ctx = click.Context(cmd, info_name=prog_name, parent=ctx_parent)
    print(cmd.get_help(ctx))
    print()
    if hasattr(cmd, "commands"):
        for name in sorted(cmd.commands):
            sub = cmd.commands[name]
            dump_help(sub, ctx, name)

if __name__ == "__main__":
    dump_help(cli)
```

- **Meets FR1:** Yes -- full control over traversal
- **Meets FR2:** Yes -- outputs plain text (--help style) or can be enhanced to Markdown
- **Meets FR3:** Yes -- just `python generate_docs.py > docs.md`
- **Meets FR4:** No new dependency -- but you own the code
- **Meets FR5:** Partial -- plain text artifact; would need rework for GitHub Pages

**Stability and Adoption:**

- N/A (custom code)
- Pattern is well-documented: [StackOverflow](https://stackoverflow.com/questions/57810659), Simon Willison's [help-scraping](https://simonwillison.net/2022/Feb/2/help-scraping)
- Zero dependency risk

**Verdict: FINALIST** -- Simplest approach with zero dependencies. Aligns well with "I would even settle for text only docs." Downside: you own the code and it won't auto-detect new command options without the script being correct (though Click's `get_help()` handles this natively).

---

## Summary

| Candidate    | Format           | Deps            | Maintained          | Stars | Verdict               |
| ------------ | ---------------- | --------------- | ------------------- | ----- | --------------------- |
| click-man    | roff (man pages) | 1               | Yes                 | 203   | REJECT (wrong format) |
| sphinx-click | RST/HTML         | Heavy (Sphinx)  | Yes                 | 220   | REJECT (overkill)     |
| md-click     | Markdown         | 1               | **No** (since 2021) | 12    | REJECT (abandoned)    |
| mkdocs-click | Markdown         | Medium (MkDocs) | Yes                 | 148   | FINALIST              |
| DIY script   | Text/Markdown    | 0               | N/A                 | N/A   | FINALIST              |

---

## Final Recommendation: DIY Click Introspection Script

The custom script approach is the best fit for this project's current stage:

- **Zero new dependencies** -- uses only Click's built-in `click.Context` and `get_help()` API, which is already a project dependency
- **Full control** over output format -- can produce plain text (`--help` style) or Markdown with headers, code blocks, and parameter tables
- **Trivially simple** -- ~40-50 lines of Python that walk the command tree recursively
- **Automatically picks up new commands** -- any new `@cli.command()` is discovered at runtime via `cmd.commands`
- **Easy CI integration** -- `python -m cc_news_analyzer.generate_docs > cli-reference.md`
- **Future upgrade path** -- if the project later needs a full docs site, the script's Markdown output can be fed directly into MkDocs or Sphinx with minimal rework

**Trade-off:** You own the code (~40-50 lines). If Click changes its introspection API (unlikely -- `get_help()` has been stable for years), you'd need to update the script. This is a very low risk.
