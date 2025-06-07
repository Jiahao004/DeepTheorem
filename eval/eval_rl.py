from transformers import AutoTokenizer, set_seed
import torch
import pandas as pd
import numpy as np
from collections import Counter
from vllm import LLM, SamplingParams

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, default="deeptheorem-7b/global_step_1000")
parser.add_argument("--data", type=str, default="data/fimo.jsonl")
parser.add_argument("--output", type=str, default="fimo")
args = parser.parse_args()

model_path = args.model
data_file = args.data

df = pd.read_json(data_file, lines=True)
tokenizer = AutoTokenizer.from_pretrained(model_path)

prompts = []
for p in df.prompt:
    messages = [
        {"role": "user", "content": p}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    prompts.append(text)
print(prompts[0])
print('---' * 10)

model = LLM(
    model=model_path,
    dtype=torch.bfloat16,
    tensor_parallel_size=4
)
sampling_params = SamplingParams(temperature=0, max_tokens=16000)
outputs = model.generate(prompts, sampling_params)
generation = [output.outputs[0].text for output in outputs]
stop_reasons = [output.outputs[0].finish_reason for output in outputs]
print(generation[0])
print('---' * 10)
print(Counter(stop_reasons))

df["generation"] = generation
df.to_json(f"{args.output}/{model_path.split('/')[-1]}.jsonl", orient='records', lines=True)

def extract_answer(s):
    s = s.lower()
    if "\\boxed{proved}" in s or "\\boxed{\\text{proved}}" in s:
        return 1
    if "\\boxed{disproved}" in s or "\\boxed{\\text{disproved}}" in s:
        return 0
    return -1
df["prediction"] = df.generation.apply(extract_answer)
print('Answer distribution:', Counter(df.answer))
print('Prediction distribution:', Counter(df.prediction))

accs = []
for problem in set(df.problem_name):
    df_ = df[df.problem_name==problem]
    accs.append((df_.answer==df_.prediction).prod())
print(f'Outcome score on {args.data.split('/')[-1].split('.')[0]}:', (np.mean(accs).round(4)*100).round(4))
