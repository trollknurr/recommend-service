import onnx
import onnxruntime as ort
import torch
from loguru import logger

from domains.recommend.adapter.output.torch_infer import Model
from entrypoint.config import Config

torch.manual_seed(0)
ort.set_seed(0)


def main(config: Config) -> None:
    model = Model(config.NUM_RECOMMENDATIONS, config.DEVICE)
    model_path = config.PROJECT_DIR / config.WEIGHTS_DIR / f"{config.NUM_RECOMMENDATIONS}_model.onnx"
    torch.onnx.export(
        model,
        (torch.tensor([1, 2, 3, 4]),),
        model_path,
        input_names=["user_history"],
        output_names=["recommendations"],
        verbose=True,
        dynamic_axes={
            "user_history": {0: "history_size"},
        },
    )

    onnx_model = onnx.load(model_path)
    onnx.checker.check_model(onnx_model)

    logger.info(f"Model saved to {model_path}")
    predictions = model(torch.tensor([1, 2, 3]))
    logger.info(f"Torch predictions: {predictions.cpu().tolist()}")
    session = ort.InferenceSession(str(model_path))
    result = session.run(None, {"user_history": [1, 2, 3]})
    result = result[0].tolist()
    logger.info(f"ONNX predictions: {result}")


if __name__ == "__main__":
    config = Config()
    main(config)
