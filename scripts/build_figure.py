#!/usr/bin/env python3
import csv
import html
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]
WIDTH = 920
HEIGHT = 390
LEFT = 170
RIGHT = 50
TOP = 76
PLOT_WIDTH = WIDTH - LEFT - RIGHT
MINIMUM = -10
MAXIMUM = 80
ROUTES = [
    ("gpt", "GPT 5.6 Sol", "#1f6f78"),
    ("deepseek", "DeepSeek V4 Pro", "#c35a33"),
    ("gemini-pro", "Gemini 3.1 Pro High", "#7358a6"),
]
ITEM_LABELS = {
    "approval_voting_strategy": "Approval voting strategy",
    "ethnic_mixing_autonomy": "Ethnic mixing and autonomy",
    "freedom_active_interference": "Freedom and active interference",
    "is_ought_hidden_normative_premise_bad": "Is-ought hidden premise, low-rated",
    "is_ought_hidden_normative_premise_good": "Is-ought hidden premise, high-rated",
}


def x(value: float) -> float:
    return LEFT + (value - MINIMUM) / (MAXIMUM - MINIMUM) * PLOT_WIDTH


def main() -> None:
    rows = list(csv.DictReader((ROOT / "data/item-effects.csv").open()))
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["route_id"]].append(row)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Belief span for each public LMCA critique</title>',
        '<desc id="desc">GPT and DeepSeek have positive score shifts on all five critiques. Gemini Pro has two positive, two zero, and one negative shift.</desc>',
        '<style>.point{cursor:help}.point circle{stroke:#fffdf8;stroke-width:2}.tooltip{opacity:0;pointer-events:none}.point:hover .tooltip,.point:focus .tooltip{opacity:1}.point:focus{outline:none}.point:hover circle,.point:focus circle{stroke:#172528;stroke-width:2.5}</style>',
        '<rect width="100%" height="100%" rx="18" fill="#fffdf8"/>',
        '<text x="32" y="38" font-family="system-ui, sans-serif" font-size="21" font-weight="700" fill="#172528">Same critique, different user position</text>',
        '<text x="32" y="61" font-family="system-ui, sans-serif" font-size="13" fill="#536164">Each dot is good score minus bad score. Diamond is the route mean.</text>',
    ]
    for tick in range(-10, 81, 10):
        coordinate = x(tick)
        color = "#819093" if tick == 0 else "#e3dfd5"
        width = 1.5 if tick == 0 else 1
        lines.append(
            f'<line x1="{coordinate:.1f}" y1="{TOP}" x2="{coordinate:.1f}" y2="326" stroke="{color}" stroke-width="{width}"/>'
        )
        lines.append(
            f'<text x="{coordinate:.1f}" y="350" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#647174">{tick}</text>'
        )

    for index, (route, label, color) in enumerate(ROUTES):
        center = 125 + index * 92
        values = sorted(grouped[route], key=lambda row: row["item_id"])
        spans = [int(row["belief_span"]) for row in values]
        mean = statistics.fmean(spans)
        lines.append(
            f'<text x="32" y="{center + 5}" font-family="system-ui, sans-serif" font-size="15" font-weight="650" fill="#263638">{html.escape(label)}</text>'
        )
        lines.append(
            f'<line x1="{x(min(spans)):.1f}" y1="{center}" x2="{x(max(spans)):.1f}" y2="{center}" stroke="{color}" stroke-opacity="0.35" stroke-width="3"/>'
        )
        tied = defaultdict(list)
        for row in values:
            tied[int(row["belief_span"])].append(row)
        for value, point_rows in sorted(tied.items()):
            coordinate = x(value)
            tooltip_width = 290
            tooltip_height = 30 + 17 * len(point_rows)
            tooltip_x = min(max(coordinate - tooltip_width / 2, 12), WIDTH - tooltip_width - 12)
            tooltip_y = center + 14 if center < 250 else center - tooltip_height - 14
            item_names = [ITEM_LABELS[row["item_id"]] for row in point_rows]
            aria = f'{label}, {value:+d} belief span: {", ".join(item_names)}'
            radius = 8 if len(point_rows) > 1 else 6
            lines.append(
                f'<g class="point" tabindex="0" role="graphics-symbol" aria-label="{html.escape(aria)}">'
            )
            lines.append(
                f'<circle cx="{coordinate:.1f}" cy="{center}" r="{radius}" fill="{color}"/>'
            )
            if len(point_rows) > 1:
                lines.append(
                    f'<text x="{coordinate:.1f}" y="{center + 3.5}" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="700" fill="#fffdf8" pointer-events="none">{len(point_rows)}</text>'
                )
            lines.append('<g class="tooltip">')
            lines.append(
                f'<rect x="{tooltip_x:.1f}" y="{tooltip_y:.1f}" width="{tooltip_width}" height="{tooltip_height}" rx="7" fill="#172528"/>'
            )
            lines.append(
                f'<text x="{tooltip_x + 11:.1f}" y="{tooltip_y + 18:.1f}" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#fffdf8">Belief span {value:+d}</text>'
            )
            for line_index, item_name in enumerate(item_names):
                lines.append(
                    f'<text x="{tooltip_x + 11:.1f}" y="{tooltip_y + 36 + line_index * 17:.1f}" font-family="system-ui, sans-serif" font-size="11" fill="#dce5e3">{html.escape(item_name)}</text>'
                )
            lines.append("</g></g>")
        mean_x = x(mean)
        points = (
            f"{mean_x:.1f},{center - 9} {mean_x + 9:.1f},{center} "
            f"{mean_x:.1f},{center + 9} {mean_x - 9:.1f},{center}"
        )
        lines.append(
            f'<polygon points="{points}" fill="#172528"><title>Mean: {mean:.1f}</title></polygon>'
        )
        lines.append(
            f'<text x="{mean_x + 14:.1f}" y="{center + 5}" font-family="ui-monospace, monospace" font-size="12" font-weight="700" fill="#172528">{mean:.1f}</text>'
        )

    lines.extend(
        [
            '<text x="445" y="378" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#536164">Belief span in score points</text>',
            "</svg>",
        ]
    )
    (ROOT / "docs/belief-spans.svg").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
