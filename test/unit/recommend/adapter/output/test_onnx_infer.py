import pytest

from domains.recommend.domain.models import UserHistory
from domains.recommend.port.output.infer import InferError
from entrypoint.grpc_server.container import Container
from unit.recommend.adapter.output.conftest import ERROR_INPUTS, ETHALON_PAIRS


@pytest.mark.parametrize(("user_history", "recommendations"), ETHALON_PAIRS)
def test_onnx_model_infer(test_container: Container, user_history: list[int], recommendations: list[int]) -> None:
    onnx_infer = test_container.onnx_infer()

    predictions = onnx_infer.infer(UserHistory(item_ids=user_history))

    assert set(predictions.item_ids) == set(recommendations)


@pytest.mark.parametrize("user_history", ERROR_INPUTS)
def test_onnx_model_infer_error(test_container: Container, user_history: list[int]) -> None:
    onnx_infer = test_container.onnx_infer()

    with pytest.raises(InferError):
        onnx_infer.infer(UserHistory(item_ids=user_history))
