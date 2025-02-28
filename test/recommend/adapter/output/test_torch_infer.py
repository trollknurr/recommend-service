import pytest

torch = pytest.importorskip("torch")

from domains.recommend.domain.models import UserHistory
from domains.recommend.port.output.infer import InferError
from entrypoint.grpc_server.container import Container
from recommend.adapter.output.conftest import ERROR_INPUTS, ETHALON_PAIRS


@pytest.mark.parametrize(("user_history", "recommendations"), ETHALON_PAIRS)
def test_model_infer(user_history: list[int], recommendations: list[int], test_container: Container) -> None:
    infer = test_container.torch_infer()

    predictions = infer.infer(UserHistory(item_ids=user_history))

    assert set(predictions.item_ids) == set(recommendations)


@pytest.mark.parametrize("user_history", ERROR_INPUTS)
def test_model_infer_error(user_history: list[int], test_container: Container) -> None:
    infer = test_container.torch_infer()

    with pytest.raises(InferError):
        infer.infer(UserHistory(item_ids=user_history))
