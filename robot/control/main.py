import sys
import time
from curses import wrapper
from pathlib import Path
ROOT = Path(__file__).absolute().parent.parent.parent
sys.path.append(str(ROOT))

import cv2
from rubiks import NxCube, NxCubeMove, solver

from arduino import Arduino
from detect import detect_cube

moves = ("B", "B", "F", "F", "D", "D", "F", "F", "L'", "U", "U", "L", "D", "D",
    "L", "L", "U", "U", "R'", "D", "D", "B'", "D", "L", "L", "F", "F", "R", "R",
    "U", "U", "R", "D", "R")
cube = NxCube(3)
for m in moves:
    cube.move(m)

def test_fiducial():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        detect_cube(img)
        cv2.imshow("img", img)
        cv2.waitKey(50)


def test_arduino():
    arduino = Arduino("/dev/ttyACM0")
    #arduino.test()
    arduino.off()

    arduino.on()
    while True:
        delta = int(input())
        if delta == 0:
            break
        arduino._motor_step(0, delta>0, delta, 0.03)


    moves = solver.solve_3x3(cube)
    for m in moves:
        arduino.make_move(m)
    arduino.set_height(0)
    arduino.set_flipper(True)
    arduino.off()
    stop

    """
    arduino.set_flipper(False)
    arduino.turn(1)
    arduino.turn(-2)
    arduino.set_flipper(True)
    """

    def checker_step():
        for i in range(8):
            arduino.set_height(i)
            arduino.turn(2)

    checker_step()
    arduino.set_height(0)
    arduino.set_flipper(False)
    checker_step()
    arduino.set_height(7)
    arduino.turn(1)
    arduino.set_height(0)
    arduino.set_flipper(True)
    checker_step()
    arduino.set_height(0)

    arduino.off()


def main():
    test_arduino()


if __name__ == "__main__":
    main()
