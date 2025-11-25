import pandas as pd
from datetime import datetime, timedelta


Meses = (
    '',
    'Enero', 'Febrero', 'Marzo', 'Abril',
    'Mayo', 'Junio', 'Julio', 'Agosto',
    'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
)


def column_mes(df_p, column_name = "Fecha"):
    df_p['Mes'] = df_p[column_name].apply(lambda x: Meses[x.month] if not pd.isna(x) else "")


def sort_by_month(return_df):
    return_df.reset_index()
    return_df["Mes"] = pd.Categorical(return_df["Mes"], categories=Meses, ordered=True)
    return_df = return_df.sort_values("Mes")
    return return_df


def dt(string_date):
    return datetime.strptime(string_date, "%Y-%m-%d").date()


def date_list(from_date = None, to_date = None):
    # Dejar fuera agosto porque distorsiona los datos.
    if to_date is None:
        to_date = datetime.now().date()
    else:
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
    if from_date is None:
        from_date = datetime.strptime("2025-9-1", "%Y-%m-%d").date()
    else:
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    days_in_report = (to_date - from_date).days
    return [from_date + timedelta(i) for i in range(0, days_in_report+1)]


def range_dates_from(df_base):
    date_from = dt(df_base["Fecha"].min())
    #print(date_from)
    date_to = datetime.strptime(df_base["Fecha"].max(), "%Y-%m-%d").date()
    #print(date_to)
    df_day = df_base[df_base["Fecha"] == str(date_from)]
    #print(df_day["Fecha"])
    id_yesterday = set(df_day["Id"].unique())
    dates = [date_from + timedelta(i) for i in range(0, (date_to - date_from + timedelta(1)).days)]
    return dates, id_yesterday


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
    #return_df["Mes"] = pd.Categorical(return_df["Mes"], categories=Meses, ordered=True)
    #return_df = return_df.sort_values("Mes")


    #return_df.set_index("Index")

    # No m ha funcionado
    #return_df.set_index("Mes")
    #return_df.index = pd.CategoricalIndex(return_df.index, categories=cm.Meses, ordered=True)
    # Ordenar por el índice
    #return_df = return_df.sort_index()

    #return_df["Index"].apply(lambda cm.M)

    return sort_by_month(return_df)


def stats_cambio_de_precios(df):
    dates = date_list(df["Fecha"].min(), df["Fecha"].max())
    df_yesterday = df[df["Fecha"] == dates.pop(0)]
    price_changes = list()
    for date in dates:
        df_today = df[df["Fecha"] == str(date)]
        # print(f"{date}: {len(df_today)}")
        id_yesterday = set(df_yesterday["Id"])
        for today_row in df_today.itertuples():
            if today_row.Id not in id_yesterday:
                continue
            df_row_yesterday = df_yesterday[df_yesterday['Id'] == today_row.Id]
            # Tengo Ids en distintas entradas
            #if len(df_row_yesterday) != 1:
            #    print(f"Error. dfrow_yesterady {len(df_row_yesterday)}")
            #    print(df_row_yesterday)
            price_yesterday =  df_row_yesterday.iloc[0]['Precio']
            price_today = today_row.Precio
            if price_yesterday != price_today:
                #print(f"Inmueble {today_row.Id} pasa de {df_row_yesterday['Precio']} a {today_row.Precio} en {date}.")
                price_changes.append({"Id": today_row.Id,
                                      'Precio original': price_yesterday,
                                      'Precio nuevo': price_today,
                                      'Diferencia precio': price_today - price_yesterday,
                                      'Fecha': str(date)})
        df_yesterday = df_today
    return price_changes


def dataframe_cambio_precios_mes(df):
    data_df = list()
    meses = df['Mes'].unique()
    for mes in meses:
        #print(mes)
        df_mes = df[df["Mes"] == mes]
        #print(f"df {len(df)} df_mes {len(df_mes)}")
        #print(f"m_media_by_days(df): ", m_media_by_days(df_mes))
        list_result = stats_cambio_de_precios(df_mes)
        data_mes = list()
        data_mes.append(mes)
        data_mes.append(len(list_result)) # Num cambios de precio

        # % anuncios cmabian
        #print(f"len(list_result) {len(list_result)} / len(df_mes) {len(df_mes)}")
        tmp = round(len(list_result) / m_media_by_days(df_mes), 2) * 100
        data_mes.append(str(tmp)+"%")

        tmp = filter(lambda x: x['Diferencia precio'] < 0, list_result)
        decrease_changes = [x['Diferencia precio'] for x in tmp]
        tmp = filter(lambda x: x['Diferencia precio'] > 0, list_result)
        increase_changes = [x['Diferencia precio'] for x in tmp]
        data_mes.append(len(decrease_changes)) # Rebaja
        data_mes.append(len(increase_changes)) # Aumenta
        if len(decrease_changes) > 0:
            data_mes.append(round(sum(decrease_changes) / len(decrease_changes), 2)) # Media rebajas
        else:
            data_mes.append(0)  # Media rebajas
        if len(increase_changes) > 0:
            data_mes.append(round(sum(increase_changes) / len(increase_changes), 2)) # Media incremento
        else:
            data_mes.append(0)  # Media incremento
        data_df.append(data_mes)
    #print(data_df)
    return_df = pd.DataFrame(data_df,
                columns=["Mes", "Cambio precios",
                         "% anuncios cambian", "Número de bajadas",
                         "Número de subidas", "Media de bajada",
                         "Media de subida"])
    #return_df["Mes"] = pd.Categorical(return_df["Mes"], categories=Meses, ordered=True)
    #return_df = return_df.sort_values("Mes")
    return sort_by_month(return_df)


