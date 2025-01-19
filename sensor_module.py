import serial
import threading
import time
import queue
import logging

class SensorModule:
    def __init__(self):
        self.serial_port = None
        self.time_sleep = 1
        self.is_recording = False
        self.data_queue = queue.Queue()
        self.thread = None

    def configure_port(self, port, baudrate):
        self.serial_port = serial.Serial(port, baudrate)

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.thread = threading.Thread(target=self.read_data)
            self.thread.start()

    def stop_recording(self):
        self.is_recording = False
        if self.thread:
            self.thread.join()
            self.thread = None

    def read_data(self):
        while self.is_recording:
            try:
                if self.serial_port.in_waiting > 0:
                    # data = self.serial_port.readline().decode('utf-8').strip()
                    data = self.serial_port.readline().strip()
                    filtered_data = self.filter_data(data)
                    self.data_queue.put(filtered_data)
                    self.save_data(filtered_data)
                time.sleep(self.time_sleep)  # Задержка в self.time_sleep секунд
            except Exception as e:
                logging.error(f"Error reading data: {e}")
                time.sleep(1)

    def filter_data(self, data):
        # Реализуйте фильтрацию данных
        return data

    def save_data(self, data):
        # Реализуйте сохранение данных в базу данных или файл
        print(data)
        pass

    def get_time_sleep(self):
        return self.time_sleep

    def set_time_sleep(self, time_sleep):
        self.time_sleep = time_sleep

    def get_latest_data(self):
        if not self.data_queue.empty():
            return self.data_queue.get()
        return None

    def close(self):
        if self.serial_port:
            self.serial_port.close()