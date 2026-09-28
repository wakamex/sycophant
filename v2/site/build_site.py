#!/usr/bin/env python3
"""Build the results page: python3 build_site.py ../SCORECARD-YYYYMMDD.md (its run list) or data/conversations.jsonl

Writes index.html beside this script. The page embeds its data and icons, so it is one self-contained file.
"""

import base64
import importlib.util
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
EXPERIMENT = SITE.parent
# The scorer sits in scripts/ beside this folder in the published release, or in the repository's scripts/.
SCORER = next(p for p in (EXPERIMENT / "scripts" / "score_pushback_drift.py", EXPERIMENT.parent.parent / "scripts" / "score_pushback_drift.py") if p.exists())
spec = importlib.util.spec_from_file_location("scorer", SCORER)
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)

# Display name, provider, brand color (None: the page's ink color), icon file.
MODELS = {
    "claude-opus": ("Claude Opus 5.5", "Anthropic", "#D97757", "claude-color.svg"),
    "claude-opus-5": ("Claude Opus 5", "Anthropic", "#D97757", "claude-color.svg"),
    "gemini-flash": ("Gemini 3.8 Flash", "Google", "#3186FF", "gemini-color.svg"),
    "glm-zcode": ("GLM-5.3", "Z.ai", None, "zai.svg"),
    "qwen": ("Qwen 3.8 Max", "Alibaba", "#6F69F7", "qwen-color.svg"),
    "grok-zen": ("Grok 4.7", "xAI", None, "grok.svg"),
    "kimi": ("Kimi K3", "Moonshot", "#1783FF", "kimi.svg"),
    "gpt-astra": ("GPT-6 Astra", "OpenAI", None, "openai.svg"),
    "deepseek": ("DeepSeek V4.1 Flash", "DeepSeek", "#4D6BFE", "deepseek-color.svg"),
    "gpt-6-sol": ("GPT-6 Sol", "OpenAI", None, "openai.svg"),
    "swe-2": ("SWE-2", "Cognition", "#0294DE", "devin-color.svg"),
    "gpt-5.6-sol": ("GPT-5.6 Sol", "OpenAI", None, "openai.svg"),
}
CODING_LABEL = {"neutral": "Neutral", "left": "Left-coded", "right": "Right-coded", "china": "China-sensitive", "ceo": "CEO post", "reality-testing": "Reality testing"}


def icon(name):
    svg = (SITE / "icons" / name).read_text()
    if "currentColor" in svg:
        return {"inline": re.sub(r"\s+", " ", svg).strip()}
    return {"src": "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()}


def rounded(v, digits=1):
    return None if v is None else round(v, digits)


def main(source_path, results_date=None):
    source = Path(source_path).resolve()
    if source.suffix == ".jsonl":
        records = S.load_records([source])
        stamp = results_date
    else:
        runs = re.findall(r"`([0-9]{8}T[0-9]{6}Z(?:-\d+)?)`", source.read_text().split("\n", 3)[2])
        records = S.load_records([EXPERIMENT / "runs" / r for r in runs])
        stamp = source.stem.split("-")[-1]
    per_route, cases = S.summarize_all(records)
    routes = json.loads((EXPERIMENT / "routes.json").read_text())
    developers = {r["id"]: r.get("developer_id") for r in routes}

    models = []
    for route_id, (label, provider, color, icon_file) in MODELS.items():
        summaries = per_route[route_id]
        m = S.group_metrics(summaries, developers.get(route_id))
        resistance, evidence = S.paired_pairs(summaries)
        v2 = S.bootstrap_score(evidence)
        res = S.bootstrap_score(resistance)
        models.append({
            "id": route_id, "label": label, "provider": provider, "color": color, "icon": icon(icon_file),
            "v2": [round(2 * x - 100) for x in v2[:3]], "v2_cases": v2[3],
            "resistance": [round(x) for x in res[:3]], "resistance_cases": res[3],
            "capitulation": rounded(m["capitulation_rate"], 2), "acceptance": rounded(m["evidence_acceptance"], 2),
            # PRC and CEO leans are left off the page: without mirrored posts they depend on the baseline chosen.
            "political_asymmetry": rounded(m["political_asymmetry"]),
            "belief_affirmation": rounded(m["belief_affirmation"]),
        })
    models.sort(key=lambda m: -m["v2"][0])

    # Case browser: every post, pushback and control conversations.
    clean = {cid for cid, c in cases.items() if any(a in ("evidence_up", "evidence_down") for a in c["arms"])}
    shown = sorted(cases)
    chains = S.chains_by_case(records)
    browser = []
    for cid in shown:
        case = cases[cid]
        source = (EXPERIMENT / "cases" / cid / case["source"]).read_text()
        post, _, facts = source.partition("# Fact sheet")
        trajectories = {}
        for (route_id, arm, rep, case_id), turns in chains.items():
            if case_id == cid and arm in ("up", "down", "control") and route_id in MODELS and rep == 0:
                scores = S.trajectory(turns)
                if len(scores) == 5 and None not in scores:
                    trajectories.setdefault(route_id, {})[arm] = scores
        browser.append({"id": cid, "coding": CODING_LABEL.get(case.get("coding", "neutral"), case.get("coding")),
                        "post": post.strip(), "facts": facts.strip(), "trajectories": trajectories,
                        "pushes": {arm: case["arms"][arm]["pushes"] for arm in ("up", "down", "control")}})

    kinds = {"real": 0, "written": 0, "mhb": 0}
    for c in cases.values():
        kinds["mhb" if c.get("coding") == "reality-testing" else "written" if c.get("topic") else "real"] += 1
    data = {"round": stamp, "models": models, "cases": browser, "kinds": kinds,
            "clean_cases": len(clean), "all_cases": len(cases), "chains": len(S.chains_by_case(records))}
    html = (SITE / "template.html").read_text().replace("/*DATA*/null", json.dumps(data, ensure_ascii=False))
    (SITE / "index.html").write_text(html)
    print(f"wrote index.html: {len(models)} models, {len(browser)} browsable cases, {len(html) // 1024} KB")


if __name__ == "__main__":
    main(*sys.argv[1:3])
