from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    ONNX_MODEL_PATH: Path = Field(default=Path("weights/model.onnx"))
