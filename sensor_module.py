import serial
import threading
import time
import datetime
import queue
import logging


class SensorModule:
    """Класс для работы с сенсорным модулем.

    Attributes:
        serial_port (serial.Serial): Последовательный порт для подключения к сенсору.
        time_sleep (int): Время задержки между чтением данных (по умолчанию 1 секунда).
        is_recording (bool): Флаг, указывающий, идет ли запись данных.
        data_queue (queue.Queue): Очередь для хранения данных.
        thread (threading.Thread): Поток для чтения данных.
        fname (str): Имя файла для сохранения данных.
        file (file): Файловый объект для записи данных.
    """

    def __init__(self):
        """Инициализирует объект SensorModule с настройками по умолчанию."""
        self.serial_port = None
        self.time_sleep = 1
        self.is_recording = False
        self.data_queue = queue.Queue()
        self.thread = None
        self.fname = None
        self.file = None

    def configure_port(self, port, baudrate):
        """Настраивает последовательный порт для подключения к сенсору.

        Args:
            port (str): Имя порта (например, 'COM3' или '/dev/ttyUSB0').
            baudrate (int): Скорость передачи данных (например, 9600).
        """
        self.serial_port = serial.Serial(port, baudrate)

    def start_recording(self):
        """Начинает запись данных с сенсора.

        Если запись еще не начата, создается поток для чтения данных и файл для сохранения.
        """
        if not self.is_recording:
            self.is_recording = True
            self.thread = threading.Thread(target=self.read_data)
            self.thread.start()
            if self.fname is None or self.file.closed:
                self.mk_def_fname()

    def stop_recording(self):
        """Останавливает запись данных с сенсора.

        Ожидает завершения потока чтения данных и закрывает файл.
        """
        self.is_recording = False
        if self.thread:
            self.thread.join()
            self.thread = None
        self.close()

    def read_data(self):
        while self.is_recording:
            try:
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.readline().decode("utf-8").strip()
                    filtered_data = self.filter_data(data)
                    if filtered_data is not None:
                        self.data_queue.put(filtered_data)
                        self.save_data(filtered_data)
                time.sleep(self.time_sleep)  # Задержка в self.time_sleep сек
            except Exception as e:
                logging.error(f"Error reading data: {e}")
                time.sleep(1)

    def filter_data(self, data):
        # Здесь должна быть фильтрацию данных
        # Но пока я просто добавляю текущее время
        # И предполагается что в data напечатано целое число
        if data is not None:
            strt = datetime.datetime.now()
            ret_data = [strt, int(data)]
            return ret_data
        return None

    def save_data(self, data):
        # Может быть сохранение данных в базу данных или файл
        print(data)
        if data is not None:
            print(", ".join(map(str, data)), file=self.file)
            self.file.flush()

    def get_time_sleep(self):
        return self.time_sleep

    def set_time_sleep(self, time_sleep):
        self.time_sleep = time_sleep

    def get_latest_data(self):
        if not self.data_queue.empty():
            return self.data_queue.get()
        return None

    def get_data(self):
        result_list = []
        while not self.data_queue.empty():
            result_list.append(self.data_queue.get())
        return result_list

    def get_fname(self):
        return self.fname

    def set_fname(self, fname):
        if self.file is not None and not self.file.closed:
            self.file.close()
            logging.info(f"Closing file: {self.fname}")
        self.fname = fname
        logging.info(f"Open file: {fname}")
        try:
            self.file = open(fname, "a+")
        except OSError:
            logging.error(f"Can not open file for writing: {fname}")

    def close(self):
        if self.serial_port:
            self.serial_port.close()
        if self.file:
            self.file.close()

    def mk_def_fname(self):
        fname = time.strftime("%Y-%m-%d--%H-%M-%S.txt", time.localtime())
        self.set_fname(fname=fname)
