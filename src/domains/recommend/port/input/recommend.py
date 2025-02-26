import abc

from pydantic import BaseModel

from domains.recommend.domain.models import UserHistory, UserRecommendation


class RecommendRequest(BaseModel):
    user_history: UserHistory


class RecommendResponse(BaseModel):
    recommendations: UserRecommendation


class Recommend(abc.ABC):
    @abc.abstractmethod
    def recommend(self, request: RecommendRequest) -> RecommendResponse:
        pass
