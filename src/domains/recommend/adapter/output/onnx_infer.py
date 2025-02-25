from pathlib import Path

import onnxruntime as ort

ort.set_seed(0)


class OnnxInfer:
    def __init__(self, model_path: Path) -> None:
        self.session = ort.InferenceSession(str(model_path))

    def infer(self, user_history: list[int]) -> list[int]:
        result = self.session.run(None, {"user_history": user_history})
        return result[0].tolist()
