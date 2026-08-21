# Methods

## Shared manipulation

Both experiments compare fresh sessions containing identical evaluation material and instructions. Only the user's unsupported position changes. Neutral sessions omit the position line.

The signed span is the score under user endorsement minus the score under user rejection. Positive values follow the user's stated view. Absolute spans measure movement in either direction.

## Three-axis factual claims

The first experiment contains two claims in each combination of low or high uncertainty, controversy, and vagueness. Seven model routes rated each claim from 0 to 100 under three framings. The [claim matrix](experiment/three-axis-statements.json) records the assignments and the [paired effects](data/three-axis-effects.csv) contain every model-claim comparison.

The frozen prompt shape is in [experiment/three-axis-prompt-template.txt](experiment/three-axis-prompt-template.txt).

The neutral condition omitted only the line stating the user's position. The valid assessment-first run produced 336 calls and 110 complete framed comparisons. Two Gemini Pro responses lacked usable scores and were retained as missing.

## Public LMCA critiques

The second experiment uses the five rated critiques printed in Tables 2, 3, 8, and 9 of [A dataset of rated conceptual arguments](https://arxiv.org/abs/2607.27499). It identifies those table entries but does not reproduce the paper or restricted LMCA records.

Each model-item pair ran under neutral, user-says-good, and user-says-bad conditions. The position, critique, rating instructions, route, and execution setup stayed fixed within each comparison. The [prompt template](experiment/prompt-template.txt) contains the exact instructions.

| Route ID | Harness | Model |
|---|---|---|
| `gpt` | Codex | `gpt-5.6-sol` |
| `gemini-pro` | Agy | `gemini-3.1-pro-high` |
| `deepseek` | DSH | `deepseek-v4-pro` |

The routes used fresh sessions through [Agent Orchestration Process](https://github.com/wakamex/agent-orchestration-process) v0.1.7 at commit `7b2c8172d0a15402533cfaa056ce3b351dc5bedc`. Calls were shuffled with seed `20260820`.

The frozen outreach rule required at least two routes to average a span of 5 points or more and produce positive spans on at least three of five critiques. GPT and DeepSeek met it.

The initial batch completed 44 of 45 calls. One interrupted Gemini response was rejected and the exact cell was rerun with the same prompt and execution settings. [Provenance](data/provenance.json) identifies the source run and selected retry.

The public examples support this matched comparison, but broader LMCA coverage would be needed to measure how common the effect is.
