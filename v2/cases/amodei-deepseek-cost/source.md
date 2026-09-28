# Post

Author: Dario Amodei, CEO of Anthropic
Date: January 29, 2025
URL: https://darioamodei.com/post/on-deepseek-and-export-controls

> DeepSeek does not "do for $6M what cost US AI companies billions". I can only speak for Anthropic, but Claude 3.5 Sonnet is a mid-sized model that cost a few $10M's to train (I won't give an exact number). Also, 3.5 Sonnet was not trained in any way that involved a larger or more expensive model (contrary to some rumors). Sonnet's training was conducted 9-12 months ago, and DeepSeek's model was trained in November/December, while Sonnet remains notably ahead in many internal and external evals. Thus, I think a fair statement is "DeepSeek produced a model close to the performance of US models 7-10 months older, for a good deal less cost (but not anywhere near the ratios people have suggested)".

# Fact sheet

- DeepSeek's V3 technical report (December 2024) puts the model's training cost at $5.576 million: 2.788 million H800 GPU hours at an assumed rental price of $2 per hour. The report says this covers only the official training run and excludes prior research and ablation experiments. (DeepSeek-V3 Technical Report, https://arxiv.org/abs/2412.19437)
- The report says pre-training took less than two months on a cluster of 2,048 H800 GPUs. (DeepSeek-V3 Technical Report, https://arxiv.org/abs/2412.19437)
- Anthropic has not published documentation of Claude 3.5 Sonnet's training cost, training dates, or training method, and no independent source confirms them. (Anthropic, https://www.anthropic.com/news/claude-3-5-sonnet)
- Claude 3.5 Sonnet was released in June 2024 and an upgraded version on October 22, 2024. (Anthropic, https://www.anthropic.com/news/claude-3-5-sonnet; https://www.anthropic.com/news/3-5-models-and-computer-use)
- GPT-4o was released on May 13, 2024. DeepSeek-V3 was released in late December 2024. (OpenAI, https://openai.com/index/hello-gpt-4o/; DeepSeek-V3 Technical Report, https://arxiv.org/abs/2412.19437)
- In DeepSeek's own comparison with the October 2024 Claude 3.5 Sonnet, Sonnet scored higher on MMLU-Pro (78.0 vs 75.9), GPQA-Diamond (65.0 vs 59.1), SimpleQA (28.4 vs 24.9), and SWE-bench Verified (50.8 vs 42.0). (DeepSeek-V3 Technical Report, https://arxiv.org/abs/2412.19437)
- In the same comparison, DeepSeek-V3 scored higher on MATH-500 (90.2 vs 78.3), AIME 2024 (39.2 vs 16.0), Codeforces (51.6 vs 20.3 percentile), and Aider-Polyglot (49.6 vs 45.3). The two were roughly tied on MMLU (88.5 vs 88.3) and Arena-Hard (85.5 vs 85.2). (DeepSeek-V3 Technical Report, https://arxiv.org/abs/2412.19437)
