import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import FuncFormatter
from src.utils.constants import diccionario_aglomerados


#@st.cache_data
def filtrar_por_fecha(df, año, trimestre, edad_min=0, edad_max=110):
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


def filtrar_por_aglomerado(df, aglo, edad_min=0, edad_max=110):
    """Filtra el dataframe por aglomerado"""

    filtro = (
        (df["AGLOMERADO"] == aglo) &
        (df["CH06"] >=edad_min) &
        (df["CH06"] < edad_max)
    )
    return df[filtro]


def calcular_dependencia_demografica(df):
    """Calcula la dependencia demografica para cada año y trimestre
    Recibe un dataframe filtrado por aglomerado.
    A ese dataframe le agrega una columna calificando por grupo etario
    Luego se agrupo por año, trimestre y grupo etario.
    Se limpian las fechas que no existe
    Calculo dependencia para cada fila y lo agrego como columna
    Return:
        dataframe: ANO4 TRIMESTRE menor activa mayor dependencia
    """
    df = df.copy()

    # Clasificamos por grupo etario (nueva columna)
    df["grupo_etario"] = pd.cut(
        df["CH06"],
        bins=[0, 14, 64, df["CH06"].max()],
        labels=["menor", "activa", "mayor"],
        include_lowest=True
    )

    # Agrupamos por año, trimestre y grupo etario
    # Tener en cuenta que pandas hace todas las combinaciones de año-trim, despues hay que limpiar las que no existen
    # Retorna esta serie ANO4 TRIMESTRE grupo_etario PONDERA
    grupo = df.groupby(["ANO4", "TRIMESTRE", "grupo_etario"])["PONDERA"].sum() 

    # Convertimos los grupos etarios en columnas:  ANO4	 TRIMESTRE	menor	activa	mayor
    grupo = grupo.unstack() 

    # Rellenamos NaN con 0 (si falta algún grupo etario en alguna fecha)
    grupo = grupo.fillna(0)

    # Eliminamos filas donde todas las poblaciones son cero (no hay datos reales)
    grupo = grupo[(grupo[["menor", "activa", "mayor"]].sum(axis=1) > 0)]

    # Eliminamos también donde activa sea 0 para evitar división por cero
    grupo = grupo[grupo["activa"] > 0]

    # Calculamos la dependencia
    grupo["dependencia"] = ((grupo["menor"] + grupo["mayor"]) / grupo["activa"]) * 100

    return grupo.reset_index().sort_values(["ANO4", "TRIMESTRE"], ascending=True)
    

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


def calcular_media_y_mediana_edad(df):
    """
    Calcula media ponderada y mediana de edad por año y trimestre.
    
    Args:
        df (DataFrame): Debe tener columnas 'ANO4', 'TRIMESTRE', 'CH06', 'PONDERA'
        
    Returns:
        DataFrame con columnas: ANO4, TRIMESTRE, media_edad, mediana_edad
    """
    resultados = []

    for (año, trim), grupo in df.groupby(['ANO4', 'TRIMESTRE']):
        if grupo.empty:
            continue

        # Media ponderada
        media = (grupo['CH06'] * grupo['PONDERA']).sum() / grupo['PONDERA'].sum()

        # Mediana simple (sin ponderar)
        mediana = grupo['CH06'].median()

        resultados.append({
            'ANO4': año,
            'TRIMESTRE': trim,
            'media_edad': round(media, 2),
            'mediana_edad': mediana
        })

    return pd.DataFrame(resultados).sort_values(['ANO4', 'TRIMESTRE'])


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


def armar_grafico_dependencia(df, select_aglo):
    """Arma gráfico de líneas a partir de un dataframe"""
    
    # Armo etiqueta con fecha para el gráfico
    df["fecha"] = df["ANO4"].astype(str) + "-T" + df["TRIMESTRE"].astype(str)

    fig, ax = plt.subplots()
    ax.plot(df["fecha"], df["dependencia"], marker='o')
    ax.set_xlabel("Año-Trimestre")
    ax.set_ylabel("Dependencia demográfica")
    ax.set_title(f"Evolución de la dependencia - {diccionario_aglomerados[select_aglo]}")
    ax.grid(True)
    plt.xticks(rotation=45, ha='right', fontsize=6)

    return fig


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
