import serial
import logging

class Sensor:
    def __init__(self, port, baudrate=9600, timeout=1, name='Sensor1', description = 'Abstract sensor', columns = 'Data1'):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.name = name
        self.description = description
        self.columns = columns

    def read_data(self):
        try:
            # Открываем порт
            with serial.Serial(self.port, self.baudrate, timeout=self.timeout) as ser:
                # Читаем данные
                raw_data = ser.readline().strip()
                return self.decode_data(raw_data)
        except serial.SerialException as e:
            print(f"Ошибка при работе с портом {self.port}: {e}")
            return None

    def decode_data(self, raw_data):
        # Пример декодирования данных
        return raw_data.decode("utf-8")