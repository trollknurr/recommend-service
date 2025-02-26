from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = Field(default="dev")
    LOG_LEVEL: str = Field(default="INFO")

    GRPC_PORT: int = Field(default=50051)
    GRPC_MAX_WORKERS: int = Field(default=10)
    GRPC_TOKEN: SecretStr | None = Field(default=None)

    PROJECT_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    ONNX_MODEL_PATH: Path = Field(default=Path("weights/model.onnx"))

    NUM_RECOMMENDATIONS: int = Field(default=10)
    DEVICE: str = Field(default="cpu")
