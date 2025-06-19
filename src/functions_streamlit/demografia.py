import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from matplotlib.ticker import FuncFormatter
from src.utils.constants import diccionario_aglomerados


#@st.cache_data
def filtrar_individuos(df, año, trimestre, edad_min=0, edad_max=110):
    """Filtra el dataframe por año,trimestre, y se asegura que la edad sea valida

    Args:
        df (dataframe): datos a filtrar
        año (int): año elegido
        trimestre (int): trimestre elegido
        edad_min (int, optional): _description_. Defaults to 0.
        edad_max (int, optional): _description_. Defaults to 110.

    Returns:
        dataframe: ya filtrado con las filas de interes
    """    
    filtro = (
        (df["ANO4"] == año) &
        (df["TRIMESTRE"] == trimestre) &
        (df["CH06"] >= edad_min) &
        (df["CH06"] < edad_max)
    )
    return df[filtro]


#@st.cache_data
def obtener_ultima_fecha(fechas):
    """Obtiene el año y trimestre mas reciente.

    Args:
        fechas (dicc): dicc de listas de trimestres

    Returns:
        tuple: (año, trim) del tipo int
    """    
    max_anio = max(fechas.keys())
    max_trim = max(fechas[max_anio])

    return (max_anio,max_trim)


#@st.cache_data
def agrupar_por_decada_y_genero(df):
    """Agrupa por década y genero. Genera este dataframe
    Retorna un DataFrame donde las filas son las décadas y las columnas son los géneros:
       CH06	    Femenino	Masculino
       0	    12345	    11340
       10	    15023	    14876
       20	    16789	    16112
    Args:
        df (dataframe): dataframe filtrado

    Returns:
        dataframe: [edad agrupada por decada, cantFemenino, cantMasculino]
    """    
    agrupado = (
        df
        .groupby([
            (df["CH06"] // 10 * 10),   # Década
            df["CH04_str"]            # Género
        ])["PONDERA"]
        .sum()
        .unstack(fill_value=0) # Cada género en una columna
    )
    return agrupado


#@st.cache_data
def agrupar_por_aglomerado(df):
    """Agrupa por código de aglomerado y calcula el promedio
    
    Edad promedio ponderada por aglomerado = 
        
        ∑(edad x pondera)
    = ----------------------- = (  g["CH06"] * g["PONDERA"]).sum() / g["PONDERA"].sum()  )
            ∑ pondera 

    Args:
        df (dataframe): Dataframe filtrado con la fecha mas reciente.
    Returns:
        promedios (Serie de pandas): indice = cod. de aglo y valor = promedio de edades
    """    
    promedios = df.groupby("AGLOMERADO").apply(
        lambda g: (g["CH06"] * g["PONDERA"]).sum() / g["PONDERA"].sum()
    )
    return promedios


def convertir_a_dataframe_formateado(promedios):
    """Convierte la serie a dataframe para poder mostrarlo en una tabla o grafico.
    Y también lo formatea.

        -Reemplaza el codigo de aglomerado por el nombre.
        -Convierte el promedio de edades a enteros.
        -Ordena el dataframe por nombre de aglomerado

    Args:
        promedios (serie): el indice es el codigo de aglo, el valor es el promedio

    Returns:
        dataframe: _description_
    """    
    # Convertir a DataFrame para poder graficar
    promedios_df = promedios.reset_index(name="Edad Promedio")

    # Convertir códigos a string para mapear bien
    promedios_df["AGLOMERADO"] = promedios_df["AGLOMERADO"].astype(str).str.zfill(2)
    # Mapear los nombres
    promedios_df["Aglomerado"] = promedios_df["AGLOMERADO"].map(diccionario_aglomerados)

    # Redondeamos la edad promedio a enteros
    promedios_df["Edad Promedio"] = promedios_df["Edad Promedio"].round(0).astype(int)

    # Ordenar columnas y ordenar por nombre de aglomerado
    promedios_df = promedios_df[["Aglomerado", "Edad Promedio"]].sort_values("Aglomerado", ascending=True)
    
    return promedios_df

def formato_miles(x, _):
    """
    Formatea los números del eje Y:
    """
    if x >= 1_000_000:
        return f'{x / 1_000_000:.1f}M'
    elif x >= 1_000:
        return f'{x / 1_000:.0f}K'
    else:
        return str(int(x))


@st.cache_data
def graficar_barras_dobles(df, año, trimestre, colores=None):
    """
    Grafica un gráfico de barras con dos columnas (por ejemplo: Femenino y Masculino)
    agrupadas por décadas (filas del DataFrame).
    
    Parámetros:
    - df: DataFrame con el índice como edad mínima de cada década (ej: 0, 10, 20) y columnas de sexo.
    - año: Año del relevamiento (para el título).
    - trimestre: Trimestre del relevamiento.
    - colores: Lista de colores personalizada para las columnas.
    """
    #    CH06	    Femenino	Masculino
    #    0	    12345	    11340
    #    10	    15023	    14876
    #    20	    16789	    16112

    # Crear figura y ejes con fondo oscuro
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0e1117')
    ax.set_facecolor('#0e1117')

    # Configurar colores de los ejes y títulos
    ax.tick_params(colors='white')      # Color de los ticks
    ax.xaxis.label.set_color('white')   # Etiqueta eje X
    ax.yaxis.label.set_color('white')   # Etiqueta eje Y
    ax.title.set_color('white')         # Título
    
    # Dibujar gráfico de barras con pandas sobre el eje `ax`
    df.plot(kind='bar', ax=ax, color=colores) #es un método de pandas que genera un gráfico de barras utilizando Matplotlib dentro de un eje (ax) personalizado.

    # Título y etiquetas de los ejes
    ax.set_title(f'Distribución por edad y sexo Año {año} T{trimestre}')
    ax.set_xlabel('Década de edad')
    ax.set_ylabel('Población ponderada')
    ax.legend(title=None, facecolor='#0e1117', edgecolor='white', labelcolor='white')

    # Aplicar el formato de miles (K, M) al eje Y
    ax.yaxis.set_major_formatter(FuncFormatter(formato_miles))

    # Ajustar altura máxima del eje Y
    ax.set_ylim(0, df.max().max() * 1.15)

    # Generar etiquetas como "0-9", "10-19", etc.
    etiquetas_x = [f"{int(edad)}-{int(edad)+9}" for edad in df.index]
    ax.set_xticklabels(etiquetas_x, rotation=0, color='white')

    # Mostrar valores numéricos sobre cada barra
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', fontsize=8, label_type='edge', padding=2, rotation=90, color='white')

    return fig
