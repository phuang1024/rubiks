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
    arduino.test()


def main():
    test_arduino()


if __name__ == "__main__":
    main()
