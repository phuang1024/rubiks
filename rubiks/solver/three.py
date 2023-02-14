__all__ = (
    "solve_3x3",
)

import os
import shutil
import time
from subprocess import Popen, DEVNULL, PIPE

from ..constants import Color
from ..cube import NxCube
from ..move import NxCubeMove


def solve_3x3(cube: NxCube, twophase: str | None = None) -> list[NxCubeMove]:
    """
    Solve 3x3 cube using rob-twophase solver.
    Note: This may take some time as twophase boots.

    :param twophase: Path to executable, or None to search in PATH.
    """
    assert cube.n == 3
    if twophase is None:
        twophase = shutil.which("twophase")
        assert twophase is not None, "twophase executable not found"

    cwd = os.path.dirname(twophase)
    proc = Popen([twophase], cwd=cwd, stdin=PIPE, stdout=PIPE, stderr=DEVNULL)
    while True:
        line = proc.stdout.readline().decode()
        if "Ready" in line:
            break

    proc.stdin.write(b"solve ")
    for face in (0, 2, 1, 5, 4, 3):
        for y in range(3):
            for x in range(3):
                code = Color.col_to_face(cube.state[face, y, x])
                proc.stdin.write(f"{code}".encode())
    proc.stdin.write(b"\n")
    proc.stdin.flush()

    # Read line containing time first.
    for _ in range(2):
        line = proc.stdout.readline().decode()

    moves = map(NxCubeMove.from_str, line.strip().split(" ")[:-1])
    moves = list(moves)

    proc.kill()

    return moves
