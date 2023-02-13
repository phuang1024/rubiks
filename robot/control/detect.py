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
        corners = np.array(corners)
        return (corners, ids)


def detect_cube(img):
    """
    Uses 4 pre-determined fiducials to detect the cube.
    Returns cropped image of the cube.
    """
    corners, ids = _fiducials.detect(img)

    if corners.shape[0] == 4:
        # Corners of each fiducial.
        real_corners = np.empty((4, 2), dtype=np.float32)
        centroid = np.mean(corners, axis=(0, 1, 2))
        for fid in corners:
            x_idx = fid[0][0][0] < centroid[0]
            y_idx = fid[0][0][1] < centroid[1]
            match (x_idx, y_idx):
                case (0, 0): idx = 0
                case (0, 1): idx = 1
                case (1, 1): idx = 2
                case (1, 0): idx = 3
                case _: raise ValueError("Invalid corner")
            real_corners[idx] = fid[0][idx]

        # Perspective transform.
        width = 300
        height = 300
        dest_points = np.array([[0, 0], [0, height], [width, height], [width, 0]], dtype=np.float32)
        trans = cv2.getPerspectiveTransform(real_corners, dest_points)
        crop = cv2.warpPerspective(img, trans, (width, height))

        crop = crop[88:244, 98:212]
        crop = cv2.resize(crop, (128, 128), interpolation=cv2.INTER_AREA)
        return crop

    return None


def grid_image(img):
    """
    Converts rubik's image to grid of each cubie's color.
    """
    def px_bounds(i):
        cvt = lambda x: int(128 / 7 * x)
        lower = cvt(i) + 2
        upper = cvt(i+1) - 2
        return (lower, upper)

    face = np.zeros((7, 7, 3), dtype=float)
    for y in range(7):
        for x in range(7):
            xmin, xmax = px_bounds(x)
            ymin, ymax = px_bounds(y)
            face[y, x] = avg_color(img[ymin:ymax, xmin:xmax])

    return face


def avg_color(img):
    """
    Returns the average color of the image.
    """
    return np.mean(img, axis=(0, 1))
