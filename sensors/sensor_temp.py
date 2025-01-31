from sensors.base_sensor import Sensor


class Sensor_Temp(Sensor):
    def __init__(self, port):
        super().__init__(
            port=port,
            name="Sensor_Temp",
            description="Термометр",
            columns="Температура",
        )

    def decode_data(self, raw_data):
        """Декодирование данных: термометр.

        В этом модуле ожидаем действительное число, значение температуры.
        """
        print(raw_data)
        return float(raw_data)
