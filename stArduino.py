import streamlit as st
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import altair as alt
import datetime
import serial
import serial.tools.list_ports
from sensor_module import SensorModule  # модуль работы с датчиком

columns = "Date,Time,Расход,Давление,R1,R2,R3,R4,U5,Температура".split(",")
columns_vis = "DateTime,Расход,Давление,Вес,R1,R2,R3,R4,U5,Температура".split(",")
columns_plot = "DateTime,Давление,Вес".split(",")
D = 10.5
L = 13.8

# Session state variables
if "is_running" not in st.session_state:
    st.session_state["is_running"] = False
if "port" not in st.session_state:
    st.session_state["port"] = "COM1"
# if "record_delay" not in st.session_state:
#     st.session_state["record_delay"] = 1
if "sensor" not in st.session_state:
    st.session_state["sensor"] = SensorModule()

sensor = st.session_state["sensor"]


def toTime(col):
    m, d = col.split(",")
    t = int(m) + int(d) / 100
    dt = datetime.timedelta(seconds=t)
    # print (dt)
    return dt


def my_to_datetime(col):
    print(col)
    return pd.to_datetime(col, format="%d.%m.%Y %S,%f")


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
        clist.append(p.name)
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


# Настройка боковой панели
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
        sensor.configure_port(ard_port, 9600)
        sensor.start_recording()
        st.sidebar.success("Запись начата!")
    else:
        # stop recording
        sensor.stop_recording()
        st.sidebar.success("Запись остановлена!")


if ard_port:
    run = st.sidebar.toggle(":red-background[**Запись**]", key="is_running", on_change=runing_callback)

st.sidebar.success(f"файл: {sensor.get_fname()}")

record_delay = st.sidebar.number_input(
    "Задержка между измерениями, с",
    # value=st.session_state["record_delay"],
    min_value=1,
    max_value=600,
    step=1,
    key="record_delay",
)

with st.sidebar.expander("Образец", expanded=True):
    D = st.number_input("Диаметр", value=D)
    L = st.number_input("Длина", value=L)


if st.button("Получить последние данные"):
    latest_data = sensor.get_latest_data()
    if latest_data:
        st.write(f"Последние данные: {latest_data}")
    else:
        st.write("Нет новых данных.")

data = importData("1.txt")


with st.expander("Данные в таблице", expanded=False):
    rev = st.toggle("Последние сверху", value=True)
    if rev:
        showdata = data[columns_vis].iloc[::-1]
    else:
        showdata = data[columns_vis]
    st.dataframe(data=showdata,
                 use_container_width=True,
                 height=300,
                 hide_index=True
                 )

with st.expander("Графики", expanded=True):
    cWeight = (
        alt.Chart(data[columns_vis])
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
        alt.Chart(data[columns_vis])
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
