import json
import os
import sys
import time
from colorsys import rgb_to_hsv
from pathlib import Path
from subprocess import run

ROOT = Path(__file__).absolute().parent.parent.parent
sys.path.append(str(ROOT))

import cv2
import numpy as np
from rubiks import Color, NxCube, NxCubeMove, solver

from arduino import Arduino
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


def do_config(arduino, cap):
    print("Config not found. Follow instructions:")
    print("Place the cube with Yellow on top and Blue in front.")
    print("Aim a webcam at it and wait for detection.")

    colors = [1, 2, 3, 4, 0, 5]
    rgb_colors = [None] * 6
    while True:
        print(f"Waiting for {Color.col_to_name(colors[0])}...")
        while True:
            ret, img = cap.read()
            img = detect_cube(cap)
            if img is not None:
                color = avg_color(img)[::-1]
                color = [int(c) for c in color]
                if input(f"Detected RGB {color}; OK? [Y/n]").strip().lower() != "n":
                    break

        rgb_colors[colors.pop(0)] = color

        # Move robot to next color.
        if len(colors) == 0:
            break
        next_face(arduino, colors[0])

        for _ in range(10):
            cap.read()

    config = {"colors": rgb_colors}
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    return config


def scan_cube(arduino, cap, rgb_colors):
    print("Scanning cube. Place Yellow center on top and Blue in front.")

    hsv_colors = [
        np.array(rgb_to_hsv(*(np.array(rgb_colors[i]) / 255)))
        for i in range(6)
    ]

    colors = [1, 2, 3, 4, 0, 5]
    faces = [None] * 6
    while True:
        print(f"Scanning face {Color.col_to_name(colors[0])}...")
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
                        hsv_cubie = np.array(rgb_to_hsv(*(grid[x, y]) / 255))
                        for i in range(6):
                            diff = hsv_cubie - hsv_colors[i]
                            distance[i] = np.linalg.norm(grid[x, y] - rgb_colors[i])
                        face[x, y] = np.argmin(distance)

                # Print face.
                for y in range(7):
                    for x in range(7):
                        print(Color.col_to_ansi(face[y, x]), end="")
                        print("# ", end="")
                    print()
                print("\033[0m")

                if input(f"Scanned face; OK? [Y/n]").strip().lower() != "n":
                    print()
                    break

        # White is reversed.
        if len(colors) == 1:
            face = face[::-1, ::-1]
        faces[colors[0]] = face

        # Move robot to next color.
        colors.pop(0)
        if len(colors) == 0:
            break
        next_face(arduino, colors[0])

        for _ in range(10):
            cap.read()

    return faces


def main():
    arduino = Arduino("/dev/ttyACM0")
    cap = cv2.VideoCapture(0)

    # Adjust camera exposure
    params = (
        "exposure_auto=1",
        "exposure_absolute=300",
        "white_balance_temperature_auto=0",
    )
    for param in params:
        run(["v4l2-ctl", "-d", "/dev/video0", "-c", param])

    # Get config
    if os.path.isfile("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
    else:
        config = do_config(arduino, cap)

    scan = scan_cube(arduino, cap, config["colors"])
    #print("Because of ****, enter faces manually.")
    #scan = manual_scan(arduino, cap, config["colors"])

    # Testing 3x3 solve
    cube = NxCube(3)
    for i in range(6):
        for y in range(3):
            for x in range(3):
                from_x = (x if x != 2 else 6)
                from_y = (y if y != 2 else 6)
                cube.state[i, y, x] = scan[i][from_y, from_x]

    print(cube)

    moves = solver.solve_3x3(cube)
    print(len(moves), "moves")
    input("Place cube in and press enter to solve.")
    for m in moves:
        arduino.make_move(m)
    arduino.set_height(0)
    arduino.set_flipper(True)

    print("Turning off motors...")
    time.sleep(1)
    arduino.set_height(0)
    arduino.off()
    cap.release()


if __name__ == "__main__":
    main()
