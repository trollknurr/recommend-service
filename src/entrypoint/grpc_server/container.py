from pathlib import Path

from dependency_injector import containers, providers

from domains.recommend.adapter.input.grpc_recommend import RecommendGrpcService
from domains.recommend.adapter.output.onnx_infer import OnnxInfer
from domains.recommend.port.output.infer import Infer
from domains.recommend.service.recommend import RecommendService
from entrypoint.config import Config
from entrypoint.logging import config_logger


def onnx_model_path(config: Config) -> Path:
    model_path = config.PROJECT_DIR / config.WEIGHTS_DIR / f"{config.NUM_RECOMMENDATIONS}_model.onnx"
    if not model_path.exists():
        msg = f"Model file not found: {model_path}"
        raise RuntimeError(msg)

    return model_path


def torch_infer(config: Config) -> Infer:
    from domains.recommend.adapter.output.torch_infer import TorchInfer

    return TorchInfer(num_recommendations=config.NUM_RECOMMENDATIONS, device=config.DEVICE)


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
    torch_infer = providers.Singleton(torch_infer, config=config)

    service = providers.Singleton(RecommendService, infer=onnx_infer)
    grpc_service = providers.Singleton(RecommendGrpcService, recommend_service=service)
