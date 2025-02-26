import abc

from domains.recommend.domain.models import UserHistory, UserRecommendation


class Infer(abc.ABC):
    @abc.abstractmethod
    def infer(self, user_history: UserHistory) -> UserRecommendation:
        pass
