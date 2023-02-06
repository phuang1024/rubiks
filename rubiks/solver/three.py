__all__ = (
    "solve_3x3",
)

from ..cube import NxCube
from ..constants import *
from ..move import NxCubeMove
from .utils import *


def solve_cross(cube: NxCube):
    def next_lateral(x):
        """
        Lateral faces 1, 2, 3, 4.
        This function returns add one, looping back.
        """
        return (x % 4) + 1

    def cycle_available(cube: NxCube, available, target: int):
        """
        Makes U moves until target is available.
        Returns new available array.
        """
        for i in range(4):
            if available[target-i]:
                break
        for _ in range(i):
            cube.move(NxCubeMove(Color.YELLOW, False))

    # First move all edges to yellow center.
    while True:
        blue = next(find_edges(cube, "BW"))
        red = next(find_edges(cube, "RW"))
        orange = next(find_edges(cube, "OW"))
        green = next(find_edges(cube, "GW"))
        edges = (blue, red, orange, green)
        if all(e[2] == 2 for e in edges):
            break

        # Find spots where edges can go.
        available = [True] * 4
        for edge in edges:
            if edge[2] == 2:
                match (edge[0], edge[1]):
                    case (1, 0): available[0] = False
                    case (2, 1): available[1] = False
                    case (1, 2): available[2] = False
                    case (0, 1): available[3] = False

        # Find edge to move rn.
        target = max((e for e in edges if e[2] != 2), key=lambda e: e[2])
        slices = list(xyz_to_slices(target, cube.n))
        idx = 0 if cube.state[slices[0]] == Color.WHITE else 1
        white_face = slices[idx][0]
        other_face = slices[1-idx][0]
        if white_face != Color.WHITE and target[2] == 0:
            # Two move step to get to the top.
            cycle_available(cube, available, white_face - 1)
            cube.move(NxCubeMove(white_face, False))
            continue

        pos = [Color.BLUE, Color.RED, Color.GREEN, Color.ORANGE].index(other_face)
        available = cycle_available(cube, available, pos)
        if white_face == Color.BLUE and other_face == Color.ORANGE:
            dir = False
        elif white_face == Color.ORANGE and other_face == Color.BLUE:
            dir = True
        else:
            dir = white_face < other_face
        cube.move(NxCubeMove(other_face, dir))
        if target[2] == 0:
            cube.move(NxCubeMove(other_face, dir))


def solve_3x3(cube: NxCube) -> None:
    """
    Uses the beginner's method.
    Very inefficient.
    WILL modify cube in place.
    WILL clear cube's stack
    Returns nothing; use cube.stack to get moves.
    """
    assert cube.n == 3
    cube.stack = []

    solve_cross(cube)
