import curses
import json
import os
import sys
import time
from pathlib import Path
ROOT = Path(__file__).absolute().parent.parent.parent
sys.path.append(str(ROOT))

import cv2
from rubiks import Color, NxCube, NxCubeMove, solver

from arduino import Arduino
from detect import detect_cube, avg_color


def center_text(stdscr: "curses._CursesWindow", text: str, pos: tuple[int, int]):
    """
    :param pos: (y, x)
    """
    y = pos[0]
    x = pos[1] - len(text) // 2
    stdscr.addstr(y, x, text)


def gui(stdscr: "curses._CursesWindow", arduino, config):
    curses.noecho()
    stdscr.nodelay(True)

    stdscr.clear()
    h, w = stdscr.getmaxyx()
    center_text(stdscr, "Rubik's Cube Solver", (0, w//2))
    stdscr.refresh()

    if config is None:
        config_win = stdscr.subwin(h-4, w-4, 2, 2)
        h, w = config_win.getmaxyx()
        center_text(config_win, "Config file not found", (0, w//2))
        center_text(config_win, "Place solved cube in robot with Yellow on top and Blue in front.", (1, w//2))
        center_text(config_win, "Aim a webcam at the robot so all fiducials and the cube are visible.", (0, w//2))
        center_text(config_win, "The robot will move to get the colors of each face.", (0, w//2))
        config_win.refresh()

        status_win = stdscr.subwin(h-4, w-4, 4, 2)
        colors = [1, 2, 3, 4, 0, 5]
        rgb_colors = []
        curr_detect = None
        cap = cv2.VideoCapture(0)
        while True:
            time.sleep(0.1)

            ret, img = cap.read()
            img = detect_cube(img)
            if img is not None:
                curr_detect = tuple(avg_color(img))

            status_win.addstr(0, 0, f"Color: {Color.col_to_name(colors[0])}")
            status_win.addstr(1, 0, "Detected: {}".format(str(curr_detect) if curr_detect is not None else "None"))
            if curr_detect:
                status_win.addstr(2, 0, "Press any key to continue")
            status_win.refresh()

            # Check for key press
            if status_win.getch() != -1:
                if curr_detect:
                    rgb_colors.append(curr_detect)
                    colors.pop(0)
                    curr_detect = None
                    raise ValueError("IT WORKS")

    while True:
        stdscr.refresh()


def main():
    arduino = Arduino("/dev/ttyACM0")
    if os.path.isfile("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
    else:
        config = None

    try:
        curses.wrapper(gui, arduino, config)
    except KeyboardInterrupt:
        pass

    print("Turning off motors...")
    time.sleep(1)
    arduino.set_height(0)
    arduino.off()


if __name__ == "__main__":
    main()
