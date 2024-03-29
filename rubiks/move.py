__all__ = (
    "NxCubeMove",
)

import random

from .constants import *


class NxCubeMove:
    """
    A move to do on a cube.

    Notation (different from standard):
    - U F R D B L: One layer clockwise.
    - U' ...: One layer counter-clockwise.
    - Ux:y ...: Starting from index 0, the slices x to y (excluding y) are rotated clockwise.
    - Ux:y' ...: Counter-clockwise of the above.
    """

    face: int
    dir: bool
    slices: tuple[int, int] | None

    def __init__(self, face: int | str, dir: bool, slices: tuple[int, int] | None = None) -> None:
        """
        :param face: Use Color.YELLOW, etc. with cube in standard orientation (see NxCube)
            Or "U", "F", etc.
        :param slices: Use None for just top layer (the face).
        """
        self.face = (face if isinstance(face, int) else Color.face_to_col(face))
        self.dir = dir
        self.slices = slices
        if self.slices is not None:
            assert self.slices[1] > self.slices[0]

    @classmethod
    def from_str(cls, s: str):
        """
        Does NOT validate string; make sure it's valid.

        :param s: "U", "U2", "Ux:y", "Ux:y'"
        """
        face = Color.face_to_col(s[0])
        dir = "'" not in s
        if ":" in s:
            pos = s.index(":")
            # TODO need to handle multi-digit numbers
            slice1 = int(s[pos-1:pos])
            slice2 = int(s[pos+1:pos+2])
            slices = (slice1, slice2)
        else:
            slices = None

        return cls(face, dir, slices)

    @classmethod
    def random(cls, n: int):
        """
        Random face, slice, dir.
        Does not go past n/2
        """
        face = random.randint(0, 5)
        limit = n // 2
        slice1 = random.randint(0, limit-1)
        slice2 = random.randint(slice1+1, limit)
        dir = random.randint(0, 1) == 0

        return cls(face, dir, (slice1, slice2))

    def __repr__(self):
        s = Color.col_to_face(self.face)
        if self.slices is not None:
            s += f"{self.slices[0]}:{self.slices[1]}"
        if not self.dir:
            s += "'"
        return s

    def invert(self):
        """
        Returns inverse of self (opposite dir)
        """
        return NxCubeMove(self.face, not self.dir, self.slices)
