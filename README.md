# Sycophant

Preliminary work toward a benchmark for whether language-model assistants change their judgments to match a user's unsupported position.

The experiments ask models to evaluate identical material in fresh sessions while changing only the user's stated view. A positive span means the model gave a higher score when the user endorsed the claim or critique than when the user rejected it.

The accompanying article, [Do LLMs have beliefs of their own?](https://mihaicosma.com/posts/do-llms-have-bliefs.html), tells the story. This repository contains the frozen designs, complete derived scores, and dependency-free analysis.

## Three-axis factual-claim trial

Seven model routes rated 16 claims under neutral, user-believes-true, and user-believes-false framings. The claims crossed uncertainty, controversy, and vagueness.

Across 110 complete comparisons, the mean absolute span was 6.18 points. Twenty-nine comparisons moved at least 10 points and 13 moved at least 20. Six crossed 50 in the user-aligned direction, including five that met the stronger 60/40 definition. None crossed 50 in the opposite direction.

- [Claim matrix](experiment/three-axis-statements.json)
- [Full scorecard](data/three-axis-scorecard.md)
- [Model-level scorecard](data/three-axis-scorecard.csv)
- [Axis summaries](data/three-axis-axes.csv)
- [All 112 model-claim comparisons](data/three-axis-effects.csv)
- [All 336 model answers](data/three-axis-responses.jsonl)

## Public LMCA pilot

GPT 5.6 Sol, DeepSeek V4 Pro, and Gemini 3.1 Pro High rated five conceptual critiques printed in the public LMCA paper. Each critique appeared under neutral, user-says-good, and user-says-bad framings, producing 45 scores.

| Model route | Mean span | Median | Positive / zero / negative |
|---|---:|---:|---:|
| GPT 5.6 Sol | 35.0 | 36 | 5 / 0 / 0 |
| DeepSeek V4 Pro | 33.6 | 22 | 5 / 0 / 0 |
| Gemini 3.1 Pro High | 11.0 | 0 | 2 / 2 / 1 |

These models were easier to sway on the LMCA critiques than on the initial factual claims. Mean signed movement rose from 3.00 to 35.0 points for GPT, from 8.06 to 33.6 for DeepSeek, and from -1.79 to 11.0 for Gemini Pro.

- [All 45 scores and item-level effects](data/item-effects.csv)
- [All 45 model answers](data/lmca-responses.jsonl)
- [Route summaries](data/route-summary.csv)
- [Frozen design](experiment/design.json)
- [Prompt template](experiment/prompt-template.txt)
- [Methods](METHODS.md)

The pilot uses only the five critiques printed in the LMCA paper. It does not include requested or restricted LMCA records.

## Verify the results

Python 3.11 or newer is sufficient. There are no third-party dependencies.

```sh
python3 scripts/analyze.py
```

The script recomputes both headline summaries and checks them against the committed tables.

## Contributing

Contributions that improve the experimental design, add independently sourced claims, or make the analysis easier to audit are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting data or a new experiment.

Licensed under the [EUPL 1.2](LICENSE).
