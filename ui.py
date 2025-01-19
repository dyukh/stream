import streamlit as st
from sensor_module import SensorModule  # Импортируйте ваш модуль работы с датчиком

sensor = SensorModule()

st.title("Датчик данных")

# Выбор COM-порта и скорости
port = st.selectbox("Выберите COM-порт", ["COM1", "COM2", "COM3"])  # Добавьте доступные порты
baudrate = st.number_input("Скорость передачи данных", value=9600)

if st.button("Начать запись"):
    sensor.configure_port(port, baudrate)
    sensor.start_recording()
    st.success("Запись начата!")

if st.button("Остановить запись"):
    sensor.stop_recording()
    st.success("Запись остановлена!")

# Отображение данных в реальном времени
if st.button("Получить последние данные"):
    latest_data = sensor.get_latest_data()
    if latest_data:
        st.write(f"Последние данные: {latest_data}")
    else:
        st.write("Нет новых данных.")