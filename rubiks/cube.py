import numpy as np


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
        # TODO self.state
