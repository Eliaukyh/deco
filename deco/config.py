import os


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "meta-llama/llama-3.1-8b-instruct",
)

DMX_API_KEY = os.getenv("DMX_API_KEY")
DMX_BASE_URL = os.getenv("DMX_BASE_URL", "https://www.dmxapi.com/v1")
DMX_MODEL = os.getenv("DMX_MODEL", "gpt-4o-mini")

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://127.0.0.1:8000/v1")
VLLM_MODEL = os.getenv("VLLM_MODEL", "qwen")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "EMPTY")
VLLM_MAX_TOKENS = int(os.getenv("VLLM_MAX_TOKENS", "512"))

QUESTION_WORKERS = int(os.getenv("QUESTION_WORKERS", "10"))
CONFLICT_WORKERS = int(os.getenv("CONFLICT_WORKERS", "30"))
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "5"))
API_RETRY_BASE_SECONDS = float(os.getenv("API_RETRY_BASE_SECONDS", "1.5"))
API_TIMEOUT_SECONDS = float(os.getenv("API_TIMEOUT_SECONDS", "120"))
