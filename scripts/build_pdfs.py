#!/usr/bin/env python3
"""Build public PDF (and web view for plain guides) from the Markdown/QMD sources.

pandoc -> standalone print HTML (print.css) -> WeasyPrint PDF.
Quarto pages already get a WEB view from `quarto render`; plain .md guides get
their HTML view written next to the source so the site can serve it.

Run from repo root, then `python3 scripts/build_downloads.py && quarto render`.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "scripts" / "print.css"

# (source, also write a public web view?)
DOCS = [
    ("lore_and_narrative_bible.qmd", False),
    ("broadcast_scripts_and_liturgy.qmd", False),
    ("quest_cards_and_facilitator_pack.qmd", False),
    ("game_design_and_activities.qmd", False),
    ("passport_production_guide.md", True),
    ("BITLAIR_PROP_FABRICATION_GUIDE.md", True),
]


def strip_quarto_format(text: str) -> str:
    """Drop the `format:` block from YAML front matter (pandoc doesn't need it)."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return text
    yaml = re.sub(r"^format:\n(?:[ \t]+.*\n?)*", "", m.group(1) + "\n", flags=re.M)
    return f"---\n{yaml.rstrip()}\n---\n" + text[m.end():]


def convert_callouts(text: str) -> str:
    """Turn Quarto callout fences into a pandoc-friendly styled div, keeping the title."""
    def repl(m: re.Match) -> str:
        kind, title = m.group(1), m.group(2)
        head = f"**{title}**\n\n" if title else ""
        return f"::: {{.callout .callout-{kind}}}\n{head}"
    return re.sub(r'^:::+\s*\{[^}]*?\.callout-(\w+)(?:[^}]*?title="([^"]*)")?[^}]*\}[ \t]*\n',
                  repl, text, flags=re.M)


def check_tools() -> None:
    missing = [t for t in ("pandoc", "weasyprint") if not shutil.which(t)]
    if missing:
        sys.exit(f"error: required tool(s) not found on PATH: {', '.join(missing)}. "
                 "Install pandoc and weasyprint (pip install weasyprint) and retry.")


def build(src_name: str, web: bool) -> None:
    src = ROOT / src_name
    stem = src.stem
    with tempfile.TemporaryDirectory() as td:
        tmp_md = Path(td) / f"{stem}.md"
        tmp_md.write_text(convert_callouts(strip_quarto_format(src.read_text())))
        html = Path(td) / f"{stem}.html"
        subprocess.run(
            ["pandoc", str(tmp_md), "-s", "--toc", "--toc-depth=2",
             "--embed-resources", "--css", str(CSS),
             "--metadata", f"pagetitle={stem.replace('_', ' ')}",
             "-o", str(html)],
            check=True, cwd=ROOT,
        )
        subprocess.run(["weasyprint", "-q", str(html), str(ROOT / f"{stem}.pdf")],
                       check=True, cwd=ROOT)
        if web:  # only after the PDF succeeded
            (ROOT / f"{stem}.html").write_text(html.read_text())
    print(f"built {stem}.pdf" + (f" + {stem}.html" if web else ""))


def main() -> int:
    check_tools()
    for name, web in DOCS:
        build(name, web)
    return 0


if __name__ == "__main__":
    sys.exit(main())
