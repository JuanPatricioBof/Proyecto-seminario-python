import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
import json

from src.utils.constants import DATA_OUT_PATH
from src.functions_streamlit.demografia import filtrar_individuos, agrupar_por_decada_y_genero, graficar_barras_dobles

path_csv = {'hogar': DATA_OUT_PATH / "hogar_process.csv", 'individual': DATA_OUT_PATH / "individual_process.csv"}
path_json = {'hogar':DATA_OUT_PATH / "estructura_hogares.json", 'individual': DATA_OUT_PATH / "estructura_individuos.json"}

colores = ["#FFB6C1", "#6495ED"]  # rosa claro y celeste pastel

st.set_page_config(page_title="Características demográficas", layout="wide")

# -------------------------
# FUNCIONES CON CACHE
# -------------------------

@st.cache_data
def cargar_datos(path):
    """Lée el csv y lo retorna como un DataFrame"""
    return pd.read_csv(path, sep=";", decimal=",", low_memory=False)


@st.cache_data
def cargar_fechas(path):
    """Lée el json que contiene los años y trimestres disponibles y lo retorna.
      Los años y trimestres son strings """
    with open(path, 'r') as f:
        fechas = json.load(f)
    # Convertimos claves e indices a enteros 
    return {int(k): [int(tri)for tri in v ] for k, v in fechas.items()}

# -------------------------
# CARGA CON SESSION STATE
# -------------------------

# Cargo DataFrames 
if "df_individuos" not in st.session_state:
    st.session_state.df_individuos = cargar_datos(path_csv["individual"])

if "df_hogares" not in st.session_state:
    st.session_state.df_hogares = cargar_datos(path_csv["hogar"])

df_ind = st.session_state.df_individuos
df_hog = st.session_state.df_hogares

# Cargo Json de fechas disponibles
if "fechas_individuos" not in st.session_state:
    st.session_state.fechas_individuos = cargar_fechas(path_json["individual"])

if "fechas_hogares" not in st.session_state:
    st.session_state.fechas_hogares = cargar_fechas(path_json["hogar"])

fechas_disponibles_ind = st.session_state.fechas_individuos
fechas_disponibles_hog = st.session_state.fechas_hogares

# -------------------------
# INTERFAZ DE USUARIO
# -------------------------

st.title("📊Características demográficas.")

#st.subheader("1.3.1 Exploración de la población según **edad y sexo** por año y trimestre.")
with st.expander("1.3.1 Exploración de la población según **edad y sexo** por año y trimestre."):
    col1, col2 = st.columns(2)
    with col1:
        año_selec = st.selectbox("Seleccioná un año", fechas_disponibles_ind.keys())#     # Eligir año de las opciones disponibles

    with col2:
        trim_selec = st.selectbox("Seleccioná un trimestre", fechas_disponibles_ind[año_selec]) # Eligir trimestre disponible de ese año

    df_filtrado = filtrar_individuos(df_ind, año_selec, trim_selec)
    agrupado = agrupar_por_decada_y_genero(df_filtrado)

    fig = graficar_barras_dobles(agrupado, año_selec, trim_selec, colores=["#FF69B4", "#1E90FF"])
    st.pyplot(fig)

with st.expander("1.3.2 Informar..."):
    st.write("Proximamente...")