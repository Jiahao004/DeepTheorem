# DeepTheorem: Advancing LLM Reasoning for Theorem Proving Through Natural Language and Reinforcement Learning 🚀

Welcome to the GitHub repository for **DeepTheorem** 🎉, a comprehensive framework for enhancing large language model (LLM) mathematical reasoning through informal, natural language-based theorem proving. This project introduces a novel approach to automated theorem proving (ATP) by leveraging the informal reasoning strengths of LLMs, moving beyond traditional formal proof systems 🌟.

## Overview 📖

Theorem proving is a critical benchmark for evaluating complex reasoning in LLMs 🧠. However, formal proof systems often misalign with the informal, natural language knowledge LLMs acquire during pre-training. DeepTheorem addresses this gap by introducing:

1. **A Large-Scale Benchmark Dataset** 📊: 
   - Contains **138K high-quality, IMO-level informal theorems and proofs** across diverse mathematical domains 📚.
   - Rigorously annotated for correctness, difficulty, and topic categories ✅.
   - Includes systematically constructed **verifiable theorem variants** for robust evaluation 🔍.
   - [Dataset Link](#) 🔗.

2. **RL-Zero** 🤖: 
   - A novel **reinforcement learning strategy** tailored for informal theorem proving ⚙️.
   - Utilizes verified theorem variants to incentivize robust mathematical inference 💡.
   - [RL-Zero Documentation](#) (e.g., see the RL-Zero methodology [here](#)) 📄.

3. **Comprehensive Evaluation Metrics** 📈:
   - Outcome metrics to assess proof correctness ✔️.
   - Process metrics to evaluate the quality of reasoning steps 🛠️.
   - [Evaluation Metrics Details](#) (e.g., explore evaluation scripts [here](#)) 🔎.



## Performance 🚀
Deeptheorem achieves the #Rank 5 position along all the commerical models and open source models.

| **Model**             | **FIMO** |         | **HMMT** |         | **Putnam** |         | **Avg.** |         | **\#Rank** |         |
| :--------------------- | :------: | :-----: | :------: | :-----: | :--------: | :-----: | :------: | :-----: | ---------: | ------: |
|                        | *out.*   | *proc.* | *out.*   | *proc.* | *out.*     | *proc.* | *out.*   | *proc.* | *out.*     | *proc.* |
| Gemini2\.5-Pro         | 57\.14   | 54\.06  | 57\.63   | 49\.82  | 64\.58     | 58\.75  | 59\.78   | 54\.21  | 2          | 3       |
| o1-mini                | 60\.32   | 55\.23  | 35\.59   | 30\.90  | 61\.46     | 52\.88  | 52\.46   | 46\.34  | 4          | 4       |
| o1                     | 66\.67   | 61\.00  | 47\.46   | 47\.30  | 62\.50     | 57\.55  | 58\.88   | 55\.28  | 3          | 2       |
| o3-mini                | 80\.95   | 77\.61  | 45\.76   | 43\.47  | 78\.12     | 75\.12  | 68\.28   | 65\.40  | 1          | 1       |
| *DeepTheorem-RL-7B     | 55\.56   | 39\.07  | 28\.81   | 20\.85  | 57\.29     | 42\.20  | 47\.22   | 34\.04  | 5          | 5       |



## Key Contributions 🌟

- **Dataset** 📚: A large, diverse, and high-quality collection of informal theorems and proofs, enabling scalable training and evaluation of LLMs.
- **RL-Zero Strategy** 🤖: A reinforcement learning approach that significantly enhances LLM performance in informal theorem proving.
- **Evaluation Framework** 📏: Comprehensive metrics for both correctness and reasoning quality, setting a new standard for ATP evaluation.
- **Performance** 🏆: DeepTheorem achieves **state-of-the-art accuracy and reasoning quality**, outperforming existing datasets and supervised fine-tuning protocols.






## DeepTheorem Dataset 📊

The DeepTheorem dataset comprises **138K IMO-level informal theorems and proofs** spanning diverse mathematical domains 🌐. Each theorem-proof pair is rigorously annotated for:
- **o3-mini Proofs** 🖋️: Ensuring mathematical accuracy through proofs generated or verified by the o3-mini model ✅.
- **Truth Value** 🔍: The truth value of the theorem extracted from the o3-mini proofs, indicating whether the theorem is true or false ✔️.
- **Difficulty** 🎚️: Categorized by complexity to suit various LLM capabilities 🧩.
- **Topic Categories** 🗂️: Covering algebra, geometry, number theory, and more 📘.
- **Variants** 🔄: Positive or negative variants of the theorem that share the same or inverse truth value of the original theorem 🔀.

The dataset also includes **verifiable theorem variants**, systematically constructed to enable robust evaluation and training 🔍.

- **Access** 🔗: Download the dataset from [Dataset Link](#) or the `data/` directory.
- **Format** 📄: JSON files with theorem statements, proofs, annotations, and variants.
- **Usage** 🚀: Use the dataset for training, evaluation, or mathematical exploration. See `examples/` for sample theorems and proofs.

## DeepTheorem RL-Zero Training Pipeline ⚙️

The RL-Zero strategy is a reinforcement learning approach tailored for informal theorem proving 🤖. It leverages the dataset’s verified theorem variants to incentivize robust mathematical inference 💡.

- **Implementation** 🛠️: Available in the `models/` directory. See [RL-Zero Documentation](#) for details.
- **Training** 🚂:
  ```bash
  python scripts/train_rl_zero.py --dataset data/theorems.json --output models/rl_zero_model
