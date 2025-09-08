import json
import litellm
import logging
import os
from dataclasses import asdict, dataclass, field
from minisweagent.models import GLOBAL_MODEL_STATS
from pathlib import Path
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from typing import Any

class LogFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        return "RAW RESPONSE:" in message or "Request Sent from LiteLLM:" in message
    
logging.basicConfig(filename='out/litellm.log', level=logging.DEBUG)
litellm.set_verbose = True
logger = logging.getLogger("litellm_model")
logger.handlers = [logging.FileHandler('out/litellm.log')]
logger.addFilter(LogFilter())
logger.propagate = False 

@dataclass
class LitellmModelConfig:
    model_name: str
    model_kwargs: dict[str, Any] = field(default_factory=dict)
    litellm_model_registry: Path | str | None = os.getenv("LITELLM_MODEL_REGISTRY_PATH")


class LitellmModel:
    def __init__(self, **kwargs):
        self.config = LitellmModelConfig(**kwargs)
        self.cost = 0.0
        self.n_calls = 0
        if self.config.litellm_model_registry and Path(self.config.litellm_model_registry).is_file():
            litellm.utils.register_model(json.loads(Path(self.config.litellm_model_registry).read_text()))

    @retry(
        stop=stop_after_attempt(20),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        retry=retry_if_not_exception_type(
            (
                litellm.exceptions.UnsupportedParamsError,
                litellm.exceptions.NotFoundError,
                litellm.exceptions.PermissionDeniedError,
                litellm.exceptions.ContextWindowExceededError,
                litellm.exceptions.APIError,
                litellm.exceptions.AuthenticationError,
                KeyboardInterrupt,
            )
        ),
    )
    def _query(self, messages: list[dict[str, str]], **kwargs):
        try:
            return litellm.completion(
                model=self.config.model_name, messages=messages, **(self.config.model_kwargs | kwargs)
            )
        except litellm.exceptions.AuthenticationError as e:
            e.message += " You can permanently set your API key with `mini-extra config set KEY VALUE`."
            raise e

    def query(self, messages: list[dict[str, str]], **kwargs) -> dict:
        response = self._query(messages, **kwargs)
        try:
            cost = litellm.cost_calculator.completion_cost(response)
        except Exception as e:
            logger.critical(
                f"Error calculating cost for model {self.config.model_name}: {e}. "
                "Please check the 'Updating the model registry' section in the documentation. "
                "http://bit.ly/4p31bi4 Still stuck? Please open a github issue for help!"
            )
            raise
        self.n_calls += 1
        self.cost += cost
        has_thoughts = hasattr(response.choices[0].message, "reasoning_content") and len(response.choices[0].message.reasoning_content)
        GLOBAL_MODEL_STATS.add(cost, has_thoughts)
        return {
            "content": self.replace_reasoning_tag_with_thought_summaries(response)
        }

    def split_reasoning(self, text) -> tuple[str, str]:
        opening_tag = f"<reasoning>"
        closing_tag = f"</reasoning>"
        start_pos = text.find(opening_tag)
        content_start = start_pos + len(opening_tag)
        end_pos = text.find(closing_tag, content_start)
        if start_pos < 0 or end_pos < 0 or start_pos > end_pos:
            return text, ''
        reasoning = text[content_start:end_pos]
        return reasoning, text[end_pos + len(closing_tag):]

    # Experiment: if the response includes message.reasoning_content, use summarized thoughts instead of <reasoning>
    # This trick seems to improve SWE-bench scores by ~1%
    def replace_reasoning_tag_with_thought_summaries(self, response) -> str:
        content = response.choices[0].message.content
        if content and hasattr(response.choices[0].message, "reasoning_content"):
            thought_summary = response.choices[0].message.reasoning_content
            reasoning, bash_command = self.split_reasoning(content or "")
            if reasoning and thought_summary and len(thought_summary) > len(reasoning):
                # replace the content of the <reasoning> tag with the more robust thought summaries
                return f"<reasoning>\n{thought_summary}\n</reasoning>\n{bash_command}"
        return content

    def get_template_vars(self) -> dict[str, Any]:
        return asdict(self.config) | {"n_model_calls": self.n_calls, "model_cost": self.cost}
