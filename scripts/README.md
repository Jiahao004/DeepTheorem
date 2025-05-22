## DeepTheorem RL-Zero Training Pipeline

- Download a qwen2.5 base model from Hugging Face, and replace `tokenizer_config.json` with [this file](tokenizer_config.json).

- Download the DeepTheorem dataset:

        mkdir deeptheorem
        huggingface-cli download --repo-type dataset Jiahao004/DeepTheorem --local-dir deeptheorem

- Preprocess the dataset into parquet format for training:

        python preprocess_data.py

- Prepare the training environment:
    - we use a modified version of verl for RL-Zero training. Install it with `git clone -b simplerl https://github.com/zwhe99/verl && cd verl && pip3 install -e . && cd ..`
    - these packages are also recommended: `pip3 install omegaconf==2.4.0.dev3 hydra-core==1.4.0.dev1 antlr4-python3-runtime==4.11.0`

- Configure training arguments and environment variables in [`train_rl.sh`](train_rl.sh):
    - set your RUN_NAME, MODEL_DIR, OUTPUT_DIR, HUGGING_FACE_HUB_TOKEN, WANDB_API_KEY (and DATA_DIR if you have moved the data)
    - set the proper NCCL variables according to the type of GPU you are using (see [here](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html))
    - set NUM_NODES to the number of machines you are using

- Start ray sessions:
    - on the main node, run `ray start  --head --port=6379  --node-ip-address=$HEAD_NODE_IP`
    - on the other nodes, run `ray start  --address=$HEAD_NODE_IP:6379 --node-ip-address=$THIS_WORKER_IP`

- Start training:
    - on the main node, run `bash train_rl.sh`
    - use [this script](https://github.com/volcengine/verl/blob/main/scripts/model_merger.py) to convert saved checkpoints into Hugging Face format.
