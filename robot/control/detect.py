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
        if False:
            cv2.imshow("original", img)
            cv2.waitKey(1)

        img = img.copy().astype(float)

        # Increase image contrast
        thres = 90
        fac = 0.5
        lumin = img.mean(axis=2)
        dark = lumin < thres
        light = lumin >= thres
        img[dark] *= fac
        img[light] = 255 - (255 - img[light]) * fac
        img = img.astype(np.uint8)
        img = cv2.GaussianBlur(img, (3, 3), 0)

        if False:
            cv2.imshow("contrast", img)
            cv2.waitKey(1)

        corners, ids, reject = _fiducials.detector.detectMarkers(img)
        corners = [c.astype(int) for c in corners]
        corners = np.array(corners)
        return (corners, ids)


def detect_cube(cap):
    """
    Uses 4 pre-determined fiducials to detect the cube.
    Returns cropped image of the cube.

    :param discard: Amount of images to read to clear cache.
    """
    ret, img = cap.read()
    corners, ids = _fiducials.detect(img)

    if corners.shape[0] == 4:
        # Corners of each fiducial.
        crop_corners = np.empty((4, 2), dtype=np.float32)
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
            crop_corners[idx] = fid[0][idx]
        tmp = np.empty_like(crop_corners)
        tmp[0] = crop_corners[2]
        tmp[1] = crop_corners[1]
        tmp[2] = crop_corners[0]
        tmp[3] = crop_corners[3]
        crop_corners = tmp

        # Perspective transform.
        width = 300
        height = 300
        dest_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)
        trans = cv2.getPerspectiveTransform(crop_corners, dest_points)
        crop = cv2.warpPerspective(img, trans, (width, height))

        crop = crop[62:205, 91:205]
        crop = cv2.resize(crop, (128, 128), interpolation=cv2.INTER_AREA)
        return crop

    return None


def grid_image(img):
    """
    Converts rubik's image to grid of each cubie's color.
    """
    def px_bounds(i):
        cvt = lambda x: int(128 / 7 * x)
        lower = cvt(i) + 4
        upper = cvt(i+1) - 4
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
