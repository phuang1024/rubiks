__all__ = (
    "NxCube",
)

import numpy as np

from constants import *


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
        s += self.face_to_str(0, offset=6)

        # Orange, blue, red
        orange = self.face_to_str(4).split("\n")
        blue = self.face_to_str(1).split("\n")
        red = self.face_to_str(2).split("\n")
        for line in range(3):
            s += orange[line] + blue[line] + red[line] + "\n"

        # White
        s += self.face_to_str(5, offset=6)

        # Green
        s += self.face_to_str(3, offset=6)

        return s

    def face_to_str(self, face: int, ansi: bool = True, spacing: int = 1, offset: int = 0) -> str:
        """
        Returns a string representation of the given face.

        :param ansi: Whether to color output in terminal. If false, uses uppercase letters.
        :param spacing: Spaces between each piece.
        :param offset: Offset from the left side of the terminal.
        """
        s = ""
        for y in range(3):
            s += " " * offset
            for x in range(3):
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


"""
      # # #
      # # #
      # # #
# # # # # # # # #
# # # # # # # # #
# # # # # # # # #
      # # #
      # # #
      # # #
      # # #
      # # #
      # # #
"""
