import grpc

from domains.recommend.domain.models import UserHistory
from domains.recommend.port.input.recommend import Recommend, RecommendRequest
from grpc_proto.recommend_api.v1 import recommend_api_pb2, recommend_api_pb2_grpc


class RecommendGrpcService(recommend_api_pb2_grpc.RecommenderServiceServicer):
    def __init__(self, recommend_service: Recommend) -> None:
        self._recommend_service = recommend_service

    def Recommend(  # noqa: N802
        self, request: recommend_api_pb2.RecommendRequest, context: grpc.ServicerContext
    ) -> recommend_api_pb2.RecommendResponse:
        response = self._recommend_service.recommend(
            RecommendRequest(user_history=UserHistory(item_ids=list(request.item_ids)))
        )
        return recommend_api_pb2.RecommendResponse(item_ids=response.recommendations.item_ids)
