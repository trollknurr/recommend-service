import pytest

from domains.recommend.domain.models import UserHistory
from domains.recommend.port.output.infer import InferError
from entrypoint.grpc_server.container import Container
from recommend.adapter.output.conftest import ERROR_INPUTS, ETHALON_PAIRS

torch = pytest.importorskip("torch")


@pytest.mark.parametrize(("user_history", "recommendations"), ETHALON_PAIRS)
def test_model_infer(user_history: list[int], recommendations: list[int], test_container: Container) -> None:
    from domains.recommend.adapter.output.torch_infer import TorchInfer

    config = test_container.config_obj()
    infer = TorchInfer(num_recommendations=config.NUM_RECOMMENDATIONS, device=config.DEVICE)

    predictions = infer.infer(UserHistory(item_ids=user_history))

    assert set(predictions.item_ids) == set(recommendations)


@pytest.mark.parametrize("user_history", ERROR_INPUTS)
def test_model_infer_error(user_history: list[int], test_container: Container) -> None:
    from domains.recommend.adapter.output.torch_infer import TorchInfer

    config = test_container.config_obj()
    infer = TorchInfer(num_recommendations=config.NUM_RECOMMENDATIONS, device=config.DEVICE)

    with pytest.raises(InferError):
        infer.infer(UserHistory(item_ids=user_history))
