from deco.prompts.answer import (
    EXTRACT_ANSWER_TEMPLATE,
    FINAL_ANSWER_TEMPLATE,
    PREFILL_GUIDANCE,
)
from deco.prompts.conflict import CONFLICT_TEMPLATE, SELECT_CONFLICT_TEMPLATE
from deco.prompts.reasoning import FIRST_STEP_TEMPLATE, NEXT_STEP_TEMPLATE
from deco.prompts.render import render_prompt


__all__ = [
    "CONFLICT_TEMPLATE",
    "EXTRACT_ANSWER_TEMPLATE",
    "FINAL_ANSWER_TEMPLATE",
    "FIRST_STEP_TEMPLATE",
    "NEXT_STEP_TEMPLATE",
    "PREFILL_GUIDANCE",
    "SELECT_CONFLICT_TEMPLATE",
    "render_prompt",
]
