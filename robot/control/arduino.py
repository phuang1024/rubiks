"""
Interface with the Arduino board.
"""

import struct
import sys
import time

import serial
from rubiks import NxCube, NxCubeMove, Color


class Arduino:
    turner_spr = 1600
    cube_size = 7

    def __init__(self, port: str):
        print("Connecting to", port)
        self.ser = serial.Serial(port, 9600)
        time.sleep(2)
        self._flush_input()

        self._pusher_pos = 0
        self._flipper_pos = True
        # 1x1x1 cube to track state.
        self._state = NxCube(1)

    def _write(self, data: bytes | list):
        if isinstance(data, list):
            data = bytes(data)
        self.ser.write(data)
        self.ser.flush()

    def _read(self, size: int) -> bytes:
        return self.ser.read(size)

    def _flush_input(self):
        self.ser.read(self.ser.in_waiting)

    def test(self):
        print("Testing connection")
        for i in range(255):
            self._write([0, i])
            resp = self._read(2)[0]
            assert resp == i, f"Expected {i}, got echo {resp}"
        self._flush_input()

    def _set_servo(self, angle: int):
        self._write([1, angle])
        self._read(1)
        self._flush_input()

    def _motor_state(self, i: int, on: bool):
        """
        Turn stepper on or off.
        """
        code = 3 if on else 2
        self._write([code, i])
        self._read(1)
        self._flush_input()

    def _motor_step(self, i: int, dir: bool, steps: int, total_time: float):
        """
        Step stepper motor.
        """
        if steps == 0:
            return
        assert steps > 0

        step_time = int(1e6 * total_time / steps)
        assert step_time < 65536, "Step time too large"
        assert steps < 65536, "Too many steps"

        self._write([4, i, dir, *struct.pack(">HH", steps, step_time)])
        self._read(1)
        self._flush_input()

    def off(self):
        self._motor_state(0, False)
        self._motor_state(1, False)

    def on(self):
        self._motor_state(0, True)
        self._motor_state(1, True)

    def set_flipper(self, state: bool):
        self._set_servo(0 if state else 86)
        self._flipper_pos = state

    def turn(self, qturns: int, time: float = 0.5, wipe: int = 15):
        """
        Turn ``qturns`` quarter turns.
        Positive is cw, negative is ccw.

        :param time: Is scaled by qturns.
        :param wipe: Overshoot to compensate for looseness.
        """
        dir = qturns > 0
        qturns = abs(qturns)
        steps = qturns * self.turner_spr // 4
        self._motor_step(0, dir, steps, time * qturns)
        self._motor_step(0, dir, wipe, 0.05)
        self._motor_step(0, not dir, wipe, 0.05)

    def set_height(self, height: int, time: float = 1):
        """
        :param height: 0 to 7: 0 = at bottom, 1 = turn 1 layer,
            2 = turn 2 layers, etc. 7 = turn all layers.
        :param time: Is scaled by move distance.
        """
        if height == 0:
            pos = 0
        elif height == 7:
            pos = 3870
        else:
            pos = 2340 + 280 * (height-2)

        delta = pos - self._pusher_pos
        time = time * abs(delta) / 2500
        self._motor_step(1, delta < 0, abs(delta), time)
        self._pusher_pos = pos

    def make_move(self, move: NxCubeMove):
        curr_top = self._state.state[0][0][0]
        if move.face not in (curr_top, Color.opposite(curr_top)):
            for i in range(1, 5):
                if self._state.state[i][0][0] == move.face:
                    break
            else:
                raise ValueError()

            if i in (1, 3):
                if (i == 3 and self._flipper_pos == True) or (i == 1 and self._flipper_pos == False):
                    self.set_height(7)
                    self.turn(2)
                    for _ in range(2):
                        self._state.move(NxCubeMove(0, True))
            else:
                self.set_height(7)
                dir = 1 if (i == 4) ^ self._flipper_pos else -1
                self.turn(dir)
                self._state.move(NxCubeMove(0, True if dir == 1 else False))
            self.set_height(0)
            self._state.move(NxCubeMove(2, self._flipper_pos))
            self.set_flipper(not self._flipper_pos)

        dir = move.dir
        slices = move.slices
        if slices is None:
            slices = (0, 1)
        if move.face == Color.opposite(curr_top):
            dir = not dir
            slices = [7-s for s in slices]

        slices = sorted(slices)
        if slices[0] != 0:
            self.set_height(slices[0])
            self.turn(1 if (not dir) else -1)
        self.set_height(slices[1])
        self.turn(1 if dir else -1)
