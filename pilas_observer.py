import streamlit as st
import altair as alt
import pandas as pd
import math
import analysis as a3


def create_graph(df, line_columns, colors, x_column = "Mes", inverse = False):
    df_long = df.melt(id_vars=x_column, value_vars=line_columns,
                      var_name="Tipo", value_name="Valor")
    df_long = df_long.sort_values(x_column)

    # --- 2. Calcular la escala automáticamente entre min y max ---
    y_min = df[line_columns].min().min()
    y_max = df[line_columns].max().max()

    if inverse:
        y_min += math.ceil(y_min * 0.07)
        y_max -= math.ceil(y_max * 0.07)
    else:
        y_min -= math.ceil(y_min * 0.07)
        y_max += math.ceil(y_max * 0.07)

    # --- 3. Crear el gráfico ---
    chart = (
        alt.Chart(df_long)
        .mark_line()
        .encode(
            x=alt.X(x_column + ":N", sort=a3.Meses, title="Mes"),  # usa :N para datos categóricos
            y=alt.Y("Valor:Q",
                    title="Cantidad",
                    scale=alt.Scale(domain=[y_min, y_max])),
            color=alt.Color(
                "Tipo:N",
                scale=alt.Scale(
                    domain=line_columns,
                    range=colors  # ← tus dos colores
                )
            )
        )
        .properties(width="container", height=400)
    )
    return chart


#@st.cache_data
def data():
    df_pilas = pd.read_csv("time_serie_pilas.csv")
    return df_pilas[df_pilas["Mes"] != "Agosto"]


def st_header(df):
    st.set_page_config(layout="wide")
    st.title("Observatorio de Pilas (Sevilla)\n")
    #st.space(size="small")
    st.subheader("Análisis de datos de venta de inmuebles en Pilas para entender cómo evoluciona el mercado inmobiliario.")
    st.subheader(f"Datos desde {df["Mes"].iloc[0].lower()} hasta {df["Mes"].iloc[-1].lower()} de 2025.", divider="rainbow")
    #st.space(size="small")

    #st.subheader(f"", divider="rainbow")


###########


df = a3.dataframe_precios_medios_altas_bajas_mes(data())
st_header(df)

# Númerod e anuncios por mes

st.space(size="small")
st.header(f"Número de anuncios por mes.", divider="gray")
st.write("Media de anuncios por mes.")
#st.line_chart(df, x="Mes", y=["Media anuncios"], color=["#FF9896"])
st.altair_chart(create_graph(df, ["Media anuncios"], ["#FF9896"]))
st.space(size="small")

left_column, center_column, right_column = st.columns(3)
with left_column:
    st.write("Nuevos anuncios y anuncios borrados por mes.")
    #st.line_chart(df, x="Mes", y=["Nuevos", "Borrados"], color=["#D62728", "#FF9896"])
    st.altair_chart(create_graph(df, ["Nuevos", "Borrados"], ["#D62728", "#FF9896"]))

with center_column:
    st.write("Precio medio nuevos anuncios y anuncios borrados por mes.")
    #st.line_chart(df, x="Mes", y=["Precio medio nuevos", "Precio medio borrados"], color=["#1F77B4", "#AEC7E8"])
    st.altair_chart(create_graph(df, ["Precio medio nuevos", "Precio medio borrados"], ["#1F77B4", "#AEC7E8"]))

with right_column:
    st.write("Precio medio por metro cuadrado de nuevos anuncios y anuncios borrados por mes.")
    #st.line_chart(df, x="Mes", y=["Precio m2 nuevos", "Precio m2 borrados"], color=["#2CA02C", "#98DF8A"])
    st.altair_chart(create_graph(df, ["Precio m2 nuevos", "Precio m2 borrados"], ["#2CA02C", "#98DF8A"]))

st.subheader(f"", divider="gray")
st.write("Resumen de datos de anuncios por mes.")
st.table(data=df)

# Días de venta

st.space(size="small")
st.header(f"Días en la plataforma.", divider="blue")
df = a3.dataframe_dias_en_venta(data())
st.table(data=df)
st.text(body="Días hasta que el anuncio se da de baja definitivamente de la plataforma, probablemente por vender la propiedad.")

# Cambios de precio por mes

st.space(size="small")
st.header(f"Cambios de precios por mes.", divider="violet")
df = a3.dataframe_cambio_precios_mes(data())

left_column, center_column, right_column = st.columns(3)
with left_column:
    st.write("Anuncios con subidas y bajadas de precio.")
    st.altair_chart(create_graph(df, ["Número de subidas", "Número de bajadas"], ["#D62728", "#FF9896"]))
with center_column:
    st.write("Subida media en euros.")
    st.altair_chart(create_graph(df, ["Media de subida"], ["#1F77B4"]))
with right_column:
    st.write("Bajada media en euros.")
    st.altair_chart(create_graph(df, ["Media de bajada"], ["#2CA02C"], inverse=True))

st.subheader(f"", divider="violet")
st.write("Resumen de datos de cambios de precio por mes.")
st.table(data=df)


st.subheader(f"", divider="rainbow")
st.write("Última actualización: 19/11/2025.")
st.write("X / Twitter: @InversorPython")

