import serial
import time
import random

# Создаем виртуальный COM-порт (нужно установить com0com)
port = 'COM6'  # Укажите ваш виртуальный порт
baudrate = 9600

with serial.Serial(port, baudrate, timeout=1) as ser:
    while True:
        # Отправляем строку
        data = str(random.randint(0, 100)) + '\n'
        ser.write(data.encode())
        print(f"Sent: {data.strip()}")
        time.sleep(1)