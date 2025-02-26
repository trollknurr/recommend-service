from domains.recommend.port.input.recommend import Recommend, RecommendRequest, RecommendResponse
from domains.recommend.port.output.infer import Infer


class RecommendService(Recommend):
    def __init__(self, infer: Infer) -> None:
        self._infer = infer

    def recommend(self, request: RecommendRequest) -> RecommendResponse:
        user_history = request.user_history
        recommendations = self._infer.infer(user_history)
        return RecommendResponse(recommendations=recommendations)
