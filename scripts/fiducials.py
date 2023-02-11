"""
Generate fiducials for printing.
"""

import cv2
import numpy as np

# Millimeters
PAPER_WIDTH = 216
FIDUCIAL_SIZE = 24
SPACING = 10

_m_to_px = lambda m: int(m / PAPER_WIDTH * RESOLUTION)
COUNT = 4
RESOLUTION = 1000
FIDUCIAL_PX = _m_to_px(FIDUCIAL_SIZE)
SPACING_PX = _m_to_px(SPACING)
del FIDUCIAL_SIZE
del SPACING


img = np.full((RESOLUTION, RESOLUTION), 255, np.uint8)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

x = SPACING_PX
y = SPACING_PX
for i in range(COUNT):
    marker = cv2.aruco.generateImageMarker(dictionary, i, 6)
    marker = cv2.resize(marker, (FIDUCIAL_PX, FIDUCIAL_PX), interpolation=cv2.INTER_NEAREST)
    img[y:y+FIDUCIAL_PX, x:x+FIDUCIAL_PX] = marker

    x += FIDUCIAL_PX + SPACING_PX
    if x + FIDUCIAL_PX + SPACING_PX >= RESOLUTION:
        x = SPACING_PX
        y += FIDUCIAL_PX + SPACING_PX

cv2.imwrite("fiducials.jpg", img)
