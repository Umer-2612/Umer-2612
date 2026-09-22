"""Generate the SVG cards used in the profile README.

Edit the data below, then run:  python3 scripts/build_cards.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

ACCENT = "#39FF88"
MUTED = "#6e7681"
TEXT = "#e6edf3"
MONO = "'JetBrains Mono','Fira Code','SF Mono',Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

TERMINAL_LINES = [
    ("whoami", "Umer Karachiwala"),
    ("cat role", "Backend & DevOps Engineer · ex-Apple Software Engineer Intern"),
    ("cat focus", "distributed systems · event-driven backends · real-time AI pipelines"),
    ("uptime", "2+ yrs shipping production systems · based in Dublin, Ireland"),
]

METRICS = [
    "2+ Years Shipping Production Systems",
    "ex-Apple Software Engineer Intern",
    "900K+ Apple Store URLs Schedulable",
    "~100 Stuck Changesets Unblocked",
    "~80% Faster Resolution",
    "Multi-DC Search on OpenSearch",
    "Sub-second Live Audio Pipeline",
    "GenAI Hackathon Lead · Shortlisted",
]

CARD_WIDTH = 900
TITLE_BAR_HEIGHT = 44
LINE_GAP = 30
GROUP_GAP = 40
REVEAL_STEP_SECONDS = 0.45
FADE_SECONDS = 0.25


def fade_in(begin: float) -> str:
    # Starts at t=0 so the line stays hidden until its turn; renderers that
    # ignore SMIL fall back to the group's default opacity and show everything.
    hidden_until = begin / (begin + FADE_SECONDS)
    return (
        f'<animate attributeName="opacity" values="0;0;1" '
        f'keyTimes="0;{hidden_until:.3f};1" dur="{begin + FADE_SECONDS:.2f}s" fill="freeze"/>'
    )


def build_terminal_card() -> str:
    rows = []
    y = TITLE_BAR_HEIGHT + 48
    step = 0
    for command, output in TERMINAL_LINES:
        rows.append(
            f'<g><text x="40" y="{y}" fill="{MUTED}">$</text>'
            f'<text x="60" y="{y}" fill="{ACCENT}">{escape(command)}</text>'
            f"{fade_in(step * REVEAL_STEP_SECONDS)}</g>"
        )
        step += 1
        y += LINE_GAP
        rows.append(
            f'<g><text x="40" y="{y}" fill="{TEXT}" font-size="17">{escape(output)}</text>'
            f"{fade_in(step * REVEAL_STEP_SECONDS)}</g>"
        )
        step += 1
        y += GROUP_GAP

    cursor_begin = step * REVEAL_STEP_SECONDS
    rows.append(
        f'<g><text x="40" y="{y}" fill="{MUTED}">$</text>'
        f'<rect x="60" y="{y - 15}" width="10" height="19" fill="{ACCENT}">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>'
        f"{fade_in(cursor_begin)}</g>"
    )
    height = y + 36

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_WIDTH}" height="{height}" viewBox="0 0 {CARD_WIDTH} {height}" role="img" aria-label="Umer Karachiwala, Backend and DevOps Engineer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b120e"/><stop offset="1" stop-color="#0d1117"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.15" cy="0.2" r="0.9">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.09"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="{ACCENT}" opacity="0.025"/>
    </pattern>
    <clipPath id="card"><rect x="1" y="1" width="{CARD_WIDTH - 2}" height="{height - 2}" rx="14"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{CARD_WIDTH}" height="{height}" fill="url(#bg)"/>
    <rect width="{CARD_WIDTH}" height="{height}" fill="url(#glow)"/>
    <rect width="{CARD_WIDTH}" height="{height}" fill="url(#scan)"/>
    <rect width="{CARD_WIDTH}" height="{TITLE_BAR_HEIGHT}" fill="#070b09"/>
  </g>
  <rect x="1" y="1" width="{CARD_WIDTH - 2}" height="{height - 2}" rx="14" fill="none" stroke="{ACCENT}" stroke-opacity="0.3"/>
  <circle cx="28" cy="22" r="6" fill="#FF5F57"/><circle cx="48" cy="22" r="6" fill="#FEBC2E"/><circle cx="68" cy="22" r="6" fill="#28C840"/>
  <text x="{CARD_WIDTH // 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{ACCENT}" opacity="0.7">umer@dublin: ~/profile</text>
  <g font-family="{MONO}" font-size="18">
    {chr(10).join('    ' + r for r in rows).strip()}
  </g>
</svg>
"""


PILL_HEIGHT = 32
PILL_GAP = 12
ROW_GAP = 14
PILL_CHAR_WIDTH = 7.0
PILL_PADDING = 34


def layout_pills(labels):
    rows, current, used = [], [], 0.0
    for label in labels:
        width = len(label) * PILL_CHAR_WIDTH + PILL_PADDING
        needed = width if not current else used + PILL_GAP + width
        if current and needed > CARD_WIDTH:
            rows.append((current, used))
            current, used = [], 0.0
            needed = width
        current = current + [(label, width)]
        used = needed
    if current:
        rows.append((current, used))
    return rows


def build_metrics_pills() -> str:
    rows = layout_pills(METRICS)
    parts = []
    for index, (pills, row_width) in enumerate(rows):
        x = (CARD_WIDTH - row_width) / 2
        y = 2 + index * (PILL_HEIGHT + ROW_GAP)
        for label, width in pills:
            parts.append(
                f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="{PILL_HEIGHT}" rx="16" fill="url(#pill)" stroke="#2f5b41"/>'
                f'<text x="{x + width / 2:.1f}" y="{y + 21}" text-anchor="middle">{escape(label)}</text>'
            )
            x += width + PILL_GAP
    height = 4 + len(rows) * PILL_HEIGHT + (len(rows) - 1) * ROW_GAP
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_WIDTH}" height="{height}" viewBox="0 0 {CARD_WIDTH} {height}" role="img" aria-label="{escape(' · '.join(METRICS))}">
  <defs>
    <linearGradient id="pill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#15231b"/><stop offset="1" stop-color="#0f1813"/>
    </linearGradient>
  </defs>
  <g font-family="{SANS}" font-size="12.5" font-weight="600" fill="#d7ffe6">
    {chr(10).join('    ' + p for p in parts).strip()}
  </g>
</svg>
"""


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "terminal-card.svg").write_text(build_terminal_card(), encoding="utf-8")
    (ASSETS / "metrics-pills.svg").write_text(build_metrics_pills(), encoding="utf-8")
    print(f"Wrote cards to {ASSETS}")


if __name__ == "__main__":
    main()
