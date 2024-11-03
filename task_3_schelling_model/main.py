from pydantic import BaseModel
import numpy as np


class EntitiesFractionConfig(BaseModel):
    """
        red_fraction + blue_fraction = 100%
    """
    red_fraction: float
    blue_fraction: float


class SchellingModel:
    red_mark = -1
    blue_mark = 1
    empty_mark = 0

    def __init__(self, n: int, entity_fraction_config: EntitiesFractionConfig, empty_fraction):
        self.n = n
        self.size = n*n
        self.red_fraction = entity_fraction_config.red_fraction * (1 - empty_fraction)
        self.blue_fraction = entity_fraction_config.blue_fraction * (1 - empty_fraction)
        self.empty_fraction = empty_fraction

        self.marks = [self.red_mark, self.blue_mark, self.empty_mark]
        self.p = [self.red_fraction, self.blue_fraction, self.empty_fraction]

        self.field_items = np.random.choice(self.marks, size=self.size, p=self.p)
        self.field = np.reshape(self.field_items, (n, n))
        self.ranks = self.field

    def do_iteration(self):
        ...

    def recalculate_ranks(self) -> None:
        ...

    def get_satisfied_count(self) -> int:
        ...

    def is_everyone_satisfied(self) -> bool:
        ...


def main():
    entity_fraction_config = EntitiesFractionConfig(
        red_fraction=0.4,
        blue_fractino=0.6,
    )
    model_map = SchellingModel(
        n=40,
        entity_fraction_config=entity_fraction_config,
        empty_fraction=0.2
    )
    while True:
        model_map.do_iteration()
        model_map.recalculate_ranks()

        if model_map.is_everyone_satisfied():
            break


if __name__ == '__main__':
    main()
