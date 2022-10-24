import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from .sinusParams import SinusParamsAdjuster
from .typing import SinParameters
import numpy as np


class SinAdjusterView(ABC):
    @abstractmethod
    def __init__(self, sinus_params_adjuster: SinusParamsAdjuster):
        pass

    @abstractmethod
    def display_points(self) -> None:
        pass

    @abstractmethod
    def display_points_and_graph(self, params: SinParameters) -> None:
        pass


class PlotView(SinAdjusterView):
    def __init__(self, sinus_params_adjuster: SinusParamsAdjuster):
        # TODO: Something is wrong with this pattern
        self.adjuster = sinus_params_adjuster

    def _draw_points(self) -> None:
        plt.scatter(
            [p.x for p in self.adjuster.points],
            [p.y for p in self.adjuster.points],
            s=10,
        )
        plt.figure(num=1, figsize=(5, 5))

    def _draw_graph(self) -> None:
        x = np.linspace(-4, 4, 1000)
        y = self.adjuster.sin_with_params(x, *(self.adjuster.params))
        plt.plot(x, y, linewidth=1)

    def display_points_and_graph(self) -> None:
        self._draw_points()
        self._draw_graph()
        plt.show()

    def display_points(self) -> None:
        self._draw_points()
        plt.show()

    def print_params(self) -> None:
        print(f"Params: {self.adjuster.params}")
        print(f"Distance: {self.adjuster.distance}")
