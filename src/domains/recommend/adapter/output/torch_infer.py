import torch

from domains.recommend.domain.models import UserHistory, UserRecommendation
from domains.recommend.port.output.infer import Infer, InferError

torch.manual_seed(0)


class Model(torch.nn.Module):
    def __init__(self, num_recommendations: int = 10, device: str = "cpu") -> None:
        super().__init__()
        self._item_embeddings = torch.rand((10000, 32), device=device)
        self._num_recommendations = num_recommendations

    def forward(self, user_history: torch.Tensor) -> torch.Tensor:
        user_embedding = self._item_embeddings[user_history].mean(dim=0)
        scores = user_embedding @ self._item_embeddings.T
        topk = torch.topk(scores, k=self._num_recommendations)
        return topk.indices


class TorchInfer(Infer):
    def __init__(self, num_recommendations: int, device: str = "cpu") -> None:
        self._model = Model(num_recommendations, device)
        self._device = device

    def infer(self, user_history: UserHistory) -> UserRecommendation:
        try:
            t_user_history = torch.tensor(user_history.item_ids, device=self._device)
            with torch.no_grad():
                t_recommendations = self._model(t_user_history)
            t_recommendations = t_recommendations.cpu().tolist()

            return UserRecommendation(item_ids=t_recommendations)
        except Exception as e:
            raise InferError(e) from e
