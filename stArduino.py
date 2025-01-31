import streamlit as st
import pandas as pd

# import numpy as np
# import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import datetime
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


# Инициализация логгера с кэшированием
@st.cache_resource
def setup_logger():
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


def toTime(col):
    m, d = col.split(",")
    t = int(m) + int(d) / 100
    dt = datetime.timedelta(seconds=t)
    # print (dt)
    return dt


def my_to_datetime(col):
    print(col)
    return pd.to_datetime(col, format="%d.%m.%Y %S,%f")


@st.cache_data
def importData(fname):
    data1 = pd.read_csv(
        fname,
        sep=r"\s+",
        names=columns,
        converters={"Time": toTime},
        # parse_dates=[['Date','Time']],
        # date_parser = my_to_datetime,
        parse_dates=["Date"],
        dayfirst=True,
        skiprows=lambda x: x % 2,
    )
    data2 = pd.read_csv(
        fname, sep=r"\s+", names=["Вес", "g"], skiprows=lambda x: not x % 2
    )
    data = pd.concat([data1, data2], axis=1)
    data["DateTime"] = data["Date"] + data["Time"]
    return data


def get_COM_list():
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

# Настройка боковой панели
st.sidebar.title("Экспериментальная установка")
with st.sidebar.expander("Сенсоры", expanded=True):
    for sensor_name, sensor_class in sensors_classes.items():
        st.write(sensor_name)


st.sidebar.title("Параметры")

clist, dlist, ckey = get_COM_list()

with st.sidebar.expander("Порты", expanded=True):
    ard_port = st.radio(
        "Порт Arduino",
        options=clist,
        captions=dlist,
        index=ckey,
    )
    w_port = st.selectbox(
        "Весы",
        options=dlist,
        index=ckey,
    )


def runing_callback():
    st.sidebar.write(st.session_state["is_running"])
    if st.session_state["is_running"]:
        # start recording
        experiment.sensors[0].configure_port(ard_port, 9600)
        experiment.start_recording()
        st.sidebar.success("Запись начата!")
    else:
        # stop recording
        experiment.stop_recording()
        st.sidebar.success("Запись остановлена!")


def delay_callback():
    st.session_state["experiment"].set_time_sleep(st.session_state["record_delay"])


if ard_port:
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

with st.sidebar.expander("Образец", expanded=True):
    D = st.number_input("Диаметр", value=D)
    L = st.number_input("Длина", value=L)


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

st.divider()

data = importData("1.txt")

with st.expander("Данные в таблице", expanded=False):
    rev = st.toggle("Последние сверху", value=True)
    if rev:
        showdata = data[col_vis].iloc[::-1]
    else:
        showdata = data[col_vis]
    st.dataframe(data=showdata, use_container_width=True, height=300, hide_index=True)

with st.expander("Графики", expanded=True):
    cWeight = (
        alt.Chart(data[col_vis])
        .mark_circle()
        .encode(
            x=alt.X(
                "DateTime",
                title="Время",
            ),
            y=alt.Y(
                "Вес",
                title="Вес, г",
            ),
        )
        .interactive()
    )
    st.altair_chart(cWeight, use_container_width=True)

    cPres = (
        alt.Chart(data[col_vis])
        .mark_circle()
        .encode(
            x=alt.X(
                "DateTime",
                title="Время",
            ),
            y=alt.Y(
                "Давление",
                title="Давление, гектоПаскали",
            ),
        )
        .interactive()
    )
    st.altair_chart(cPres, use_container_width=True)
