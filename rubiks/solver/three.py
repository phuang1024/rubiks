__all__ = (
    "solve_3x3",
)

from ..cube import NxCube
from ..constants import *
from ..move import NxCubeMove
from .utils import *


def solve_cross(cube: NxCube):
    def find_white_edges(cube):
        blue = next(find_edges(cube, "BW"))
        red = next(find_edges(cube, "RW"))
        green = next(find_edges(cube, "GW"))
        orange = next(find_edges(cube, "OW"))
        edges = (blue, red, green, orange)
        return edges

    def pos_to_lateral(pos):
        pos = pos[:2]
        if pos == (1, 0):
            return 0
        if pos == (2, 1):
            return 1
        if pos == (1, 2):
            return 2
        if pos == (0, 1):
            return 3
        raise ValueError(f"Invalid pos {pos}")

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
        edges = find_white_edges(cube)
        if all(e[2] == 2 for e in edges):
            break

        # Find spots where edges can go.
        available = [True] * 4
        for edge in edges:
            if edge[2] == 2:
                available[pos_to_lateral(edge)] = False

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

    print(cube)
    input()

    # Now move them to the white center.
    while True:
        edges = find_white_edges(cube)
        for i, e in enumerate(edges):
            if e[2] == 2:
                target = e
                index = i
                break
        else:
            break

        slices = list(xyz_to_slices(target, cube.n))
        is_flipped = [s for s in slices if cube.state[s] == Color.WHITE][0][0] != Color.YELLOW

        if is_flipped:
            target_lateral = (index - 1) % 4
        else:
            target_lateral = index
        curr_lateral = pos_to_lateral(target)
        for _ in range((curr_lateral-target_lateral) % 4):
            cube.move(NxCubeMove(Color.YELLOW, True))
        if is_flipped:
            cube.move(NxCubeMove(target_lateral+1, True))
            cube.move(NxCubeMove(Color.YELLOW, False))
            next_face = (target_lateral + 1) % 4
            cube.move(NxCubeMove(next_face+1, False))
        else:
            for _ in range(2):
                cube.move(NxCubeMove(target_lateral+1, True))

        print(target)
        print(cube)
        input()


def solve_white(cube: NxCube):
    def get_white_corners(cube):
        info = (
            ("WBO", (0, 0, 0)),
            ("WBR", (2, 0, 0)),
            ("WGO", (0, 2, 0)),
            ("WGR", (2, 2, 0)),
        )
        ret = []
        for code, pos in info:
            real_pos = find_corner(cube, code)
            correct = False
            if real_pos == pos:
                # Check if correct
                slices = list(xyz_to_slices(real_pos, cube.n))
                bottom = [s for s in slices if s[0] == Color.WHITE][0]
                correct = cube.state[bottom] == Color.WHITE
            ret.append((real_pos, pos, correct))

        return ret

    def pos_to_lateral(pos):
        """
        Returns the two lateral faces containing the corner pos.
        """
        pos = pos[:2]
        if pos == (0, 0):
            return (0, 3)
        if pos == (2, 0):
            return (0, 1)
        if pos == (0, 2):
            return (2, 3)
        if pos == (2, 2):
            return (2, 1)
        raise ValueError(f"Invalid pos {pos}")

    while True:
        corners = get_white_corners(cube)
        for real, nom, correct in corners:
            if real != nom or not correct:
                break
        else:
            break

        if real[2] == 0:
            # Move it out of the incorrect pos.
            lat1, lat2 = pos_to_lateral(real)
            cube.move(NxCubeMove(lat1+1, True))
            cube.move(NxCubeMove(Color.YELLOW, False))
            cube.move(NxCubeMove(lat1+1, False))
            continue

        # Move it above the correct pos.
        if real[:2] != nom[:2]:
            corner_indices = ((0, 0), (2, 0), (2, 2), (0, 2))
            real_idx = corner_indices.index(real[:2])
            nom_idx = corner_indices.index(nom[:2])
            delta = (real_idx - nom_idx) % 4
            for _ in range(delta):
                cube.move(NxCubeMove(Color.YELLOW, True))

        # Insert it.
        lat1, lat2 = pos_to_lateral(nom)


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
