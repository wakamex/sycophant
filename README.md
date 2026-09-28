# Sycophant

Benchmarks for whether language-model assistants change their judgments to please a user rather than in response to evidence.

## [v2: Sycophancy Bench v2](v2/)

Twelve models rated the same posts in five-turn conversations, once under evidence-free pushback and once with a real correction published after their training cutoffs. The v2 score, from -100 to 100, compares how far the correction moved each model's rating with how far pushback did. Claude Opus 5.5 and Opus 5 update on evidence and hold under pressure; GPT-6 Sol, SWE-2 and GPT-5.6 Sol move further for pushback than for evidence. The folder has every post, fact sheet, correction and conversation, the scorer, and the results page.

## [v1: user-belief framing](v1/)

The first experiments: seven models rated 16 factual claims, and three models rated five critiques from the public LMCA paper, with only the user's stated view changing between fresh sessions. The accompanying article is [Do LLMs have beliefs of their own?](https://mihaicosma.com/blog/do-llms-have-beliefs.html)

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting data or a new experiment. Licensed under the [EUPL 1.2](LICENSE).
