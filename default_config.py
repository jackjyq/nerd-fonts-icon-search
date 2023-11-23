from pprint import pformat
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    # see the list of available model name at: https://huggingface.co/models
    huggingface_model: str = "all-MiniLM-L6-v2"

    # None always use local embedding function (consume more memory)
    huggingface_api_key: str | None = None

    device: Literal["cpu", "cuda"] = "cpu"

    def __str__(self) -> str:
        return pformat(self.model_dump(), indent=2)
