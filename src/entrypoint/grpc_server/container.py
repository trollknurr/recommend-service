from pathlib import Path

from dependency_injector import containers, providers

from domains.recommend.adapter.input.grpc_recommend import RecommendGrpcService
from domains.recommend.adapter.output.onnx_infer import OnnxInfer
from domains.recommend.service.recommend import RecommendService
from entrypoint.config import Config
from entrypoint.logging import config_logger


def onnx_model_path(config: Config) -> Path:
    return config.PROJECT_DIR / config.WEIGHTS_DIR / f"{config.NUM_RECOMMENDATIONS}_model.onnx"


class Container(containers.DeclarativeContainer):
    config = Config()
    config_obj = providers.Object(config)

    logger = providers.Resource(config_logger, level=config.LOG_LEVEL, env=config.ENV)
    onnx_model_path = providers.Resource(onnx_model_path, config=config)

    onnx_infer = providers.Singleton(
        OnnxInfer,
        model_path=onnx_model_path,
        device=config.DEVICE,
    )

    service = providers.Singleton(RecommendService, infer=onnx_infer)
    grpc_service = providers.Singleton(RecommendGrpcService, recommend_service=service)
