### Outcome Evaluation

To evaluate DeepTheorem models trained with RL, see `eval_rl.py`. There is no need to set system prompts, as we use the prompt set before training (refer to [this README](https://github.com/Jiahao004/DeepTheorem/blob/main/scripts/README.md)).

To evaluate other models (e.g. Qwen2.5, LLaMA3, DeepSeek-R1, GPT4), see `eval_llm.py`.

- For open-source models, remember to change the system prompt for each model (prompts for Qwen2.5, LLaMA3, and DeepSeek-R1 models are provided in the script as comments).
- For API-based models, the prompts are the same, but you need to modify the code to query the model APIs with your keys.

### Process Evaluation

We use GPT-4o for process evaluation. The prompts are provided in `eval_process.py`.
