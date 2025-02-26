from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger

from entrypoint.auth import StaticTokenValidationInterceptor
from entrypoint.grpc_server.container import Container
from grpc_proto.recommend_api.v1 import recommend_api_pb2, recommend_api_pb2_grpc


def main() -> None:
    container = Container()
    container.init_resources()
    config = container.config_obj()

    logger.info("GRPC server starting...")
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=config.GRPC_MAX_WORKERS),
        interceptors=(
            StaticTokenValidationInterceptor(config.GRPC_TOKEN.get_secret_value()) if config.GRPC_TOKEN else None
        ),
    )
    recommend_api_pb2_grpc.add_RecommenderServiceServicer_to_server(
        container.grpc_service(),
        server,
    )
    service_names = (
        recommend_api_pb2.DESCRIPTOR.services_by_name["RecommenderService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    port = server.add_insecure_port(f"[::]:{config.GRPC_PORT}")
    server.start()
    logger.info(f"GRPC server started on port {port}!")
    server.wait_for_termination()


if __name__ == "__main__":
    main()
