from sensors.base_sensor import Sensor


class Sensor_Temp(Sensor):
    def __init__(self, port):
        super().__init__(
            port=port,
            name="Sensor_Resis",
            description="Резистивиметр",
            columns="dU"
        )

    def decode_data(self, raw_data):
        # Декодирование данных
        print(raw_data)
        return int(raw_data)
