import argparse
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
            color = [int(c) for c in color]
            if input(f"Detected RGB {color}; OK? [Y/n]").strip().lower() != "n":
                break

    return color


def scan_face(color, cap, rgb_colors):
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

            if input(f"Scanned face; OK? [Y/n]").strip().lower() != "n":
                print()
                break

    # White is reversed.
    if color == 5:
        face = face[::-1, ::-1]

    return face


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=int, default=0)
    args = parser.parse_args()

    arduino = Arduino("/dev/ttyACM0")
    cap = cv2.VideoCapture(args.video)

    # Adjust camera exposure
    params = (
        "exposure_auto=1",
        "exposure_absolute=40",
        "white_balance_temperature_auto=0",
    )
    for param in params:
        run(["v4l2-ctl", "-d", f"/dev/video{args.video}", "-c", param])

    print("In all cases, place cube Yellow up and Blue front.")

    # Get config
    if os.path.isfile("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
    else:
        print("Config file not found.")
        print("Place solved cube inside the robot to calibrate color of each face.")
        colors = foreach_face(arduino, avg_face_color, (cap,))
        config = {"colors": colors}
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

    input("Press enter to begin scanning cube.")
    scan = foreach_face(arduino, scan_face, (cap, config["colors"]))

    # Testing 3x3 solve
    cube = NxCube(3)
    for i in range(6):
        for y in range(3):
            for x in range(3):
                from_x = (x if x != 2 else 6)
                from_y = (y if y != 2 else 6)
                cube.state[i, y, x] = scan[i][from_y, from_x]

    moves = solver.solve_3x3(cube)
    print("Solved 3x3 in", len(moves), "moves")

    if input("Enter (1) to automatically move to standard position; nothing to skip: ").strip() == "1":
        arduino.set_height(7)
        arduino.turn(1)
        arduino.set_height(0)
        arduino.set_flipper(False)
        arduino.set_height(7)
        arduino.turn(-1)
        arduino.set_height(0)
        arduino.set_flipper(True)
        arduino.set_height(7)
        arduino.turn(1)
        arduino.set_height(0)

    input("Make sure cube is in standard position. Press enter to solve.")

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
