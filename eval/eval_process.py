import pandas as pd

model_name="gpt-4o"

prompt_template = '''You are an expert in scoring solutions for mathematical proof questions. The following question asks to prove or disprove a statement, where the statement may be either true or false. The test subject is asked to end their proof with \\boxed{proved} if they prove the statement to be true, and \\boxed{disproved} if they prove the statement to be false.

The question:

```
<question>
```

The ground truth of the statement:

```
<answer>
```

The test subject's solution:

```
<solution>
```

Your task is to evaluate the proof's quality and assign a score from 0 to 1 based on four criteria: logical validity (40%), completeness (30%), correctness (20%), and clarity (10%).

Instructions:

1. Analyze the proof step by step.
2. For each criterion:
   - Logical Validity: Check if each step follows logically from the previous one. Flag any logical errors.
   - Completeness: Verify if all necessary cases and steps are included to prove the theorem.
   - Correctness: Confirm if the final conclusion is correct.
   - Clarity: Assess if the proof is clear, unambiguous, and well-explained.
3. Assign a sub-score (0 to 1) for each criterion and compute the total score using the weights: (0.4 × validity) + (0.3 × completeness) + (0.2 × correctness) + (0.1 × clarity).
4. Provide a brief explanation (2-3 sentences) summarizing any errors or issues and justifying the score.

Final output format:

```
{
    "score": float,
    "validity": float,
    "completeness": float,
    "correctness": float,
    "clarity": float,
    "explanation": str
}
```

where "score" is the total score, and "validity", "completeness", "correctness", "clarity" are the subscores.'''


# 1. the input file is output by eval_llm.py or eval_rl.py
df = pd.read_json('fimo/global_step_1000.jsonl', lines=True)

prompts = []
for _, s in df.iterrows():
    prompts.append(prompt_template.replace('<question>', s['prompt']).replace('<answer>', ("True" if s['answer'] else "False")).replace('<solution>', s['generation']))

# 2. use your own framework to query GPT-4o with these prompts
