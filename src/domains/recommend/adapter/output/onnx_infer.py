from pathlib import Path

import onnxruntime as ort

from domains.recommend.domain.models import UserHistory, UserRecommendation
from domains.recommend.port.output.infer import Infer


class OnnxInfer(Infer):
    def __init__(self, model_path: Path, num_recommendations: int, device: str = "cpu") -> None:
        ort.set_seed(0)
        # TODO: учитывать device и num_recommendations
        # TODO: проверить, что cuda и mps есть провайдеры и кидать ошибку
        self.session = ort.InferenceSession(str(model_path))

    def _infer(self, user_history: list[int]) -> list[int]:
        result = self.session.run(None, {"user_history": user_history})
        return result[0].tolist()

    def infer(self, user_history: UserHistory) -> UserRecommendation:
        return UserRecommendation(item_ids=self._infer(user_history.item_ids))
