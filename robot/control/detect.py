import cv2
import numpy as np


class _fiducials:
    """
    More like a namespace.
    """
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, params)

    @staticmethod
    def detect(img):
        """
        Detects the fiducials in the image.
        """
        corners, ids, reject = _fiducials.detector.detectMarkers(img)
        corners = [c.astype(int) for c in corners]
        return (corners, ids)


def detect_cube(img):
    """
    Uses 4 pre-determined fiducials to detect the cube.
    """
    corners, ids = _fiducials.detect(img)
    for c in corners:
        cv2.polylines(img, c, True, (0, 255, 0), 2)
