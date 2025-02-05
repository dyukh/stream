import streamlit as st
import pandas as pd

# import numpy as np
# import matplotlib.pyplot as plt
import plotly.express as px
import logging
import os
import serial
import serial.tools.list_ports

from sensors import load_sensors
from experiment import Experiment  # модуль работы с датчиком


columns = "Date,Time,Расход,Давление,R1,R2,R3,R4,U5,Температура".split(",")
col_vis = "DateTime,Расход,Давление,Вес,R1,R2,R3,R4,U5,Температура".split(",")
col_plot = "DateTime,Давление,Вес".split(",")
D = 10.5
L = 13.8

# Session state variables
if "is_running" not in st.session_state:
    st.session_state["is_running"] = False
if "port" not in st.session_state:
    st.session_state["port"] = "COM1"
# if "record_delay" not in st.session_state:
#     st.session_state["record_delay"] = 1
if "datalist" not in st.session_state:
    st.session_state["datalist"] = []
if "experiment" not in st.session_state:
    st.session_state["experiment"] = Experiment()

experiment = st.session_state["experiment"]
"""Experiment: main variable with Experiment (list of sensors and functions)"""


@st.cache_resource
def setup_logger():
    """Инициализация логгера с кэшированием"""
    logger = logging.getLogger("stream_app")
    logger.setLevel(logging.DEBUG)

    # Форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Обработчик для записи в файл
    if not os.path.exists("logs"):
        os.makedirs("logs")
    file_handler = logging.FileHandler("logs/stream_app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Получаем логгер
logger = setup_logger()

# Логирование
logger.info("Запуск приложения Streamlit")


def get_COM_list():
    """Получение доступных COM-портов

    Returns:
        tuple: (clist, dlist, kindex)

            clist: список COM-портов.

            dlist: список описаний COM-портов.

            kindex: индекс первого USB-to-serial порта (или 0)
    """
    clist = []
    dlist = []
    plist = serial.tools.list_ports.comports(include_links=False)
    for p in plist:
        clist.append(p.device)
        dlist.append(p.description)
        # st.write(p.name, p.description)
        # st.write(p)

    key = serial.tools.list_ports.grep("USB")
    k = next(key, None)
    if k is not None:
        kindex = dlist.index(k.description)
    else:
        kindex = 0

    # st.write(k, kindex)
    return clist, dlist, kindex


st.title("Эксперимент")

# st.divider()

# Загружаем все доступные сенсоры
sensors_classes = load_sensors()
sensor_names = [sensor_name for sensor_name, sensor_class in sensors_classes.items()]

clist, dlist, ckey = get_COM_list()

# Настройка боковой панели
st.sidebar.title("Экспериментальная установка")
with st.sidebar.expander("Добавить сенсор", expanded=True):
    # for sensor_name, sensor_class in sensors_classes.items():
    #     st.write(sensor_name)

    with st.form("add_new_sensor"):
        newport = st.selectbox(
            "Порт",
            options=clist,
            index=ckey,
            label_visibility='collapsed',
        )
        newtype = st.selectbox(
            "Сенсор",
            options=sensor_names,
            label_visibility='collapsed',
        )
        newtitle = st.text_input("Заголовок", "")
        addnew = st.form_submit_button('Добавить')

    if addnew:
        newsensor = sensors_classes[newtype](port=newport)
        experiment.add_sensor(newsensor)

with st.sidebar.expander("Сенсоры", expanded=True):
    for sensor in experiment.sensors:
        st.markdown("**" + sensor.port + ":** " + sensor.description)


st.sidebar.title("Параметры")


def runing_callback():
    """Запуск или останов, реакция на кнопку"""
    st.sidebar.write(st.session_state["is_running"])
    if st.session_state["is_running"]:
        # start recording
        # experiment.sensors[0].configure_port(ard_port, 9600)
        experiment.start_recording()
        st.sidebar.success("Запись начата!")
    else:
        # stop recording
        experiment.stop_recording()
        st.sidebar.success("Запись остановлена!")


def delay_callback():
    """Применяет изменения времени задержки междуи змерениями"""
    st.session_state["experiment"].set_time_sleep(st.session_state["record_delay"])


run = st.sidebar.toggle(
    ":red-background[**Запись**]",
    key="is_running",
    on_change=runing_callback,
)

st.sidebar.success(f"файл: {experiment.get_fname()}")

record_delay = st.sidebar.number_input(
    "Задержка между измерениями, с",
    # value=st.session_state["record_delay"],
    min_value=1,
    max_value=3600,
    step=1,
    key="record_delay",
    on_change=delay_callback,
)

# with st.sidebar.expander("Образец", expanded=True):
#     D = st.number_input("Диаметр", value=D)
#     L = st.number_input("Длина", value=L)


if st.button("Обновить данные"):
    latest_data = experiment.get_data()
    if latest_data:
        st.session_state["datalist"].extend(latest_data)
    df = pd.DataFrame(
        st.session_state["datalist"][-1000:], columns=["Время", "Показания"]
    )
    plot = px.scatter(df, x="Время", y="Показания")
    st.plotly_chart(plot)
    col1, col2 = st.columns(2)
    col1.dataframe(df)
    col2.write(df.describe())
