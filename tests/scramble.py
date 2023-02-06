moves = ("B", "B", "F", "F", "D", "D", "F", "F", "L'", "U", "U", "L", "D", "D",
    "L", "L", "U", "U", "R'", "D", "D", "B'", "D", "L", "L", "F", "F", "R", "R",
    "U", "U", "R", "D", "R")
moves = (
    "F", "L'"
)

import rubiks
from rubiks import NxCube

cube = NxCube(3)
for m in moves:
    cube.move(m)
