import threading
import time
import datetime
import queue
import logging
from sensor_module import SensorModule


class Experiment:
    """Класс для работы с экспериментальной установкой --- набором сенсорных модулей.

    Attributes:
        time_sleep (int): Время задержки между чтением данных (по умолчанию 1 секунда).
        is_recording (bool): Флаг, указывающий, идет ли запись данных.
        data_queue (queue.Queue): Очередь для хранения данных.
        thread (threading.Thread): Поток для чтения данных.
        fname (str): Имя файла для сохранения данных.
        file (file): Файловый объект для записи данных.
    """    
    def __init__(self):
        """Инициализирует объект Experiment с настройками по умолчанию."""
        self.sensors = []
        self.time_sleep = 1
        self.is_recording = False
        self.data_queue = queue.Queue()
        self.thread = None
        self.fname = None
        self.file = None

    def add_sensor(self, sensor):
        """Добавляет sensor в список датчиков экспериментальной установки.

        Args:
            sensor (SensorModule): объект SensorModule.
        """
        self.sensors.append(sensor)

    def start_recording(self):
        """Начинает запись данных со всех сенсоров экспериментальной установки.

        Если запись еще не начата, 
        открываются порты для каждого из сенсоров, 
        создается поток для чтения данных и файл для сохранения.
        """
        if not self.is_recording:
            self.is_recording = True
            for sensor in self.sensors:
                sensor.open()
            if self.fname is None or self.file.closed:
                self.mk_def_fname()
            self.thread = threading.Thread(target=self.read_data)
            self.thread.start()

    def stop_recording(self):
        """Останавливает запись данных экспериментальной установки.

        Ожидает завершения потока чтения данных, закрывает порты сенсоров и закрывает файл.
        """
        self.is_recording = False
        if self.thread:
            self.thread.join()
            self.thread = None
        for sensor in self.sensors:
            sensor.close()
        if self.file:
            self.file.close()

    def read_data(self):
        """Цикл чтения данных экспериментальной установки.
        
        Читает и сохраненяет данные всех сенсоров экспериментальной установки,
        после чего спит time_sleep секунд. 
        """
        while self.is_recording:
            data = []
            for sensor in self.sensors:
                data.extend(sensor.read())
            self.save_data(data)
            time.sleep(self.time_sleep)  # Задержка в self.time_sleep сек

    def save_data(self, data):
        """Сохранение одной порции данных.
        
        Может быть сохранение данных в базу данных или файл.
        Сейчас сохранет в очередь, печатает в консоль и в файл.
        """
        strt = datetime.datetime.now()
        print(data)
        if data is not None:
            self.data_queue.put(data)
            print(strt + ",", ", ".join(map(str, data)), file=self.file)
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

    def mk_def_fname(self):
        fname = time.strftime("%Y-%m-%d--%H-%M-%S.txt", time.localtime())
        self.set_fname(fname=fname)
