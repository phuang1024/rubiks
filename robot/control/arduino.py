"""
Interface with the Arduino board.
"""

import struct
import sys
import time

import serial


class Arduino:
    turner_spr = 1600

    def __init__(self, port: str):
        print("Connecting to", port)
        self.ser = serial.Serial(port, 9600)
        time.sleep(2)
        self._flush_input()

        self._pusher_pos = 0

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
        self._set_servo(0 if state else 88)

    def turn(self, qturns: int, time: float = 0.25):
        """
        Turn ``qturns`` quarter turns.
        Positive is cw, negative is ccw.

        :param time: Is scaled by qturns.
        """
        dir = qturns > 0
        qturns = abs(qturns)
        steps = qturns * self.turner_spr // 4
        self._motor_step(0, dir, steps, time * qturns)

    def set_height(self, height: int, time: float = 0.5):
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
            pos = 2300 + 280 * (height-2)

        delta = pos - self._pusher_pos
        time = time * abs(delta) / 2500
        self._motor_step(1, delta < 0, abs(delta), time)
        self._pusher_pos = pos
