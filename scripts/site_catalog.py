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
NIGHTMARE_ASSIGNMENTS = (
    ("01", "Duplicate Checkout", "nightmares/01.md"),
    ("02", "Inventory Validation", "nightmares/02.md"),
    ("03", "Double Cancellation", "nightmares/03.md"),
    ("04", "Cart Ownership Leak", "nightmares/04.md"),
    ("05", "Checkout Price Mismatch", "nightmares/05.md"),
    ("06", "Payment Error Handling", "nightmares/06.md"),
    ("07", "Partial Checkout Failure", "nightmares/07.md"),
    ("08", "Admin Authorization Regression", "nightmares/08.md"),
    ("09", "Cart Update Race", "nightmares/09.md"),
    ("10", "Misleading Regression Tests", "nightmares/10.md"),
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
    nightmare_cards = []
    for challenge_id, title, assignment_path in NIGHTMARE_ASSIGNMENTS:
        assignment_url = (
            "https://github.com/ehuerta6/bloomberg-interview-practice/blob/main/"
            + assignment_path
        )
        nightmare_cards.append(
            '        <li>\n'
            f'          <a class="problem-card" href="{escape(assignment_url, quote=True)}" target="_blank" rel="noopener noreferrer">\n'
            f'            <span class="problem-number">{escape(challenge_id)}</span>\n'
            f'            <span class="problem-title">{escape(title)}</span>\n'
            '            <span class="tag tag-nightmare">Nightmare</span>\n'
            '          </a>\n'
            '        </li>'
        )
    nightmares = (
        '    <section aria-labelledby="nightmares">\n'
        '      <h2 id="nightmares" tabindex="-1">Nightmare Mode</h2>\n'
        '      <p>Ten original CIC exercises for practicing AI-assisted engineering: five Engineering Tickets and five PR Reviews. These are not official Bloomberg interview questions.</p>\n'
        '      <ul class="problem-grid">\n' + "\n".join(nightmare_cards) + '\n      </ul>\n'
        '      <p class="meta"><a href="#main-content">Back to top</a></p>\n'
        '    </section>'
    )
    navigation.append('      <a href="#nightmares">Nightmare Mode</a>')
    return Template(TEMPLATE.read_text(encoding="utf-8")).substitute(
        navigation="\n".join(navigation),
        total=len(manifest["problems"]),
        categories="\n".join(sections),
        nightmares=nightmares,
    )
