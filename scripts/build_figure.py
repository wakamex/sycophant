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


def x(value: float) -> float:
    return LEFT + (value - MINIMUM) / (MAXIMUM - MINIMUM) * PLOT_WIDTH


def main() -> None:
    rows = list(csv.DictReader((ROOT / "data/item-effects.csv").open()))
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["route_id"]].append((row["item_id"], int(row["belief_span"])))

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Belief span for each public LMCA critique</title>',
        '<desc id="desc">GPT and DeepSeek have positive score shifts on all five critiques. Gemini Pro has two positive, two zero, and one negative shift.</desc>',
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

    offsets = [-18, -9, 0, 9, 18]
    for index, (route, label, color) in enumerate(ROUTES):
        center = 125 + index * 92
        values = sorted(grouped[route])
        mean = statistics.fmean(value for _, value in values)
        lines.append(
            f'<text x="32" y="{center + 5}" font-family="system-ui, sans-serif" font-size="15" font-weight="650" fill="#263638">{html.escape(label)}</text>'
        )
        lines.append(
            f'<line x1="{x(min(v for _, v in values)):.1f}" y1="{center}" x2="{x(max(v for _, v in values)):.1f}" y2="{center}" stroke="{color}" stroke-opacity="0.28" stroke-width="3"/>'
        )
        for offset, (item, value) in zip(offsets, values, strict=True):
            lines.append(
                f'<circle cx="{x(value):.1f}" cy="{center + offset * 0.55:.1f}" r="5.5" fill="{color}"><title>{html.escape(item)}: {value:+d}</title></circle>'
            )
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
