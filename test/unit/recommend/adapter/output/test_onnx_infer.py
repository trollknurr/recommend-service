from domains.recommend.adapter.output.onnx_infer import OnnxInfer
from entrypoint.config import Config


def test_onnx_model_infer(config: Config) -> None:
    onnx_infer = OnnxInfer(config.PROJECT_DIR / config.ONNX_MODEL_PATH, config.NUM_RECOMMENDATIONS)

    recommendations = onnx_infer._infer([1, 2, 3, 4])

    assert set(recommendations) == {5510, 1021, 9640, 1682, 2544, 3281, 874, 8599, 3572, 2766}
