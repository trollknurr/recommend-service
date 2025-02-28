import click
import grpc
from loguru import logger

from grpc_proto.recommend_api.v1 import recommend_api_pb2, recommend_api_pb2_grpc

EXAMPLES = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [0],
    [1, 1, 1, 1],
    [9999, 999, 99],
]


@click.command()
@click.option("--host", default="localhost", help="GRPC host")
@click.option("--port", default=50051, help="GRPC port")
def main(host: str, port: int) -> None:
    if host != "localhost":
        channel = grpc.secure_channel(host, grpc.ssl_channel_credentials())
    else:
        channel = grpc.insecure_channel(f"{host}:{port}")

    stub = recommend_api_pb2_grpc.RecommenderServiceStub(channel)

    for example in EXAMPLES:
        response = stub.Recommend(recommend_api_pb2.RecommendRequest(item_ids=example))
        logger.info(f"Recommendations for {example}: {response.item_ids}")


if __name__ == "__main__":
    main()
