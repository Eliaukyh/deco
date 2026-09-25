import random
import time

from deco.config import API_RETRY_BASE_SECONDS


def sleep_backoff(attempt):
    delay = API_RETRY_BASE_SECONDS * (2 ** attempt) + random.random() * 0.5
    time.sleep(delay)
