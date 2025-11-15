import streamlit as st
import pandas as pd
import analysis as a3


@st.cache_data
def data():
    df_master = pd.read_csv("time_serie_pilas.csv")
    df_pilas = df_master[df_master["Localidad"] == "Pilas"]
    return a3.dataframe_precios_medios_altas_bajas_mes(df_pilas)


df = data()

st.set_page_config(layout="wide")
st.title("Observatorio de Pilas (Sevilla)\n")
st.space(size="small")
st.subheader(f"Datos desde {df["Mes"].iloc[0].lower()} hasta {df["Mes"].iloc[-1].lower()} de 2025.", divider="gray")
st.space(size="small")

st.write("Media de anuncios por mes.")
st.line_chart(df, x="Mes", y=["Media anuncios"], color=["#FF9896"])
st.space(size="small")

left_column, center_column, right_column = st.columns(3)
with left_column:
    st.write("Nuevos anuncios y anuncios borrados por mes.")
    st.line_chart(df, x="Mes", y=["Nuevos", "Borrados"], color=["#D62728", "#FF9896"])

with center_column:
    st.write("Precio medio nuevos anuncios y anuncios borrados por mes.")
    st.line_chart(df, x="Mes", y=["Precio medio nuevos", "Precio medio borrados"], color=["#1F77B4", "#AEC7E8"])

with right_column:
    st.write("Precio medio por metro cuadrado de nuevos anuncios y anuncios borrados por mes.")
    st.line_chart(df, x="Mes", y=["Precio m2 nuevos", "Precio m2 borrados"], color=["#2CA02C", "#98DF8A"])

st.subheader(f"", divider="gray")
st.write("Resumen de datos.")
st.table(data=df)

st.subheader(f"", divider="gray")
st.write("Última actualización: 15/11/2025.")
st.write("X / Twitter: @InversorPython")

