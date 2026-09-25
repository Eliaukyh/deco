import re


REFUSAL_OR_DENIAL_PATTERN = re.compile(
    r"\b(?:not|cannot|can't|unable|refuse|refused|incorrect|"
    r"inconsistent|contradict|contradicts|contradictory)\b",
    flags=re.IGNORECASE,
)


def contains_refusal_or_denial(answer):
    if answer is None:
        return False
    return REFUSAL_OR_DENIAL_PATTERN.search(answer) is not None
