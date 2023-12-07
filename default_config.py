from pprint import pformat
from typing import Literal

from pydantic import BaseModel, ConfigDict, computed_field


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    app_title: str = "Nerd Fonts Icon Search API Documentation"
    """ model config

    huggingface_api_key
      - set a valid huggingface_api_key
        - use local model to populate the database (faster)
        - use cloud model to search (less resources)
      - unset huggingface_api_key
        - always use local model

    huggingface_model
     - https://huggingface.co/sentence-transformers
     - https://www.sbert.net/docs/pretrained_models.html

    device
      - cpu
      - cuda, you need to install pytorch with cuda support, see https://pytorch.org/

    frontend_host
    frontend_port
      - used to set the CORS policy
    """
    huggingface_api_key: str | None = None
    huggingface_model: str = "distiluse-base-multilingual-cased-v2"
    device: Literal["cpu", "cuda"] = "cpu"
    frontend_host: str = "localhost"
    frontend_port: int = 3000

    @computed_field
    def allow_origins(self) -> list[str]:
        netloc = f"{self.frontend_host}:{self.frontend_port}"
        return [f"http://{netloc}", f"https://{netloc}"]

    def __str__(self) -> str:
        return pformat(self.model_dump(), indent=2)
