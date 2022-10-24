from collections.abc import Callable
from typing import List, Optional
from .typing import SinParameters
from dataclasses import dataclass
import numpy as np
from random import uniform
from .strategies import StrategyFactory


@dataclass
class Point:
    x: float
    y: float


class SinusParamsAdjuster(StrategyFactory):
    def __init__(
        self,
        adjusting_strategy_type: str,
        similarity_threshold: float,
        points: Optional[List[Point]] = None,
    ):
        self._params: Optional[SinParameters] = None
        self.distance: float
        self.distance_threshold = similarity_threshold
        self.points = get_random_points() if points is None else points
        self.adjusting_strategy = self.create_strategy(adjusting_strategy_type)

    def sin_with_params(self, x, a1, k1, p1, a2, k2, p2, a3, k3, p3, c) -> float:
        """Function to which program adjust parameters"""
        return (
            a1 * np.sin(k1 * x + p1)
            + a2 * np.sin(k2 * x + p2)
            + a3 * np.sin(k3 * x + p3)
            + c
        )

    @property
    def params(self):
        if self._params is None:
            self.adjusting_strategy.perform_algorithm()
            (
                self._params,
                self.distance,
            ) = self.adjusting_strategy.get_params_and_distance()

        return self._params


def get_random_points() -> List[Point]:
    return [Point(x=uniform(-4, 4), y=uniform(-2, 2)) for _ in range(5)]
