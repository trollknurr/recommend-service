import torch

from domains.recommend.adapter.output.torch_infer import Model


def test_model_infer() -> None:
    model = Model()
    user_history = torch.tensor([1, 2, 3, 4])

    recommendations = model(user_history)

    assert torch.equal(recommendations, torch.tensor([5510, 1021, 9640, 1682, 2544, 3281, 874, 8599, 3572, 2766]))
