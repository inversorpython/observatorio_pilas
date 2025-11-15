import pandas as pd
from datetime import datetime, timedelta


Meses = (
    '',
    'Enero', 'Febrero', 'Marzo', 'Abril',
    'Mayo', 'Junio', 'Julio', 'Agosto',
    'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
)


def date_list():
    # Dejar fuera agosto porque distorsiona los datos.
    to_date = datetime.now().date()
    from_date = datetime.strptime("2025-8-28", "%Y-%m-%d").date()
    days_in_report = (to_date - from_date).days
    return [from_date + timedelta(i) for i in range(0, days_in_report)]


def stat_altas_bajas(df_base):
    #print(len(df_base))
    date_from = datetime.strptime(df_base["Fecha"].min(), "%Y-%m-%d").date()
    #print(date_from)
    date_to = datetime.strptime(df_base["Fecha"].max(), "%Y-%m-%d").date()
    #print(date_to)
    df_day = df_base[df_base["Fecha"] == str(date_from)]
    #print(df_day["Fecha"])
    id_yesterday = set(df_day["Id"].unique())
    dates = [date_from + timedelta(i) for i in range(1, (date_to - date_from).days)]
    id_altas = set()
    id_bajas = set()

    for date in dates:
        #print(date)
        df_day = df_base[df_base["Fecha"] == str(date)]
        #print(len(df_day))
        #print(df_day)

        id_today = set(df_day["Id"].unique())
        #print(len(id_today))
        alta = set(id_today) - set(id_yesterday)
        baja = set(id_yesterday) - set(id_today)
        id_altas.update(alta)
        id_bajas.update(baja)
        id_yesterday = id_today
    return id_altas, id_bajas


def stats_precios_medios_altas_bajas(df):
    id_altas, id_bajas = stat_altas_bajas(df)
    id_altas_bajas = id_altas.intersection(id_bajas)
    #print("Altas: ", len(id_altas))
    #print("Bajas: ", len(id_bajas))
    #print("Altas y Bajas mismo mes: ", len(id_altas_bajas))
    media_altas = df[df['Id'].isin(id_altas)]["Precio"].mean()
    #print(media_altas)
    m2_media_altas = round(media_altas / df[df['Id'].isin(id_altas)]["M2"].mean(), 2)
    #print("M2 ", m2_media_altas)
    media_bajas = df[df['Id'].isin(id_bajas)]["Precio"].mean()
    #print(media_bajas)
    m2_media_bajas = round(media_bajas / df[df['Id'].isin(id_bajas)]["M2"].mean(), 2)
    #print("M2 ", m2_media_bajas)
    media_altas_bajas = df[df['Id'].isin(id_altas_bajas)]["Precio"].mean()
    #print(media_altas_bajas)
    #print("M2 ", round(media_altas_bajas / df[df['Id'].isin(id_altas_bajas)]["M2"].median(), 2))
    return (len(id_altas), len(id_bajas), len(id_altas_bajas), media_altas, m2_media_altas, media_bajas, m2_media_bajas)

    # Por tipod e vivienda.


def m_media_by_days(df):
    return round(len(df) / len(df["Fecha"].unique()), 2)


def dataframe_precios_medios_altas_bajas_mes(df):
    #df_return = pd.c
    data_df = list()
    meses = df['Mes'].unique()
    for mes in meses:
        #print(mes)
        df_mes = df[df["Mes"] == mes]
        #print(f"m_media_by_days(df): ", m_media_by_days(df_mes))
        list_result = stats_precios_medios_altas_bajas(df_mes)
        data_mes = list()
        data_mes.append(mes)
        #data_mes.append(cm.Meses.index(mes))
        data_mes.append(list_result[0])
        data_mes.append(list_result[1])
        data_mes.append(list_result[3])
        data_mes.append(list_result[5])
        data_mes.append(list_result[4])
        data_mes.append(list_result[6])
        #data_mes.append(list_result[7])
        data_mes.append(m_media_by_days(df_mes))
        data_df.append(data_mes)
    #print(data_df)
    return_df = pd.DataFrame(data_df, columns=["Mes", "Nuevos", "Borrados", "Precio medio nuevos", "Precio medio borrados", "Precio m2 nuevos", "Precio m2 borrados", "Media anuncios"])
    return_df["Mes"] = pd.Categorical(return_df["Mes"], categories=Meses, ordered=True)
    return_df = return_df.sort_values("Mes")


    #return_df.set_index("Index")

    # No m ha funcionado
    #return_df.set_index("Mes")
    #return_df.index = pd.CategoricalIndex(return_df.index, categories=cm.Meses, ordered=True)
    # Ordenar por el índice
    #return_df = return_df.sort_index()

    #return_df["Index"].apply(lambda cm.M)

    return return_df
