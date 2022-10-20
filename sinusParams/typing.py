import typing
from collections.abc import Iterable
import numpy.typing as npt

# SinParameters = Iterable[float]
SinParameters = typing.List[float]

# TODO: There must be a better way
SinWithParameters = typing.Callable[
    [
        float | npt.ArrayLike,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ],
    float,
]
