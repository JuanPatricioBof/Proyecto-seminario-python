"""Pagina 05. Funciones para empleo y actividad"""
import pandas as pd
import json
import streamlit as st


def format_number(x):
    if isinstance(x, (int, float)):
        return f"{x:,.0f}".replace(",", ".") if x == int(x) else f"{x:,.1f}".replace(",", ".")
    return x

def evolucion_desempleo(df, aglomerado=None):
    """
    Calcula la evolución de la tasa de desempleo por período (año + trimestre), con opción de filtrar por aglomerado.
    Args:
        df (pd.DataFrame): DataFrame con datos individuales, incluyendo las columnas 'CONDICION_LABORAL', 
                           'PONDERA', 'ANO4', 'TRIMESTRE' y 'AGLOMERADO'.
        aglomerado (str, optional): Código del aglomerado. Si no se especifica, se calcula para todo el país.
    Returns:
        dict: Diccionario con las tasas de desempleo por período (clave = 'YYYYTn', valor = tasa en float).
    """
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)

    if aglomerado:
        df = df[df['AGLOMERADO'] == aglomerado]

    # Filtramos solo ocupados y desocupados
    df = df[df['CONDICION_LABORAL'].isin(['Ocupado dependiente', 'Ocupado autónomo', 'Desocupado'])]

    # Creamos columna para el período
    df['PERIODO'] = df['ANO4'].astype(str) + 'T' + df['TRIMESTRE'].astype(str)

    # Clasificamos ocupados/desocupados
    df['ESTADO'] = df['CONDICION_LABORAL'].apply(lambda x: 'ocupado' if 'Ocupado' in x else 'desocupado')

    # Agrupamos por PERIODO y ESTADO, y sumamos ponderaciones
    resumen = df.groupby(['PERIODO', 'ESTADO'])['PONDERA'].sum().unstack(fill_value=0)

    # Calculamos la tasa de desempleo
    resumen['tasa_desempleo'] = (resumen['desocupado'] / (resumen['ocupado'] + resumen['desocupado'])) * 100

    return resumen['tasa_desempleo'].round(2).sort_index().to_dict()


def evolucion_empleo(df, aglomerado=None):
    """
    Calcula la evolución de la tasa de empleo por período, con opción de filtrar por aglomerado.
    Args:
        df (pd.DataFrame): DataFrame con datos individuales, incluyendo las columnas 'CONDICION_LABORAL', 
                           'PONDERA', 'ANO4', 'TRIMESTRE' y 'AGLOMERADO'.
        aglomerado (str, optional): Código del aglomerado. Si no se especifica, se calcula para todo el país.
    Returns:
        dict: Diccionario con las tasas de empleo por período (clave = 'YYYYTn', valor = tasa en float).
    """
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)

    if aglomerado:
        df = df[df['AGLOMERADO'] == aglomerado]

    # Filtramos solo ocupados y desocupados
    df = df[df['CONDICION_LABORAL'].isin(['Ocupado dependiente', 'Ocupado autónomo', 'Desocupado'])]

    # Creamos columna para el período
    df['PERIODO'] = df['ANO4'].astype(str) + 'T' + df['TRIMESTRE'].astype(str)

    # Clasificamos ocupados/desocupados
    df['ESTADO'] = df['CONDICION_LABORAL'].apply(lambda x: 'ocupado' if 'Ocupado' in x else 'desocupado')

    # Agrupamos por PERIODO y ESTADO, y sumamos ponderaciones
    resumen = df.groupby(['PERIODO', 'ESTADO'])['PONDERA'].sum().unstack(fill_value=0)

    # Calculamos la tasa de empleo
    resumen['tasa_empleo'] = (resumen['ocupado'] / (resumen['ocupado'] + resumen['desocupado'])) * 100

    return resumen['tasa_empleo'].round(2).sort_index().to_dict()

def obtener_estadisticas_empleo(df, codigo_aglomerado):
    """Obtiene estadísticas de empleo para un aglomerado específico y devuelve el porcentaje de ocupados, etiquetas y tamaños para un gráfico de torta"""
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)
    df['CONDICION_LABORAL'] = df['CONDICION_LABORAL'].str.strip()

    # Filtra el DataFrame para el aglomerado seleccionado
    df_aglo = df[df['AGLOMERADO'] == codigo_aglomerado]

    if df_aglo.empty or 'PONDERA' not in df_aglo.columns:
        return 0, [], []

    total_personas = df_aglo['PONDERA'].sum()

    # Filtra solo los ocupados
    ocupados_validos = ['Ocupado autónomo', 'Ocupado dependiente']
    df_ocupados = df_aglo[df_aglo['CONDICION_LABORAL'].isin(ocupados_validos)].copy()

    total_ocupados = df_ocupados['PONDERA'].sum()

    if total_ocupados == 0 or total_personas == 0:
        return 0, [], []

    # Calcula el porcentaje de ocupados sobre el total de personas
    porcentaje_ocupados = round((total_ocupados / total_personas) * 100, 1)

    # Mapea los tipos de empleo para el gráfico de torta
    mapeo = {1: 'Estatal', 2: 'Privado', 3: 'Otro'}
    df_ocupados['TIPO_EMPLEO'] = df_ocupados['PP04A'].map(mapeo)

    conteo = df_ocupados.groupby('TIPO_EMPLEO')['PONDERA'].sum()

    labels = conteo.index.tolist()
    sizes = [round((v / total_ocupados) * 100, 1) for v in conteo.values]

    return porcentaje_ocupados, labels, sizes

def calcular_tasas(df, fechas_disponibles):
    """
    Calcula la tasa de empleo y desempleo para todos los aglomerados,
    comparando el primer y último período disponible.
    """
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)

    # Busca el año y trimestre más antiguo y más reciente disponible
    anio_min = min(fechas_disponibles.keys())
    trimestre_min = min(fechas_disponibles[anio_min])
    anio_max = max(fechas_disponibles.keys())
    trimestre_max = max(fechas_disponibles[anio_max])

    tasas = {}

    for aglo in df['AGLOMERADO'].unique():
        tasas[aglo] = {}

        for periodo, anio, trimestre in [('antiguo', anio_min, trimestre_min), ('actual', anio_max, trimestre_max)]:
            # Filtra por aglomerado, año y trimestre
            df_periodo = df[
                (df['AGLOMERADO'] == aglo) &
                (df['ANO4'] == anio) &
                (df['TRIMESTRE'] == trimestre)
            ]

            # Suma pondera de ocupados y desocupados
            ocupados = df_periodo[df_periodo['CONDICION_LABORAL'].isin(['Ocupado autónomo', 'Ocupado dependiente'])]['PONDERA'].sum()
            desocupados = df_periodo[df_periodo['CONDICION_LABORAL'] == 'Desocupado']['PONDERA'].sum()

            total = ocupados + desocupados

            if total == 0:
                tasa_empleo = 0
                tasa_desempleo = 0
            else:
                # Calcula tasas  sobre el total  (ocupados + desocupados)
                tasa_empleo = round((ocupados / total) * 100, 1)
                tasa_desempleo = round((desocupados / total) * 100, 1)

            tasas[aglo][periodo] = {'empleo': tasa_empleo, 'desempleo': tasa_desempleo}

    return tasas
