from pprint import pformat
from typing import Literal

from pydantic import BaseModel, ConfigDict, computed_field


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    """ model config
    set a valid huggingface_api_key:
      use local model to populate the database (faster)
      use cloud model to search (less memory)
    
    set huggingface_api_key to None,
      always use local model

    see the list of available model name at: https://huggingface.co/models
      """
    huggingface_api_key: str | None = None
    huggingface_model: str = "all-MiniLM-L6-v2"
    device: Literal["cpu", "cuda"] = "cpu"

    """backend server config

    the frontend_host and port will be used to set the CORS policy
    """
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    frontend_host: str = "localhost"
    frontend_port: int = 3000

    @computed_field
    def allow_origins(self) -> list[str]:
        netloc = f"{self.frontend_host}:{self.frontend_port}"
        return [
            f"{netloc}",
            f"http://{netloc}",
            f"https://{netloc}",
        ]

    def __str__(self) -> str:
        return pformat(self.model_dump(), indent=2)