def stats_dias_en_venta(df_base):
    """
    Un id puede tener varias altas y bajas. Si al final iene un úmerod e dñías de 0 significa que ha encontrado un alta sin baja.
    :param df_base:
    :return:
    """
    id_dias_fechas = dict()
    id_log = dict()

    def add_alta(id_, fecha):
        if id_ not in id_log:
            id_log[id_] = [f"Alta:{str(fecha)}"]
        else:
            id_log[id_].append(f"Alta:{str(fecha)}")
        if id_ not in id_dias_fechas:
            id_dias_fechas[id_] = {'Fecha alta':fecha, 'Fecha baja': None, 'Dias': 0}
        else:
            if id_dias_fechas[id_]['Fecha alta'] is not None:
                #print(f"Warning {id_} has a previous date { id_dias_fechas[id_]['Fecha alta']} than {fecha}")
                id_dias_fechas[id_]['Fecha baja'] = None
                id_dias_fechas[id_]['Dias'] = 0
                return
            id_dias_fechas[id_]['Fecha alta'] = fecha

    def add_baja(id_, fecha, dias):
        if id_ not in id_log:
            id_log[id_] = [f"Baja:{str(fecha)}"]
        else:
            id_log[id_].append(f"Baja:{str(fecha)}")
        if id_ not in id_dias_fechas:
            id_dias_fechas[id_] = {'Fecha alta':None, 'Fecha baja': fecha, 'Dias': dias}
        else:
            id_dias_fechas[id_]['Fecha baja'] = fecha
            id_dias_fechas[id_]['Dias'] = dias

    dates, id_yesterday = range_dates_from(df_base)
    df_today = df_base[df_base["Fecha"] == df_base['Fecha'].min()]
    #print(f"Fecha origen {dates[0]} - {dates[-1]}")
    for date in dates:
        #print(str(date))
        #df_yesterday = df_today
        df_today = df_base[df_base["Fecha"] == str(date)]
        #print(f"Today: {len(df_today)}")
        #print(df_day)
        id_today = set(df_today["Id"].unique())
        #print(len(id_today))
        altas = set(id_today) - set(id_yesterday)
        for id_alta in altas:
            add_alta(id_alta, date)
        bajas = set(id_yesterday) - set(id_today)
        for id_baja in bajas:
            if id_baja not in id_dias_fechas:
                continue
            fecha_alta = id_dias_fechas[id_baja]['Fecha alta']
            diff = date - fecha_alta
            dias_venta = diff.days
            if diff.seconds > 0:
                dias_venta += 1
            #print("Resta", dias_venta,"<<") # Es un timedelta
            #id_dias[id_baja] = dias_venta
            add_baja(id_baja, date, dias_venta)
           # df_yesterday.loc[df_yesterday["Id"] == id_baja, 'Días en venta'] = dias_venta

            #print(df_yesterday[df_yesterday["Id"] == id_baja]["Fecha alta"])

        id_yesterday = id_today
    return id_dias_fechas, id_log


def dataframe_dias_en_venta(df):
    dict_fechas_dias, _ = stats_dias_en_venta(df)
    dict_altas_con_bajas = {k:v for k,v in dict_fechas_dias.items() if v['Fecha alta'] is not None and v['Fecha baja'] is not None and v['Dias'] > 1}
    list_dias = [v['Dias'] for _,v in dict_altas_con_bajas.items()]
    df_data = [round(sum(list_dias)/len(list_dias), 2), max(list_dias), min(list_dias)]
    #print(df_data)
    return pd.DataFrame((df_data,), columns=("Media días", "Máximo días", "Mínimo días"))


