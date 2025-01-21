from sensor_module import SensorModule  # Импортируйте ваш модуль работы с датчиком
import time

sensor = SensorModule()


# Выбор COM-порта и скорости
port = "COM4"
baudrate = 9600

sensor.configure_port(port, baudrate)
sensor.start_recording()

print('Start')

for i in range(10):
    latest_data = sensor.get_data()
    print(i, latest_data)
    time.sleep(5)

sensor.stop_recording()

print('Stop')

for i in range(10):
    latest_data = sensor.get_data()
    print(i, latest_data)
    time.sleep(5)
