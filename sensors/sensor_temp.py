from sensors.base_sensor import Sensor

class Sensor_Temp(Sensor):
    def __init__(self, port):
        super().__init__(port, name="Sensor_Temp", description="Temperature Sensor", columns='Temp')

    def decode_data(self, raw_data):
        # Декодироsвание данных
        print(raw_data)
        return (int(raw_data))