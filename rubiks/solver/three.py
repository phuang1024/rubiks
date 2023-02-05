__all__ = (
    "solve_3x3",
)

from ..cube import NxCube
from ..move import NxCubeMove


def solve_3x3(cube: NxCube) -> list[NxCubeMove]:
    """
    Uses the beginner's method.
    Very inefficient.
    """
