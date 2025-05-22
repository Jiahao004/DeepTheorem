set -e
set -u

RUN_NAME=verl-llm.qwen-2_5-3b+data.deeptheorem+alg.grpo
DATA_DIR=deeptheorem
MODEL_DIR=your_model_dir
OUTPUT_DIR=your_output_dir
REWARD_FUNC=reward_func_proof.py
NUM_NODES=2

mkdir -p .checkpoints/$RUN_NAME

ray job submit --address="http://127.0.0.1:8265" \
    --runtime-env-json='{
    "env_vars": {
        "NCCL_NET_GDR_READ": "1",
        "NCCL_IB_TIMEOUT": "24",
        "NCCL_IB_GID_INDEX": "3",
        "NCCL_IB_SL": "3",
        "NCCL_CHECKS_DISABLE": "1",
        "NCCL_P2P_DISABLE": "0",
        "NCCL_LL_THRESHOLD": "16384",
        "NCCL_IB_CUDA_SUPPORT": "1",
        "NCCL_SOCKET_IFNAME": "eth1",
        "NCCL_IB_HCA": "mlx5_2:1",
        "HUGGING_FACE_HUB_TOKEN": "your_hf_token",
        "LM_HARNESS_CACHE_PATH": "cache",
        "VLLM_ATTENTION_BACKEND": "XFORMERS",
        "PYTHONUNBUFFERED": "1",
        "WANDB_API_KEY": "your_wandb_key"
    },
    "working_dir": "./",
    "pip": ["latex2sympy2", "word2number", "timeout_decorator"]
    }' -- PYTHONUNBUFFERED=1 python3 -m verl.trainer.main_ppo \
    data.train_files=$DATA_DIR/train.parquet \
    data.val_files=$DATA_DIR/test.parquet \
    data.prompt_key=prompt \
    data.train_batch_size=128 \
    data.val_batch_size=128 \
    data.max_prompt_length=2048 \
    data.max_response_length=8192 \
    algorithm.adv_estimator=grpo \
    algorithm.kl_ctrl.kl_coef=0.0 \
    actor_rollout_ref.actor.entropy_coeff=0.0 \
    actor_rollout_ref.model.path=$MODEL_DIR \
    actor_rollout_ref.model.use_remove_padding=True \
    actor_rollout_ref.actor.optim.lr=1e-6 \
    actor_rollout_ref.actor.optim.lr_warmup_steps_ratio=0.05 \
    actor_rollout_ref.actor.ppo_mini_batch_size=128 \
    actor_rollout_ref.actor.use_dynamic_bsz=True \
    actor_rollout_ref.actor.ppo_max_token_len_per_gpu=10240 \
    actor_rollout_ref.actor.use_kl_loss=False \
    actor_rollout_ref.actor.kl_loss_coef=0.0 \
    actor_rollout_ref.actor.fsdp_config.param_offload=False \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \
    actor_rollout_ref.rollout.temperature=1.0 \
    actor_rollout_ref.rollout.top_p=1.0 \
    actor_rollout_ref.rollout.n=64 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.5 \
    actor_rollout_ref.rollout.disable_log_stats=False \
    actor_rollout_ref.rollout.log_prob_max_token_len_per_gpu=10240 \
    actor_rollout_ref.rollout.enforce_eager=False \
    actor_rollout_ref.rollout.free_cache_engine=False \
    actor_rollout_ref.ref.fsdp_config.param_offload=False \
    actor_rollout_ref.ref.log_prob_max_token_len_per_gpu=10240 \
    reward_model.reward_func_path=$REWARD_FUNC \
    trainer.project_name=verl \
    trainer.experiment_name=$RUN_NAME \
    trainer.default_local_dir=$OUTPUT_DIR \
    trainer.logger=['console','wandb'] \
    +trainer.val_before_train=False \
    trainer.n_gpus_per_node=8 \
    trainer.nnodes=$NUM_NODES \
    trainer.save_freq=5 \
    trainer.save_rollout=True \
    trainer.test_freq=999999 \
    trainer.total_epochs=999999 \
    trainer.total_training_steps=1000 \
    trainer.resume_mode=auto \
    2>&1 | tee -a .checkpoints/$RUN_NAME/train.log
