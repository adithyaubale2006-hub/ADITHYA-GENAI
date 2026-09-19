"""Rendering helpers for the Streamlit interface."""

from html import escape
from pathlib import Path

import streamlit as st


TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def _template(name, **values):
    template = (TEMPLATE_DIR / name).read_text(encoding="utf-8")
    return template.format(**values)


def _markdown_html(html):
    st.markdown(html, unsafe_allow_html=True)


def inject_css():
    css = (Path(__file__).resolve().parent / "styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_sidebar_logo():
    _markdown_html(_template("sidebar_logo.html"))


def render_pipeline_panel(rows):
    st.markdown('<div class="pipeline-label">Pipeline</div>', unsafe_allow_html=True)
    for label, value in rows:
        _markdown_html(_template("pipeline_row.html", label=escape(str(label)), value=escape(str(value))))


def render_disclaimer():
    _markdown_html(
        '<div class="disclaimer">For research use only. This tool summarizes the documents '
        "provided to it and does not provide investment advice.</div>"
    )


def render_masthead(filings, chunks, k):
    _markdown_html(
        _template(
            "masthead.html",
            filings=escape(str(filings)),
            chunks=escape(str(chunks)),
            k=escape(str(k)),
        )
    )


def parse_answer_sections(answer):
    headings = {
        "answer": "Answer",
        "key financial metrics": "Key Financial Metrics",
        "analysis": "Analysis",
        "risks / considerations": "Risks / Considerations",
        "source": "Source",
    }
    sections = []
    current = None
    for line in str(answer).splitlines():
        heading = line.strip().rstrip(":").lower()
        if heading in headings:
            if current:
                current["body"] = "\n".join(current["lines"]).strip()
                sections.append(current)
            current = {"heading": headings[heading], "lines": []}
        elif current:
            current["lines"].append(line)

    if current:
        current["body"] = "\n".join(current["lines"]).strip()
        sections.append(current)

    if not sections:
        return [{"heading": "Answer", "body": str(answer).strip()}]
    return sections


def render_answer_report(sections):
    for section in sections:
        heading = section.get("heading", "Answer")
        body = section.get("body", "")
        extra_class = "risk" if heading.lower().startswith("risks") else heading.lower().split()[0]
        icon = ""
        _markdown_html(
            _template(
                "report_block.html",
                extra_class=escape(extra_class),
                icon=icon,
                label=escape(heading),
                body=escape(body).replace("\n", "<br>") or "&nbsp;",
            )
        )


def render_passage_card(index, source_name, page, text):
    _markdown_html(
        _template(
            "passage_card.html",
            index=escape(str(index)),
            source_name=escape(str(source_name)),
            page=escape(str(page)),
            text=escape(str(text)).replace("\n", "<br>"),
        )
    )