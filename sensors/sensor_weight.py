from sensors.base_sensor import Sensor
from parse import parse

# Шаблон строки, сформированной printf
template = "{:g} g"


class Sensor_Temp(Sensor):
    def __init__(self, port):
        super().__init__(
            port=port, name="Sensor_Weight", description="Весы", columns="Вес"
        )

    def decode_data(self, raw_data):
        """Декодирование данных: весы.

        В этом модуле ожидаем действительное число и символ g.
        Пример данных:
                6.045 g
        """
        print(raw_data)
        result = parse(template, raw_data)
        if result:
            return result[0]
        return float("nan")
