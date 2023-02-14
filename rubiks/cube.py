__all__ = (
    "NxCube",
)

import numpy as np

from .constants import *
from .move import NxCubeMove


class NxCube:
    """
    NxNxN standard Rubik's Cube.

    Standard orientation:
    Yellow on top, blue facing you.
    """

    n: int
    stack: list[NxCubeMove]
    # State is np array shape (6, n, n)
    # See docs for the order of stuff.
    state: np.ndarray
    maps: list[list[NxCubeMove]]

    def __init__(self, n: int) -> None:
        """
        Initialize as solved.
        """
        self.n = n
        self.stack = []
        self.maps = []

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

        # Green (need to rotate 180deg)
        green = [line.strip().split(" ") for line in self.face_to_str(3).strip().split("\n")[:-1]]
        green = [line[::-1] for line in green[::-1]]
        for line in green:
            s += " " * (2*self.n) + " ".join(line) + "\n"

        s += "\n"
        s += Color.ANSI_RESET
        s += "Move stack: "
        s += " ".join([str(move) for move in self.stack])
        s += "\n"

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

    def move(self, move: NxCubeMove | str) -> None:
        """
        Executes the move.
        Note: If slices extends all the way thru cube, the opposite face is also rotated.
        i.e. U0:3 on 3x3 rotates whole cube.
        """
        if isinstance(move, str):
            move = NxCubeMove.from_str(move)

        slices = move.slices
        if slices is None:
            slices = (0, 1)

        assert slices[1] <= self.n
        for s in range(slices[0], slices[1]):
            self._slice(move.face, s, move.dir)
        if slices[0] == 0:
            self._turn(move.face, move.dir)
        if slices[1] == self.n:
            self._turn(Color.opposite(move.face), not move.dir)

        self.stack.append(move)

    def moves(self, moves: list[NxCubeMove | str]) -> None:
        """
        Executes a list of moves.
        """
        for move in moves:
            self.move(move)

    def push_map(self, top: int, front: int) -> list[NxCubeMove]:
        """
        Perform a series of moves to rotate whole cube to desired orientation.
        Mapping is relative to std pos: No matter current map, assume top is Yellow and front is Blue.
        After map, turning "Yellow" (top) face will turn whatever top face is.
        Uses pop_map() to remove.

        :return: Moves performed.
        """
        find_lateral = lambda cube, x: [i for i in range(1, 5) if cube[i][0][0] == x][0]

        orient = NxCube(self.n)

        if orient.state[5][0][0] == top:
            for _ in range(2):
                orient.move(NxCubeMove("F", True, (0, self.n)))
        elif orient.state[0][0][0] != top:
            face = top % 4 + 1
            orient.move(NxCubeMove(face, True, (0, self.n)))

        lat = find_lateral(orient.state, front) - 1
        for _ in range(lat):
            orient.move(NxCubeMove("U", True, (0, self.n)))

        moves = orient.stack
        self.moves(moves)
        self.maps.append(moves)
        return moves

    def pop_map(self) -> list[NxCubeMove]:
        moves = self.maps.pop()
        moves = list(reversed([m.invert() for m in moves]))
        self.moves(moves)
        return moves

    def scramble(self, length: int | None = None) -> None:
        """
        :param length: Amount of moves. If None, is n^2 * 3
        """
        if length is None:
            length = self.n ** 2 * 3
        for _ in range(length):
            self.move(NxCubeMove.random(self.n))

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

    def _slice(self, face_ind: int, depth: int, dir: bool) -> None:
        """
        Do a slice.
        Note: If depth is 0, it acts on the face.
        But it only changes the lateral sides; the face itself is not rotated.
        """
        # First find the np slices for the 4 lateral sides.
        # Unfortunately, it is just manual casework.
        if face_ind == 0:
            # Yellow face
            slices = (
                np.s_[1, depth, :],   # Blue
                np.s_[2, depth, :],   # Red
                np.s_[3, depth, :],   # Green
                np.s_[4, depth, :],   # Orange
            )
        elif face_ind == 1:
            # Blue face
            slices = (
                np.s_[5, depth, :],        # White
                np.s_[2, ::-1, depth],     # Red
                np.s_[0, -depth-1, ::-1],  # Yellow
                np.s_[4, :, -depth-1],     # Orange
            )
        elif face_ind == 2:
            # Red face
            slices = (
                np.s_[5, :, -depth-1],   # White
                np.s_[3, ::-1, depth],   # Green
                np.s_[0, :, -depth-1],   # Yellow
                np.s_[1, :, -depth-1],   # Blue
            )
        elif face_ind == 3:
            # Green face
            slices = (
                np.s_[5, -depth-1, ::-1],  # White
                np.s_[4, ::-1, depth],     # Orange
                np.s_[0, depth, :],        # Yellow
                np.s_[2, :, -depth-1],     # Red
            )
        elif face_ind == 4:
            # Orange face
            slices = (
                np.s_[5, ::-1, depth],   # White
                np.s_[1, ::-1, depth],   # Blue
                np.s_[0, ::-1, depth],   # Yellow
                np.s_[3, :, -depth-1],   # Green
            )
        elif face_ind == 5:
            # White face
            slices = (
                np.s_[3, -depth-1, ::-1],  # Green
                np.s_[2, -depth-1, ::-1],  # Red
                np.s_[1, -depth-1, ::-1],  # Blue
                np.s_[4, -depth-1, ::-1],  # Orange
            )
        else:
            raise ValueError("Invalid face index.")

        # Now rotate the lateral sides.
        segments = [self.state[s].copy() for s in slices]
        if dir:
            self.state[slices[0]] = segments[1]
            self.state[slices[1]] = segments[2]
            self.state[slices[2]] = segments[3]
            self.state[slices[3]] = segments[0]
        else:
            self.state[slices[0]] = segments[3]
            self.state[slices[1]] = segments[0]
            self.state[slices[2]] = segments[1]
            self.state[slices[3]] = segments[2]
