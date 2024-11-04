import random

import numpy
import pandas as pd
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
    satisfy_threshold = 2  # number of entities with the same type

    RED_mark_icon = '🛑'
    BLUE_mark_icon = '🟦'
    FREE_mark_icon = '⬜️'

    free_place_symbols = [FREE_mark_icon, empty_mark]

    def __init__(self, n: int, entity_fraction_config: EntitiesFractionConfig, empty_fraction, web_view=False):
        self.n = n
        self.size = n * n
        self.red_fraction = entity_fraction_config.red_fraction * (1 - empty_fraction)
        self.blue_fraction = entity_fraction_config.blue_fraction * (1 - empty_fraction)
        self.empty_fraction = empty_fraction

        # used for field map for output view
        if web_view:
            # Number representation
            self.marks = [self.red_mark, self.blue_mark, self.empty_mark]
        else:
            self.marks = [self.RED_mark_icon, self.BLUE_mark_icon, self.FREE_mark_icon]

        # percentage for each group
        self.p = [self.red_fraction, self.blue_fraction, self.empty_fraction]

        self.field_items = np.random.choice(self.marks, size=self.size, p=self.p)

        # used to output and build ranks matrix
        self.field: np.ndarray = np.reshape(self.field_items, (n, n))

        # used to determine satisfaction-level
        self.ranks = self.calculate_ranks(self.field)

        self.iteration_count = 0

    def get_unsatisfied_condition(self):
        return (self.ranks != -1) & (self.ranks < self.satisfy_threshold)

    def do_iteration(self):
        """
            move not-satisfied to free space
        """
        # get coord of non-satisfied cells
        unsatisfied_i_indices, unsatisfied_j_indices = np.where(self.get_unsatisfied_condition())
        unsatisfied_entities_coords = list(zip(unsatisfied_i_indices, unsatisfied_j_indices))

        # get coord of free_place cells
        free_i_indices, free_j_indices = np.where(self.ranks == -1)
        free_place_coords = list(zip(free_i_indices, free_j_indices))

        while unsatisfied_entities_coords and free_place_coords:
            # get random object from selection
            unsatisfied_entity_coord = random.choice(unsatisfied_entities_coords)
            free_place_coord = random.choice(free_place_coords)

            # change cell's values
            self.swap_cells(unsatisfied_entity_coord, free_place_coord)

            # pop objects from lists
            unsatisfied_entities_coords.remove(unsatisfied_entity_coord)
            free_place_coords.remove(free_place_coord)

            # push new free place
            free_place_coords.append(unsatisfied_entity_coord)

        self.iteration_count += 1

    def calculate_ranks(self, field: np.ndarray) -> numpy.ndarray:
        """
            calc entities satisfy value
        """
        pad: np.ndarray = np.pad(field, 1)
        ranks: np.ndarray = np.zeros(field.shape)
        n, m = field.shape
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                similar_object_count = np.sum(pad[i - 1:i + 2, j - 1:j + 2] == pad[i, j]) - 1
                if pad[i, j] in self.free_place_symbols:
                    similar_object_count = -1
                ranks[i - 1, j - 1] = similar_object_count

        return ranks

    def swap_cells(self, coord1: np.ndarray, coord2: np.ndarray):
        """Swap two coord value"""
        self.field[coord1], self.field[coord2] = self.field[coord2], self.field[coord1]

    def recalculate_ranks(self) -> None:
        self.ranks = self.calculate_ranks(self.field)

    def get_unsatisfied_count(self):
        return np.sum(self.get_unsatisfied_condition())

    def is_everyone_satisfied(self) -> bool:
        return self.get_unsatisfied_count() == 0

    def print_field(self):
        print(self.pretty_output(self.field))

    def print_info(self):
        print("\nRESULT")
        self.print_field()
        print("Iteration:", self.iteration_count)
        print('Unsatisfied entities =', self.get_unsatisfied_count())

    @staticmethod
    def pretty_output(field):
        separated_strings = ["".join(field[:, i].ravel()) for i in range(field.shape[0])]
        return "\n".join(separated_strings)

    @staticmethod
    def rank_output(rank: np.ndarray):
        output_rank = rank.copy()
        critical_map = {
            0: "0️⃣",
            1: "1️⃣",
        }
        df = pd.DataFrame(output_rank)
        df = df.replace(critical_map)
        return df.values
