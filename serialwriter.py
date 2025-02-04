# -*- coding: utf-8 -*-
"""Запись в COM-порт.

Для целей тестирования, пишет в порт строку со случайным числом.
Нужен 0-модем.

    Windows: com0com

    Linux: socat
"""
import serial
import time
import random


port = 'COM6'
baudrate = 9600

def main():
    with serial.Serial(port, baudrate, timeout=1) as ser:
        while True:
            # Отправляем строку
            data = str(random.randint(0, 100)) + '\n'
            ser.write(data.encode())
            print(f"Sent: {data.strip()}")
            time.sleep(1)


if __name__ == "__main__":
    main()