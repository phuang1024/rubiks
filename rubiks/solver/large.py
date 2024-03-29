__all__ = (
    "move_all_centers",
    "solve_centers",
)

from ..constants import Color
from ..cube import NxCube
from ..move import NxCubeMove


def move_all_centers(cube: NxCube, from_face: int, to_face: int, cubie: int):
    """
    Move center cubies from one to another face.

    :param cubie: Cubie color to move.
    """
    cube.push_map(from_face, to_face)
    center_size = cube.n - 2

    while True:
        # Check if done
        done = True
        todo = None
        for y in range(1, center_size + 1):
            for x in range(1, center_size + 1):
                if cube.state[0, y, x] == cubie:
                    done = False
                    todo = (x, y)
                    break
            if not done:
                break
        if done:
            break
        assert todo is not None

        # Spin faces to good position
        subtract = cube.n - 1
        positions = (
            (todo[0], todo[1]),
            (subtract - todo[1], todo[0]),
            (subtract - todo[0], subtract - todo[1]),
            (todo[1], subtract - todo[0]),
        )
        # X is more important than Y.
        topleft = min(positions, key=lambda p: 1000*p[0] + p[1])
        topleft_ind = positions.index(topleft)

        from_steps = (positions.index(todo) - topleft_ind) % 4
        for i, p in enumerate(positions):
            if cube.state[1, p[1], p[0]] != cubie:
                to_steps = (i - topleft_ind) % 4
                break
        else:
            raise ValueError("No position to move to")
        for _ in range(from_steps):
            cube.move("U'")
        for _ in range(to_steps):
            cube.move("F'")

        # Perform the swap algorithm
        left_slice = (subtract-topleft[0], subtract-topleft[0]+1)
        right_slice = (topleft[1], topleft[1]+1)
        cube.move(NxCubeMove("R", False, left_slice))
        cube.move("F")
        cube.move(NxCubeMove("R", False, right_slice))
        cube.move("F'")
        cube.move(NxCubeMove("R", True, left_slice))
        cube.move("F")
        cube.move(NxCubeMove("R", True, right_slice))

    cube.pop_map()

def solve_centers(cube: NxCube):
    """
    Clears cube stack at beginning.
    """
    # Verify count of centers is correct.
    expect = (cube.n-2) ** 2
    count = [0] * 6
    for i in range(6):
        count[i] = (cube.state[:, 1:-1, 1:-1] == i).sum()
    assert count == [expect] * 6

    cube.stack = []

    for to_face in range(6):
        # First move opposite side to intermediate face.
        opp = Color.opposite(to_face)
        if to_face <= 2:
            inter = to_face + 1
        else:
            inter = None
        if inter is not None:
            move_all_centers(cube, opp, inter, to_face)

        # Now move all from lateral.
        from_faces = list(range(6))
        from_faces.remove(to_face)
        from_faces.remove(opp)
        for fro in from_faces:
            move_all_centers(cube, fro, to_face, to_face)

    return cube.stack
