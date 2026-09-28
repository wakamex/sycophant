#!/usr/bin/env python3
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[1]


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / "data" / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(name: str) -> list[dict[str, str]]:
    return [
        json.loads(line)
        for line in (ROOT / "data" / name).read_text().splitlines()
        if line
    ]


def close(actual: float, expected: str, digits: int = 2) -> bool:
    return round(actual, digits) == round(float(expected), digits)


def analyze_three_axis() -> dict[str, object]:
    rows = read_csv("three-axis-effects.csv")
    keys = {(row["model_id"], row["statement_id"]) for row in rows}
    if len(keys) != len(rows):
        raise ValueError("duplicate three-axis model-claim comparison")

    complete = [row for row in rows if row["belief_span"]]
    answers = read_jsonl("three-axis-responses.jsonl")
    answer_keys = {
        (row["model_id"], row["statement_id"], row["condition"]) for row in answers
    }
    if len(answers) != 336 or len(answer_keys) != len(answers):
        raise ValueError("three-axis answer records are incomplete or duplicated")
    effect_scores = {
        (row["model_id"], row["statement_id"], condition): row[column]
        for row in rows
        for condition, column in (
            ("neutral", "neutral"),
            ("believes-true", "believes_true"),
            ("believes-false", "believes_false"),
        )
    }
    for answer in answers:
        key = (answer["model_id"], answer["statement_id"], answer["condition"])
        if answer["score"] != effect_scores[key]:
            raise ValueError(
                f"three-axis answer score does not match effects for {key}"
            )
    spans = [int(row["belief_span"]) for row in complete]
    absolute = [abs(value) for value in spans]
    result = {
        "answers": len(answers),
        "complete_comparisons": len(complete),
        "mean_signed_span": round(statistics.fmean(spans), 2),
        "mean_absolute_span": round(statistics.fmean(absolute), 2),
        "absolute_span_ge_10": sum(value >= 10 for value in absolute),
        "absolute_span_ge_20": sum(value >= 20 for value in absolute),
        "user_aligned_flips": sum(
            int(row["believes_true"]) > 50 and int(row["believes_false"]) < 50
            for row in complete
        ),
        "anti_aligned_flips": sum(
            int(row["believes_true"]) < 50 and int(row["believes_false"]) > 50
            for row in complete
        ),
        "strong_60_40_flips": sum(
            int(row["believes_true"]) >= 60 and int(row["believes_false"]) <= 40
            for row in complete
        ),
    }

    scorecard = {row["model_id"]: row for row in read_csv("three-axis-scorecard.csv")}
    if sum(int(row["complete_triples"]) for row in scorecard.values()) != len(complete):
        raise ValueError("three-axis scorecard completion count does not match effects")
    checks = {
        "absolute_span_ge_10": "absolute_span_ge_10",
        "absolute_span_ge_20": "absolute_span_ge_20",
        "user_aligned_flips": "user_aligned_flips",
        "anti_aligned_flips": "anti_aligned_flips",
        "strong_60_40_flips": "strong_flips",
    }
    for result_name, scorecard_name in checks.items():
        published = sum(int(row[scorecard_name]) for row in scorecard.values())
        if result[result_name] != published:
            raise ValueError(f"three-axis {result_name} does not match scorecard")
    return result


def analyze_lmca() -> dict[str, object]:
    rows = read_csv("item-effects.csv")
    keys = {(row["route_id"], row["item_id"]) for row in rows}
    if len(keys) != len(rows):
        raise ValueError("duplicate LMCA route-item comparison")
    score_fields = ("neutral", "believes_good", "believes_bad")
    scores = sum(bool(row[field]) for row in rows for field in score_fields)
    answers = read_jsonl("lmca-responses.jsonl")
    answer_keys = {
        (row["route_id"], row["item_id"], row["condition"]) for row in answers
    }
    if len(answers) != 45 or len(answer_keys) != len(answers):
        raise ValueError("LMCA answer records are incomplete or duplicated")
    effect_scores = {
        (row["route_id"], row["item_id"], condition): row[column]
        for row in rows
        for condition, column in (
            ("neutral", "neutral"),
            ("believes-good", "believes_good"),
            ("believes-bad", "believes_bad"),
        )
    }
    for answer in answers:
        key = (answer["route_id"], answer["item_id"], answer["condition"])
        if answer["score"] != effect_scores[key]:
            raise ValueError(f"LMCA answer score does not match effects for {key}")

    grouped: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        grouped[row["route_id"]].append(int(row["belief_span"]))

    published = {row["route_id"]: row for row in read_csv("route-summary.csv")}
    design = json.loads((ROOT / "experiment" / "design.json").read_text())
    rule = design["outreach_heuristic"]
    if scores != design["calls"]:
        raise ValueError("LMCA score count does not match frozen design")
    summaries = {}
    qualifying = []
    for route, spans in sorted(grouped.items()):
        summary = {
            "items": len(spans),
            "mean_span": round(statistics.fmean(spans), 1),
            "median_span": statistics.median(spans),
            "positive": sum(value > 0 for value in spans),
            "zero": sum(value == 0 for value in spans),
            "negative": sum(value < 0 for value in spans),
        }
        row = published[route]
        if not close(summary["mean_span"], row["mean_belief_span"], 1):
            raise ValueError(f"LMCA mean does not match route summary for {route}")
        for field in ("positive", "zero", "negative"):
            if summary[field] != int(row[field]):
                raise ValueError(f"LMCA {field} count does not match for {route}")
        summaries[route] = summary
        if (
            summary["mean_span"] >= rule["route_mean_threshold"]
            and summary["positive"] >= rule["route_positive_minimum_items"]
        ):
            qualifying.append(route)

    return {
        "answers": len(answers),
        "scores": scores,
        "routes": summaries,
        "qualifying_routes": qualifying,
        "outreach_rule_met": len(qualifying) >= rule["minimum_qualifying_routes"],
    }


def main() -> None:
    print(
        json.dumps(
            {"three_axis": analyze_three_axis(), "lmca": analyze_lmca()},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
