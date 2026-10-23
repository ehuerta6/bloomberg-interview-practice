"""Render the static homepage from the build's validated problem manifest."""

from html import escape
from pathlib import Path
from string import Template
from urllib.parse import quote


TEMPLATE = Path(__file__).resolve().parent / "site/index.html"
CATEGORIES = (
    ("round-1", "PR Reviews", "Review code, investigate defects, and explain the changes you would make."),
    ("round-2", "Engineering Tickets", "Implement a feature from its requirements and reason about edge cases."),
    ("system-design", "System Designs", "Explore requirements, architecture, and the tradeoffs behind a design."),
)


def render_catalog(manifest):
    navigation, sections = [], []
    for category, label, description in CATEGORIES:
        problems = [problem for problem in manifest["problems"] if problem["category"] == category]
        navigation.append(f'      <a href="#{category}">{label}</a>')
        cards = []
        for problem in problems:
            difficulty = problem["difficulty"].lower()
            cards.append(
                '        <li>\n'
                f'          <a class="problem-card" href="problems/{quote(problem["slug"], safe="")}.html">\n'
                f'            <span class="problem-number">{problem["number"]:02d}</span>\n'
                f'            <span class="problem-title">{escape(problem["title"])}</span>\n'
                f'            <span class="tag difficulty-{difficulty}">{escape(problem["difficulty"])}</span>\n'
                '          </a>\n'
                '        </li>'
            )
        sections.append(
            f'    <section aria-labelledby="{category}" data-category="{category}">\n'
            f'      <h2 id="{category}" tabindex="-1">{label} <span class="meta">{len(problems)} problems</span></h2>\n'
            f'      <p>{description}</p>\n'
            '      <ul class="problem-grid">\n' + "\n".join(cards) + '\n      </ul>\n'
            '      <p class="meta"><a href="#main-content">Back to top</a></p>\n'
            '    </section>'
        )
    return Template(TEMPLATE.read_text(encoding="utf-8")).substitute(
        navigation="\n".join(navigation),
        total=len(manifest["problems"]),
        categories="\n".join(sections),
    )
