# -*- coding: utf-8 -*-
"""Чтение из COM-порта.

Для целей тестирования. Можно использовать совместно с ``serialwriter.py``.
"""

import serial
import time


port = "COM5"
baudrate = 9600


def main():
    with serial.Serial(port, baudrate, timeout=1) as ser:
        while True:
            data = ser.readline().strip()
            print(data.decode())
            time.sleep(1)


if __name__ == "__main__":
    main()
