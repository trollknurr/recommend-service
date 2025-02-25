import onnx
import torch

from domains.recommend.adapter.output.torch_infer import Model
from entrypoint.config import Config


def main(config: Config) -> None:
    model = Model()
    torch.onnx.export(
        model,
        (torch.tensor([1, 2, 3, 4]),),
        config.PROJECT_DIR / config.ONNX_MODEL_PATH,
        input_names=["user_history"],
        output_names=["recommendations"],
    )

    onnx_model = onnx.load(config.PROJECT_DIR / config.ONNX_MODEL_PATH)
    onnx.checker.check_model(onnx_model)


if __name__ == "__main__":
    config = Config()
    main(config)
