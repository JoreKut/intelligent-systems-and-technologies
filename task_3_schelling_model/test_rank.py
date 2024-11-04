from main import SchellingModel, EntitiesFractionConfig
import numpy as np

import pytest

matrix_pair_1 = (
    np.array([
        [1, 0, 1],
        [-1, 0, -1],
        [1, 1, 0],
    ]),
    np.array([
        [0., -1., 0.],
        [0., -1., 0.],
        [1., 1., -1.],
    ])
)

matrix_pair_2 = (
    np.array([[0, 0, -1, 0, -1],
              [0, 0, 1, -1, -1],
              [1, 1, 0, 1, -1],
              [1, 1, -1, 0, -1],
              [-1, 0, 0, 0, -1]]),

    np.array([[-1., -1., 1., -1., 2.],
              [-1., -1., 2., 4., 3.],
              [3., 4., -1., 1., 3.],
              [3., 3., 0., -1., 2.],
              [0., -1., -1, -1., 1.]])
)


@pytest.mark.parametrize(
    ("field_matrix", 'rank_matrix'),
    [
        matrix_pair_1,
        matrix_pair_2,
    ]
)
def test_rank_calculation(
        field_matrix, rank_matrix
):
    entity_fraction_config = EntitiesFractionConfig(red_fraction=0.5, blue_fraction=0.5)
    model = SchellingModel(n=10, entity_fraction_config=entity_fraction_config, empty_fraction=0.1)

    result = model.calculate_ranks(field_matrix)
    assert (result == rank_matrix).all()
