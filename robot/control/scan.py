import numpy as np

from rubiks import *

from detect import detect_cube, avg_color, grid_image


def next_face(arduino, i):
    """
    For scanning.
    """
    if i in (2, 3, 4):
        arduino.set_height(7)
        arduino.turn(1)
        arduino.set_height(0)
    elif i == 0:
        arduino.set_height(0)
        arduino.set_flipper(False)
        arduino.set_height(7)
        arduino.turn(1)
        arduino.set_height(0)
        arduino.set_flipper(True)
        arduino.set_height(7)
        arduino.turn(1)
        arduino.set_height(0)
    elif i == 5:
        arduino.set_height(7)
        arduino.turn(2)
        arduino.set_height(0)


def foreach_face(arduino, callback, args=(), kwargs={}):
    """
    For each face of the cube, call the function and return aggregate results.
    Calls in the order (blue, red, green, orange, yellow, white).
    But results are order (yellow, blue, red, green, orange, white).

    Callback takes args (color, *args, **kwargs)
    """
    colors = [1, 2, 3, 4, 0, 5]
    ret = [None] * 6
    while True:
        ret[colors[0]] = callback(colors[0], *args, **kwargs)

        # Move robot to next color.
        colors.pop(0)
        if len(colors) == 0:
            break
        next_face(arduino, colors[0])

    return ret


def avg_face_color(color, cap):
    for _ in range(10):
        cap.read()

    print(f"Waiting for {Color.col_to_name(color)}...")
    while True:
        ret, img = cap.read()
        img = detect_cube(cap)
        if img is not None:
            color = avg_color(img)[::-1]
            grid = grid_image(img)[..., ::-1]
            color = grid[3][3]

            color = [int(c) for c in color]
            if input(f"Detected RGB {color}; OK? [Y/n]").strip().lower() != "n":
                break

    return color


def scan_face(color, cap, rgb_colors, auto: bool):
    for _ in range(10):
        cap.read()

    print(f"Scanning face {Color.col_to_name(color)}...")
    while True:
        ret, img = cap.read()
        img = detect_cube(cap)
        if img is not None:
            grid = grid_image(img)[..., ::-1]
            face = np.zeros((7, 7), dtype=int)

            # Find face colors.
            for y in range(7):
                for x in range(7):
                    distance = [0] * 6
                    for i in range(6):
                        distance[i] = np.linalg.norm(grid[x, y] - rgb_colors[i])
                    face[x, y] = np.argmin(distance)

            # Print face.
            for y in range(7):
                for x in range(7):
                    print(Color.col_to_ansi(face[y, x]), end="")
                    print("# ", end="")
                print()
            print("\033[0m")

            if auto or input(f"Scanned face; OK? [Y/n]").strip().lower() != "n":
                print()
                break

    # White is reversed.
    if color == 5:
        face = face[::-1, ::-1]

    return face