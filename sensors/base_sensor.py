import serial
import logging

# Получаем логгер
logger = logging.getLogger("stream_app")


class Sensor:
    """Класс сенсорного модуля.

    Attributes:
        port (str): Имя порта (например, 'COM3' или '/dev/ttyUSB0').
        baudrate (int): Скорость передачи данных (например, 9600).
        timeout (int): Таймаут в секундах (сколько максимум ждать данные).
        name (str): Короткое название.
        description (str): Длинное название, или описание.
        columns (str): Строка с заголовками --- именами колонок в возвращаемом значении.

    """        
    def __init__(
        self,
        port,
        baudrate=9600,
        timeout=10,
        name="Sensor1",
        description="Abstract sensor",
        columns="Data1",
    ):
        """Инициализирует объект Sensor с настройками по умолчанию."""
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.name = name
        self.description = description
        self.columns = columns
        self.serial = None
        logger.debug(f"Инициализация сенсора: {self.name}")

    def open(self):
        """Открыть порт для чтения"""
        logger.debug(f"Открываем порт: {self.port} сенсора: {self.name}")
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Порт {self.port} открыт.")
        except serial.SerialException as e:
            print(f"Ошибка при открытии порта {self.port}: {e}")

    def close(self):
        """Закрыть порт для чтения, если он открыт"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            logger.debug(f"Закрываем порт: {self.port} сенсора: {self.name}")
        print(f"Порт {self.port} закрыт.")

    def read_data(self):
        """Чтения порции данных сенсора."""
        if self.serial and self.serial.is_open:
            raw_data = self.serial.readline().strip()
            return self.decode_data(raw_data)
        return None

    def decode_data(self, raw_data):
        """ Декодирование данных: абстрактный сенсор.
        
        Эта функция должна быть переопределена в конкретных сенсорах, 
        переводить строку-ответ в список чисел.

        Сейчас просто возвращает *как есть*.
        """
        return raw_data.decode("utf-8")
