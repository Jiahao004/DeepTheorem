import pandas as pd
from datasets import load_from_disk, Dataset
from tqdm.auto import tqdm

dataset = load_from_disk('deeptheorem')

data = []
for row in tqdm(dataset):
    data.append(
        {
            "data_source": "deeptheorem",
            "prompt": [
                {"role": "user", "content": row["pos_question"]}
            ],
            "ability": "math",
            "reward_model":{
                "style": "rule",
                "ground_truth": "proved" if row["pos_truth_value"] else "disproved"
            },
            "extra_info":{
                "split": "train",
                "index": row["id"],
                "answer": "proved" if row["pos_truth_value"] else "disproved",
                "question": row["pos_question"]
            }
        }
    )
    data.append(
        {
            "data_source": "deeptheorem",
            "prompt": [
                {"role": "user", "content": row["neg_question"]}
            ],
            "ability": "math",
            "reward_model":{
                "style": "rule",
                "ground_truth": "proved" if row["neg_truth_value"] else "disproved"
            },
            "extra_info":{
                "split": "train",
                "index": row["id"],
                "answer": "proved" if row["neg_truth_value"] else "disproved",
                "question": row["neg_question"]
            }
        }
    )
train_dataset = Dataset.from_list(data)
train_dataset.to_parquet("deeptheorem/train.parquet")
train_dataset.to_parquet("deeptheorem/test.parquet")
