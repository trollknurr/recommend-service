import torch

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
