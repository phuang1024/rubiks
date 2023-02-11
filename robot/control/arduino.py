"""
Interface with the Arduino board.
"""

import struct
import time

import serial


class Arduino:
    def __init__(self, port: str):
        print("Connecting to", port)
        self.ser = serial.Serial(port, 9600)
        time.sleep(2)

    def write(self, data: bytes | list):
        if isinstance(data, list):
            data = bytes(data)
        self.ser.write(data)
        self.ser.flush()

    def read(self, size: int) -> bytes:
        return self.ser.read(size)

    def test(self):
        print("Testing connection")
        for i in range(255):
            self.write([0, i])
            resp = self.read(2)[0]
            assert resp == i, f"Expected {i}, got echo {resp}"

    def set_servo(self, angle: int):
        self.write([1, angle])
        self.read(1)

    def motor_state(self, i: int, on: bool):
        """
        Turn stepper on or off.
        """
        code = 3 if on else 2
        self.write([code, i])
        self.read(1)

    def motor_step(self, i: int, steps: int, total_time: float):
        """
        Step stepper motor.
        """
        step_time = int(1e6 * total_time / steps)
        assert step_time < 65536, "Step time too large"
        self.write([4, i, steps, *struct.pack("<H", step_time)])
        self.read(1)
