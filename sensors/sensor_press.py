from sensors.base_sensor import Sensor
from parse import parse

# Шаблон строки, сформированной printf
# "Date,Time,Расход,Давление,R1,R2,R3,R4,U5,Температура"
#     14.11.2024 4163,84 0 2865.63 1 2 3 4 5 -127.00
template = "{:d}.{:d}.{:d} {:d},{:d} 0 {:g} 1 2 3 4 5 -127.00"


class Sensor_Temp(Sensor):
    def __init__(self, port):
        super().__init__(
            port=port,
            name="Sensor_Press",
            description="Расход-Давление",
            columns="Давление",
        )

    def decode_data(self, raw_data):
        """Декодирование данных: давление.

        В этом модуле ожидаем много разного, но используем давление (действительное число).
        Пример данных:
                14.11.2024 4163,84 0 **2865.63** 1 2 3 4 5 -127.00
        """
        print(raw_data)
        result = parse(template, raw_data)
        if result:
            return float(result[5])
        return float("nan")
