import threading
import time
import datetime
import queue
import logging


class Experiment:
    def __init__(self):
        self.sensors = []
        self.time_sleep = 1
        self.is_recording = False
        self.data_queue = queue.Queue()
        self.thread = None
        self.fname = None
        self.file = None

    def add_sensor(self,sensor):
        self.sensors.append(sensor)

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            for sensor in self.sensors:
                sensor.open()
            if self.fname is None or self.file.closed:
                self.mk_def_fname()
            self.thread = threading.Thread(target=self.read_data)
            self.thread.start()

    def stop_recording(self):
        self.is_recording = False
        if self.thread:
            self.thread.join()
            self.thread = None
        self.close()

    def close(self):
        for sensor in self.sensors:
            sensor.open()
        if self.file:
            self.file.close()

    def read_data(self):
        while self.is_recording:
            data = []
            for sensor in self.sensors:
                data.extend(sensor.read())
            self.save_data(data)
            time.sleep(self.time_sleep)  # Задержка в self.time_sleep сек

    def save_data(self, data):
        # Может быть сохранение данных в базу данных или файл
        strt = datetime.datetime.now()
        print(data)
        if data is not None:
            self.data_queue.put(data)
            print(strt+',', ", ".join(map(str, data)), file=self.file)
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
