# DeCO

Core implementation of **DeCO: A training-free framework for
in-context knowledge editing via incremental reasoning**.

## How to Run?

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### OpenRouter

```bash
export OPENROUTER_API_KEY=your_key
export OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
python main.py \
  --backend openrouter
```

### DMX

```bash
export DMX_API_KEY=your_key
export DMX_MODEL=qwen2.5-14b-instruct
python main.py \
  --backend dmx
```

### Local vLLM

```bash
export VLLM_BASE_URL=http://127.0.0.1:8000/v1
export VLLM_MODEL=qwen

python main.py \
  --backend vllm
```

You can edit the config in the ```config.py``` file.

Question-level evaluation runs concurrently. Conflict checks inside one
reasoning step also run concurrently. Contriever GPU inference is protected by
a lock because all workers share one model instance.
