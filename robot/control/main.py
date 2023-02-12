import time

import cv2

from arduino import Arduino
from detect import detect_cube


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

    arduino.on()
    while True:
        delta = int(input())
        if delta == 0:
            break
        arduino._motor_step(0, delta>0, delta, 0.03)
    arduino.set_flipper(True)

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
