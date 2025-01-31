from sensors.base_sensor import Sensor


class Sensor_Temp(Sensor):
    def __init__(self, port):
        super().__init__(
            port=port, name="Sensor_Resis", description="Резистивиметр", columns="dU"
        )

    def decode_data(self, raw_data):
        """Декодирование данных: резистивиметр.

        В этом модуле ожидаем просто целое число.
        Это разность потенциалов на приемных электордах (в единицах АЦП),
        её ещё надо будет пересчитать в кажущиеся сопротивления.
        """
        print(raw_data)
        return int(raw_data)
