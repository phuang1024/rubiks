import argparse
import json
import os
import sys
import time
from pathlib import Path
from subprocess import run

ROOT = Path(__file__).absolute().parent.parent.parent
sys.path.append(str(ROOT))

import cv2
from rubiks import *
from tqdm import tqdm

from arduino import Arduino
from scan import *


def setup_camera(args):
    cap = cv2.VideoCapture(args.video)

    # Adjust camera exposure
    params = (
        "exposure_auto=1",
        "exposure_absolute=28",
        "white_balance_temperature_auto=0",
    )
    for param in params:
        run(["v4l2-ctl", "-d", f"/dev/video{args.video}", "-c", param])

    return cap


def to_standard_pos(args, arduino):
    """
    Prompts if user wants to move to standard position.
    """
    if args.auto or input("Enter \"1\" to automatically move to standard position; nothing to skip: ").strip() == "1":
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


def solve(args, config, arduino, cap):
    if args.auto:
        print("Auto mode: After pressing enter, robot will scan and solve cube.")
    input("Press enter to begin scanning cube.")
    scan = foreach_face(arduino, scan_face, (cap, config["colors"], args.auto))
    cap.release()

    cube = NxCube(7)
    for i in range(6):
        cube.state[i] = scan[i]

    center_moves = solver.solve_centers(cube)
    print("Solve cube:")
    print(f"- Solve centers: {len(center_moves)} moves")

    to_standard_pos(args, arduino)
    if not args.auto:
        input("Make sure cube is in standard position. Press enter to solve.")

    for m in tqdm(center_moves, desc="Solving centers"):
        arduino.make_move(m)


def scramble(args, arduino):
    cube = NxCube(7)
    cube.scramble()
    moves = cube.stack

    print(f"Scramble cube: {len(moves)} moves")
    if not args.auto:
        input("Press enter to scramble.")

    for m in tqdm(moves, desc="Scrambling"):
        arduino.make_move(m)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["solve", "scramble"])
    parser.add_argument("--video", type=int, default=0)
    parser.add_argument("--auto", help="No user input", action="store_true")
    parser.add_argument("--config", help="Force reconfigure", action="store_true")
    args = parser.parse_args()

    arduino = Arduino("/dev/ttyACM0")
    arduino.set_flipper(True)
    cap = setup_camera(args)

    print("In all cases, place cube Yellow up and Blue front.")

    # Get config
    if not args.config and os.path.isfile("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
    else:
        print("Starting configuration:")
        print("Place cube inside the robot to calibrate color of each face.")
        colors = foreach_face(arduino, avg_face_color, (cap,))
        config = {"colors": colors}
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        to_standard_pos(args, arduino)

    # Do action
    try:
        if args.action == "solve":
            solve(args, config, arduino, cap)
        elif args.action == "scramble":
            scramble(args, arduino)
    except KeyboardInterrupt:
        print("Keyboard interrupt. Exiting...")

    # Cleanup
    print("Turning off motors...")
    time.sleep(2)
    arduino.set_height(0)
    arduino.set_flipper(True)
    time.sleep(2)
    arduino.off()


if __name__ == "__main__":
    main()