def dataframe_dias_en_venta_2(df):
    dict_fechas_dias, dict_log = stats_dias_en_venta(df)
    dict_altas_con_bajas = {k:v for k,v in dict_fechas_dias.items() if v['Fecha alta'] is not None and v['Fecha baja'] is not None and v['Dias'] > 1}
    #df_dias_ventas = pd.DataFrame(dict_altas_con_bajas)
    df_dias_ventas = pd.DataFrame.from_dict(dict_altas_con_bajas, orient='index').reset_index()
    df_dias_ventas = df_dias_ventas.rename(columns={'index': 'Id'})
    df_dias_ventas = df_dias_ventas.sort_values("Fecha baja")

    # column_mes(df_dias_ventas, "Fecha baja")
    #df_dias_meses = df_dias_ventas.groupby("Mes")["Fecha baja"].count().to_frame("Días")
    #df_dias_meses = df_dias_meses.reset_index()
    #print(df_dias_meses)

    #return sort_by(df_dias_meses)
    return df_dias_ventas

def id_ocupadas(df):
    df_filtrado = df[df["Tags"].notna()]
    ocupadas_tag = set(df_filtrado[df_filtrado['Tags'].str.contains("ocupada")]['Id'])
    ocupadas_desc = set(df[df['Descripción'].str.contains("ocupada")]['Id'])
    ocupadas_posesion = set(df[df['Descripción'].str.contains("posesión")]["Id"])
    ocupadas_id = ocupadas_tag | ocupadas_desc | ocupadas_posesion
    return ocupadas_id


def dataframe_media_ocupadas_2(df):

    def _create_df(mes, df_):
        df_list = list()
        for id_ in ocupadas_id:
            row_list = list()
            row_list.append(id_)
            selection = df_[df_['Id'] == id_]
            if len(selection) == 0:
                continue
            row = selection.iloc[0]
            row_list.append(row['Fecha'])
            row_list.append(mes)
            row_list.append(row['Precio'])
            df_list.append(row_list)

        return pd.DataFrame(df_list, columns=("Id", "Fecha", "Mes", "Precio"))


    ocupadas_id = id_ocupadas(df)
    #df = dataframe_ocupadas(df)
    meses = set(df['Mes'].unique())
    df_list = list()
    for mes in meses:
        row_list = list()
        row_list.append(mes)
        df_mes = _create_df(mes, df[df['Mes'] == mes])
        row_list.append(round(df_mes['Precio'].mean(), 2))
        row_list.append(len(df_mes))
        df_list.append(row_list)
    df_return = pd.DataFrame(df_list, columns=("Mes", "Media precio", "Número anuncios"))
    return sort_by_month(df_return)


# Tipos de inmuebles

def dataframe_tipo_de_inmueble(df_):
    """
    Fnca se considera casa
    Ático se considera piso
    Devuelve coia deld ataframe de entrada con una nueva columna 'Tipo'
    :param df_:
    :return:
    """
    df_ = df_.copy() # Aún con el loc, si no copio primero tengo el error del slice
    df_.loc[:, "Tipo"] = "Sin identificar"

    df_.loc[(df_['Dirección'].str.contains(r"piso|ático", case=False, na=False)), "Tipo"] = "Piso"
    #ids = set(df_[df_['Tipo'] == "Piso"]['Id'].unique())
    ids = set()

    #df_.loc[(df_['Dirección'].str.contains("independiente") | df_['Dirección'].str.contains("casa") | df_['Dirección'].str.contains("finca"))
    #    & ~df_["Id"].isin(ids), "Tipo"] = "Casa"
    df_.loc[(df_['Dirección'].str.contains(r"independiente|casa|finca", case = False, na=False))
            , "Tipo"] = "Casa"

    #ids = ids | set(df_[df_['Tipo'] == "Casa"]['Id'].unique())

    df_.loc[(df_['Dirección'].str.contains(r"pareado|pareada|adosado|adosada", case=False, na=False))
        , "Tipo"] = "Adosado / pareado"
    #& (~df_["Id"].isin(ids))

    return df_


def dataframe_medias_mes_tipo_inmueble(df_):
    df_ = dataframe_tipo_de_inmueble(df_)
    df_ = df_.drop_duplicates(subset=["Id"])
    data_df = list()
    for mes in df_['Mes'].unique():
        row_list = list()
        row_list.append(mes)
        df_mes = df_[df_['Mes'] == mes]
        df_gb_count = df_mes.groupby("Tipo")['Id'].count()
        df_gb_price = df_mes.groupby("Tipo")['Precio'].mean()
        #print(df_gb_count)
        #print(df_gb_price)
        for index in range(0, 4):
            #print(index)
            row_list.append(df_gb_count.iloc[index])
            row_list.append(df_gb_price.iloc[index].round(2))
        data_df.append(row_list)
    return sort_by_month(pd.DataFrame(data_df, columns = ("Mes", "Pisos", "Precio medio pisos", "Casas", "Precio medio casas", "Adosados", "Precio medio adosados", "Sin identificar", "Precio medio sin identificar")))

