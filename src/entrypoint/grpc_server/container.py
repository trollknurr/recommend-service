from dependency_injector import containers, providers

from domains.recommend.adapter.input.grpc_recommend import RecommendGrpcService
from domains.recommend.adapter.output.onnx_infer import OnnxInfer
from domains.recommend.adapter.output.torch_infer import TorchInfer
from domains.recommend.service.recommend import RecommendService
from entrypoint.config import Config
from entrypoint.logging import config_logger


class Container(containers.DeclarativeContainer):
    config = Config()
    config_obj = providers.Object(config)

    logger = providers.Resource(config_logger, level=config.LOG_LEVEL, env=config.ENV)

    torch_infer = providers.Singleton(TorchInfer, num_recommendations=config.NUM_RECOMMENDATIONS, device=config.DEVICE)
    onnx_infer = providers.Singleton(
        OnnxInfer,
        model_path=config.ONNX_MODEL_PATH,
        num_recommendations=config.NUM_RECOMMENDATIONS,
        device=config.DEVICE,
    )

    service = providers.Singleton(RecommendService, infer=torch_infer)
    grpc_service = providers.Singleton(RecommendGrpcService, recommend_service=service)
