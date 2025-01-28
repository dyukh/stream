from sensors import load_sensors

def main():
    # Загружаем все доступные сенсоры
    sensors_classes = load_sensors()

    sensors = []
    for sensor_name, sensor_class in sensors_classes.items():
        sensor = sensor_class(port="COM3")  # Пример порта
        sensors.append(sensor)
        print(f"{sensor.name}")

    # Чтение данных с сенсоров
    for sensor in sensors:
        data = sensor.read_data()
        print(f"{sensor.name}: {data}")

if __name__ == "__main__":
    main()
