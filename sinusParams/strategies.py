from abc import ABC, abstractmethod

# from .sinusParams import SinusParamsAdjuster
from .typing import SinParameters, SinWithParameters
from random import random, randint, sample, shuffle, uniform
from typing import Callable, List
import math
from . import helpers


class ParamsAdjustingStrategy(ABC):
    @abstractmethod
    def __init__(
        self,
        sin_func: SinWithParameters,
        similarity_threshold: float,
    ):
        pass

    @abstractmethod
    def perform_algorithm(self) -> None:
        pass

    @abstractmethod
    def get_params_and_similarity(self) -> tuple[SinParameters, float]:
        pass

    def set_adjuster(self) -> None:
        pass


class StrategyFactory:
    similarity_threshold: float

    def create_strategy(self, strategy_type: str) -> ParamsAdjustingStrategy:
        match strategy_type:
            case "evolutionary":
                return EvolutionaryStrategy(
                    self,
                    similarity_threshold=self.similarity_threshold,
                    population_number=200,
                )
            case _:
                raise ValueError(f"{strategy_type} is not allowed strategy type")


class EvolutionaryStrategy(ParamsAdjustingStrategy):
    def __init__(
        self,
        adjuster,  # : SinusParamsAdjuster,
        *,
        similarity_threshold: float,
        population_number: int,
        mutation_chance: float = 0.2,
    ):
        self.adjuster = adjuster
        self.similarity = 0.000001

        self.similarity_threshold = similarity_threshold
        self.mutation_chance = mutation_chance
        self.params_list = self.get_random_params_population(population_number)
        self.sort_params_list_by_accuracy()

    @staticmethod
    def get_random_params_population(population_number: int) -> List[SinParameters]:
        params_population = []
        for _ in range(population_number):
            params = [uniform(-2.5, 2.5) for _ in range(10)]
            params_population.append(params)
        return params_population

    def sort_params_list_by_accuracy(self):
        self.params_list.sort(key=self.points_to_graph_distance)

    def remove_bottom_population_half(self):
        number_of_survivors = len(self.params_list) // 2
        self.params_list = self.params_list[:number_of_survivors]

    # TODO: Maybe hermetization again
    def points_to_graph_distance(self, params: SinParameters) -> float:
        """Euclidian distance"""
        squared_diffs = 0
        for point in self.adjuster.points:
            perfect_y = point.y
            actual_y = self.adjuster.sin_with_params(point.x, *params)
            squared_diffs += (perfect_y - actual_y) ** 2

        return math.sqrt(squared_diffs)

    def populate_missing_params(self):
        shuffle(self.params_list)

        for i in range(0, len(self.params_list), 2):
            children1 = self.params_list[i].copy()
            children2 = self.params_list[i + 1].copy()

            gens_indexes_to_swap = sample([j for j in range(0, 10)], 5)

            helpers.swap_lists_on_indexes(
                children1, children2, indexes_to_swap=gens_indexes_to_swap
            )

            self.mutate_params(children1)
            self.mutate_params(children2)

            self.params_list.append(children1)
            self.params_list.append(children2)

    def mutate_params(self, params: SinParameters) -> None:
        for i in range(len(params)):
            if random() < self.mutation_chance:
                params[i] = self._mutate_param(params[i])

    @staticmethod
    def _mutate_param(param: float) -> float:
        if randint(1, 2) == 1:
            param *= 1.30
        elif randint(1, 2) == 1:
            param *= 0.7
        if randint(1, 2) == 1:
            param *= -1
        return param

    def perform_algorithm(self) -> None:
        i = 0
        while not self.similarity < self.similarity_threshold and i < 1_000:
            self.remove_bottom_population_half()
            self.populate_missing_params()
            self.sort_params_list_by_accuracy()
            self.similarity = 1 / self.points_to_graph_distance(self.params_list[0])
            i += 1

    def get_params_and_similarity(self):
        return self.params_list[0], self.similarity
