import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import datetime


columns = "Date,Time,Расход,Давление,R1,R2,R3,R4,U5,Температура".split(",")
columns_vis = "DateTime,Расход,Давление,Вес,R1,R2,R3,R4,U5,Температура".split(",")
columns_plot = "DateTime,Давление,Вес".split(",")
D = 10.5
L = 13.8

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
        sep="\s+",
        names=columns,
        converters={"Time": toTime},
        # parse_dates=[['Date','Time']],
        # date_parser = my_to_datetime,
        parse_dates=["Date"],
        dayfirst=True,
        skiprows=lambda x: x % 2,
    )
    data2 = pd.read_csv(
        fname, sep="\s+", names=["Вес", "g"], skiprows=lambda x: not x % 2
    )
    data = pd.concat([data1, data2], axis=1)
    data["DateTime"] = data["Date"] + data["Time"]
    return data


st.title('Эксперимент')

#st.divider()


# Настройка боковой панели
st.sidebar.title("Параметры")

st.sidebar.button("Stop", type="primary")

with st.sidebar.expander("Порты", expanded=True):
    ard_port = st.selectbox(
        "Порт Arduino",
        ("COM1", "COM2", "COM3", "COM4"),
        index=1,
    )
    w_port = st.selectbox(
        "Весы",
        ("COM1", "COM2", "COM3", "COM4"),
        index=0,
    )

with st.sidebar.expander("Образец", expanded=True):
    D = st.number_input("Диаметр", value = D)
    L = st.number_input("Длина", value = L)


data = importData("1.txt")

with st.expander("Данные в таблице", expanded=False):
    rev = st.toggle("Последние сверху", value=True)
    if(rev):
        showdata = data[columns_vis].iloc[::-1]
    else:
        showdata = data[columns_vis]
    st.dataframe(data=showdata, 
                use_container_width=True, 
                height = 300,
                hide_index=True)

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
                title='Вес, г',
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
                title='Давление, гектоПаскали',
            ),
        )
        .interactive()
    )
    st.altair_chart(cPres, use_container_width=True)
