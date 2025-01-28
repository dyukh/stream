from sensors.base_sensor import BaseSensor

class Sensor_Temp(BaseSensor):
    def __init__(self, port):
        super().__init__(port, name="Sensor_Temp", description="Temperature Sensor", columns='Temp')

    def decode_data(self, raw_data):
        # Декодирование данных
        return (int(raw_data[0]))