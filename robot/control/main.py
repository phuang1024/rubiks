import cv2

from detect import detect_cube


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        detect_cube(img)
        cv2.imshow("img", img)
        cv2.waitKey(50)


if __name__ == "__main__":
    main()
