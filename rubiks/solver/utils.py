"""
Utilities.

Find utils: Find position of pieces with specified colors.
Colors can be tuple of cols (BLUE, RED), etc.
Or string of colors "BR", etc.
"""

__all__ = (
    "corner_locs",
    "edge_locs",
    "center_locs",
    "xyz_to_slices",
    "xyz_to_colors",
    "find_corner",
    "find_edges",
    "find_centers",
)

import numpy as np

from ..cube import NxCube
from ..constants import *
from ..move import NxCubeMove


def _cvt_colors(colors: str | set[int]) -> set[int]:
    """
    Converts each char to color if string.
    """
    if isinstance(colors, str):
        return {Color.char_to_col(c) for c in colors}
    return colors


def corner_locs(n: int):
    for x in range(0, 2):
        for y in range(0, 2):
            for z in range(0, 2):
                yield (x*(n-1), y*(n-1), z*(n-1))

def edge_locs(n: int):
    for x in range(1, n-1):
        for y in range(0, 2):
            for z in range(0, 2):
                yield (x, y*(n-1), z*(n-1))
    for x in range(0, 2):
        for y in range(1, n-1):
            for z in range(0, 2):
                yield (x*(n-1), y, z*(n-1))
    for x in range(0, 2):
        for y in range(0, 2):
            for z in range(1, n-1):
                yield (x*(n-1), y*(n-1), z)

def center_locs(n: int):
    for x in range(0, 2):
        for y in range(1, n-1):
            for z in range(1, n-1):
                yield (x*(n-1), y, z)
    for x in range(1, n-1):
        for y in range(0, 2):
            for z in range(1, n-1):
                yield (x, y*(n-1), z)
    for x in range(1, n-1):
        for y in range(1, n-1):
            for z in range(0, 2):
                yield (x, y, z*(n-1))


def xyz_to_slices(loc: tuple[int, int, int], n: int) -> set:
    """
    Converts XYZ location to set of slices to perform on cube.state
    XYZ location must be on surface of cube.
    May return 1, 2, or 3 (depending on loc type)
    """
    slices = []
    if loc[0] == 0:
        slices.append(np.s_[4, -loc[2]-1, -loc[1]-1])
    elif loc[0] == n-1:
        slices.append(np.s_[2, -loc[2]-1, loc[1]])
    if loc[1] == 0:
        slices.append(np.s_[1, -loc[2]-1, loc[0]])
    elif loc[1] == n-1:
        slices.append(np.s_[3, -loc[2]-1, -loc[0]-1])
    if loc[2] == 0:
        slices.append(np.s_[5, loc[1], loc[0]])
    elif loc[2] == n-1:
        slices.append(np.s_[0, -loc[1]-1, loc[0]])
    return set(slices)

def xyz_to_colors(cube: NxCube, loc: tuple[int, int, int]) -> set[int]:
    """
    Returns colors of piece at that coord.
    """
    return {cube.state[s] for s in xyz_to_slices(loc, cube.n)}


def find_corner(cube: NxCube, colors: str | set[int]) -> tuple[int, int, int]:
    colors = _cvt_colors(colors)
    for loc in corner_locs(cube.n):
        if xyz_to_colors(cube, loc) == colors:
            return loc
    raise ValueError("Corner not found")

def find_edges(cube: NxCube, colors: str | set[int]):
    colors = _cvt_colors(colors)
    for loc in edge_locs(cube.n):
        if xyz_to_colors(cube, loc) == colors:
            yield loc

def find_centers(cube: NxCube, color: str | int):
    if isinstance(color, str):
        color = Color.char_to_col(color)
    for loc in center_locs(cube.n):
        if list(xyz_to_colors(cube, loc))[0] == color:
            yield loc
