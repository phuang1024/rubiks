"""
Rubik's cube representation and solver.
"""

from .constants import *
from .cube import *


def _main(face):
    #face = 0

    cube = NxCube(4)
    print("Original:")
    print(cube)

    """
    cube.state[1][1] = Color.RED
    print("Mutated:")
    print(cube)
    """

    cube._slice(face, 1, True)
    print("Slice CW:")
    print(cube)

    cube._slice(face, 1, False)
    print("Slice CCW (should be original):")
    print(cube)

    cube._slice(face, 1, False)
    print("Slice CCW again:")
    print(cube)
