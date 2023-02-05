__all__ = (
    "NxCube",
)

import numpy as np

from .constants import *


class NxCube:
    """
    NxNxN standard Rubik's Cube.

    Standard orientation:
    Yellow on top, blue facing you.
    """

    n: int
    # State is np array shape (6, n, n)
    # See docs for the order of stuff.
    state: np.ndarray

    def __init__(self, n: int) -> None:
        """
        Initialize as solved.
        """
        self.n = n
        self.state = np.zeros((6, n, n), dtype=np.int8)
        self.state[0] = Color.YELLOW
        self.state[1] = Color.BLUE
        self.state[2] = Color.RED
        self.state[3] = Color.GREEN
        self.state[4] = Color.ORANGE
        self.state[5] = Color.WHITE

    def __repr__(self) -> str:
        """
        Draws net of cube.
          #       Y
        # # #   O B R
          #       W
          #       G
        """
        s = ""

        # Yellow
        s += self.face_to_str(0, offset=2*self.n)

        # Orange, blue, red
        orange = self.face_to_str(4).split("\n")
        blue = self.face_to_str(1).split("\n")
        red = self.face_to_str(2).split("\n")
        for line in range(self.n):
            s += orange[line] + blue[line] + red[line] + "\n"

        # White
        s += self.face_to_str(5, offset=2*self.n)

        # Green
        s += self.face_to_str(3, offset=2*self.n)

        return s

    def face_to_str(self, face: int, ansi: bool = True, spacing: int = 1, offset: int = 0) -> str:
        """
        Returns a string representation of the given face.

        :param ansi: Whether to color output in terminal. If false, uses uppercase letters.
        :param spacing: Spaces between each piece.
        :param offset: Offset from the left side of the terminal.
        """
        s = ""
        for y in range(self.n):
            s += " " * offset
            for x in range(self.n):
                col = self.state[face, y, x]
                if ansi:
                    s += Color.col_to_ansi(col) + "#"
                else:
                    s += Color.col_to_char(col)
                s += " " * spacing
            s += "\n"

        if ansi:
            s += Color.ANSI_RESET

        return s

    def _turn(self, face_ind: int, dir: bool) -> None:
        """
        ONLY turns the face. Doesn't change the lateral slices affected.

        :param dir: cw if True else ccw
        """
        # Go ring by ring.
        rings = (self.n + 1) // 2
        face = self.state[face_ind]
        for ring in range(rings):
            ring_size = self.n - 2 * ring
            if ring_size == 1:
                continue
            padding = (self.n - ring_size) // 2

            # Inclusive coords.
            bounds = (padding, self.n - padding - 1)

            # Get slices for each of 4 segments.
            top = np.s_[bounds[0], bounds[0] : bounds[1]]
            right = np.s_[bounds[0] : bounds[1], bounds[1]]
            bottom = np.s_[bounds[1], bounds[1] : bounds[0] : -1]
            left = np.s_[bounds[1] : bounds[0] : -1, bounds[0]]

            top_seg = face[top].copy()
            right_seg = face[right].copy()
            bottom_seg = face[bottom].copy()
            left_seg = face[left].copy()

            # Switch them.
            if dir:
                """
                face[top], face[right], face[bottom], face[left] = (
                    face[left], face[top], face[right], face[bottom])
                """
                face[top] = left_seg
                face[left] = bottom_seg
                face[bottom] = right_seg
                face[right] = top_seg
            else:
                """
                face[top], face[right], face[bottom], face[left] = (
                    face[right], face[bottom], face[left], face[top])
                """
                face[top] = right_seg
                face[left] = top_seg
                face[bottom] = left_seg
                face[right] = bottom_seg
