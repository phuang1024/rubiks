"""
Rubik's cube representation and solver.
"""

from .constants import *
from .cube import *


def _main():
    cube = NxCube(4)
    print("Original:")
    print(cube)

    cube.state[1][1] = Color.RED
    print("Mutated:")
    print(cube)

    cube._turn(1, True)
    print("Turn CW:")
    print(cube)

    cube._turn(1, False)
    print("Turn CCW (should be original):")
    print(cube)

    cube._turn(1, False)
    print("Turn CCW again:")
    print(cube)
