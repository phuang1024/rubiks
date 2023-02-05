"""
Rubik's cube representation and solver.
"""

from .constants import *
from .cube import *
from .move import *


def _main(face):
    move = NxCubeMove.from_str("U2:3'")
    print(move)
    print(move.face, move.dir, move.slices)
    print(move.invert())
