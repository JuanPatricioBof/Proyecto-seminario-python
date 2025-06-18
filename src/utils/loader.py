import streamlit as st
import pandas as pd
import json
import os
from src.utils.constants import DATA_OUT_PATH, PATHS

# -------------------------
# FUNCIONES CON CACHE
# -------------------------

@st.cache_data
def cargar_parcial_csv(path, usecols=None, filtro=None):
    """Lee un archivo CSV y lo retorna como DataFrame de pandas parcial.

    Args:
        path (str or Path): Ruta al archivo CSV
        usecols (list), optional): Columnas a guardar. Defaults to None.
        filtro (list(tuples), optional): Años y trimestres a filtrar. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.    
    """
    if not os.path.exists(path):
        st.warning(f"⚠️ El archivo {path} no existe.")
        return pd.DataFrame() # Vacío
    
    df = pd.read_csv(path, sep=";", decimal=",", low_memory=False, usecols=usecols)
    
    if filtro:
        df = df[df[["año", "trimestre"]].apply(tuple, axis=1).isin(filtro)]
    # Explicación de como funciona
    # df[["año", "trimestre"]] #Devuelve un DataFrame con solo esas 2 columnas.
    # .apply(tuple, axis=1) Convierte cada fila en una tupla.
    # .isin(filtros) Devuelve una serie booleana que dice si cada tupla está o no en la lista de filtros: [True, False, True, False]
    # df[ ... ] Aplica ese filtro y se queda solo con las filas True.

    return df


@st.cache_data
def cargar_json(path):
    """
    Lee un archivo json y lo retorna como un diccionario con los datos convertidos a int.
    Args:
        path (str or Path): Ruta al archivo json.
    Returns:
        diccionario: los años y trimestres del tipo int.
    """

    with open(path, 'r') as f:
        fechas = json.load(f)
    return {int(k): [int(tri) for tri in v] for k, v in fechas.items()}


# def file_exists(path):
#     """Verifica que el archivo exista

#     Args:
#         path (path or str): ruta al archivo

#     Returns:
#         boolean: True si existe, false si no.
#     """    
#     return os.path.exists(path)


# def cargar_datos_en_session():
#     """Carga en session_state los dataframes y diccionario de fechas"""

#     # Cargo DataFrames
#     if "df_individuos" not in st.session_state:
#         st.session_state.df_individuos = cargar_csv(PATHS["individual"]["csv"])
#     if "df_hogares" not in st.session_state:
#         st.session_state.df_hogares = cargar_csv(PATHS["hogar"]["csv"])
    
#     # Cargo Json de fechas disponibles
#     if "fechas_individuos" not in st.session_state:
#         st.session_state.fechas_individuos = cargar_json(PATHS["individual"]["json"])
#     if "fechas_hogares" not in st.session_state:
#         st.session_state.fechas_hogares = cargar_json(PATHS["hogar"]["json"])
