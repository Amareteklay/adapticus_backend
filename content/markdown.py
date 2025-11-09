# content/markdown.py
from __future__ import annotations

from markdown_it import MarkdownIt

# CommonMark + useful extras
_md = MarkdownIt("commonmark").enable("table").enable("strikethrough")


def md_to_html(md_text: str | None) -> str:
    return _md.render(md_text or "")
