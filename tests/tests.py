import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np

from rubiks import *


class TestNxCube:
    def test_init(self):
        for n in range(2, 5):
            cube = NxCube(n)
            assert cube.n == n
            assert cube.state.shape == (6, n, n)
            assert np.all(cube.state[0] == Color.YELLOW)
            assert np.all(cube.state[1] == Color.BLUE)
            assert np.all(cube.state[2] == Color.RED)
            assert np.all(cube.state[3] == Color.GREEN)
            assert np.all(cube.state[4] == Color.ORANGE)
            assert np.all(cube.state[5] == Color.WHITE)

    def test_turn(self):
        for n in range(2, 5):
            # Set first bar to different color
            cube = NxCube(n)
            cube.state[0] = Color.YELLOW
            cube.state[0, 0, :] = Color.WHITE

            expect = np.full_like(cube.state[0], Color.YELLOW)
            expect[0] = Color.WHITE
            assert np.all(cube.state[0] == expect)

            cube._turn(0, True)
            expect[...] = Color.YELLOW
            expect[:, -1] = Color.WHITE
            assert np.all(cube.state[0] == expect)

            cube._turn(0, False)
            expect[...] = Color.YELLOW
            expect[0] = Color.WHITE
            assert np.all(cube.state[0] == expect)

            cube._turn(0, False)
            expect[...] = Color.YELLOW
            expect[:, 0] = Color.WHITE
            assert np.all(cube.state[0] == expect)

            if n >= 3:
                # Now set the second bar to diff color.
                cube.state[0] = Color.YELLOW
                cube.state[0, 1, :] = Color.WHITE

                expect = np.full_like(cube.state[0], Color.YELLOW)
                expect[1] = Color.WHITE
                assert np.all(cube.state[0] == expect)

                cube._turn(0, True)
                expect[...] = Color.YELLOW
                expect[:, -2] = Color.WHITE
                assert np.all(cube.state[0] == expect)

                cube._turn(0, False)
                expect[...] = Color.YELLOW
                expect[1] = Color.WHITE
                assert np.all(cube.state[0] == expect)

                cube._turn(0, False)
                expect[...] = Color.YELLOW
                expect[:, 1] = Color.WHITE
                assert np.all(cube.state[0] == expect)
