from pathlib import Path

import onnxruntime as ort
from loguru import logger

from domains.recommend.domain.models import UserHistory, UserRecommendation
from domains.recommend.port.output.infer import Infer, InferError


class OnnxInfer(Infer):
    def __init__(self, model_path: Path, device: str = "cpu") -> None:
        ort.set_seed(0)
        match device:
            case "cpu":
                providers = ["CPUExecutionProvider"]
            case "cuda":
                providers = ["CUDAExecutionProvider"]
            case "mps":
                providers = ["CoreMLExecutionProvider"]
            case _:
                msg = f"Invalid device: {device}"
                raise ValueError(msg)

        logger.info(f"Load model {model_path}, configured providers: {providers}")
        self.session = ort.InferenceSession(str(model_path), providers=providers)
        actual_providers = self.session.get_providers()
        if actual_providers != providers:
            logger.warning(f"Session providers: {actual_providers}, expected: {providers}")

    def infer(self, user_history: UserHistory) -> UserRecommendation:
        try:
            result = self.session.run(None, {"user_history": user_history.item_ids})
            item_ids = result[0].tolist()
            return UserRecommendation(item_ids=item_ids)

        except Exception as e:
            raise InferError(e) from e
