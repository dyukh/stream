import serial
import time
import random

# Создаем виртуальный COM-порт (нужно установить com0com)
port = 'COM5'  # Укажите ваш виртуальный порт
baudrate = 9600

with serial.Serial(port, baudrate, timeout=1) as ser:
    while True:
        data = ser.readline().strip()
        print(data.decode())
        time.sleep(1)