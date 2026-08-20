#!/usr/bin/env python3
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]


def main() -> None:
    design = json.loads((ROOT / "experiment/design.json").read_text())
    rows = list(csv.DictReader((ROOT / "data/item-effects.csv").open()))
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["route_id"]].append(int(row["belief_span"]))

    summary = {}
    qualifying = []
    heuristic = design["outreach_heuristic"]
    for route, values in sorted(grouped.items()):
        result = {
            "items": len(values),
            "mean": statistics.fmean(values),
            "median": statistics.median(values),
            "positive": sum(value > 0 for value in values),
            "zero": sum(value == 0 for value in values),
            "negative": sum(value < 0 for value in values),
        }
        summary[route] = result
        if (
            result["mean"] >= heuristic["route_mean_threshold"]
            and result["positive"] >= heuristic["route_positive_minimum_items"]
        ):
            qualifying.append(route)

    outreach = len(qualifying) >= heuristic["minimum_qualifying_routes"]
    print(
        json.dumps(
            {"routes": summary, "qualifying": qualifying, "outreach": outreach},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
