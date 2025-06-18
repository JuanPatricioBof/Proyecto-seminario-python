import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
from src.utils.loader import cargar_parcial_csv, cargar_json, file_exists
from src.functions_streamlit.demografia import filtrar_individuos, agrupar_por_decada_y_genero, graficar_barras_dobles
from src.utils.constants import PATHS

# --- Configuración de la página ---
st.set_page_config(
    page_title="Demografía",      # Cambialo según la página
    #page_icon="📊",               # Podés usar emojis distintos en cada página
    layout="wide",
    initial_sidebar_state="expanded"
)
# CASO PARA UNA SOLA ENCUESTA
# --- Carga segura ---

columnas_necesarias = ['ANO4','TRIMESTRE','PONDERA','CH06','CH04_str']
df_ind = cargar_parcial_csv(PATHS["individual"]["csv"], columnas_necesarias)

if df_ind.empty:
    st.warning("No hay datos disponibles.")
    st.stop()

fechas_ind = cargar_json(PATHS["individual"]["json"])

# CASO PARA DOS ENCUESTAS

# puede estar vacio o con datos, o talvez preguntar si existe la key y en caso que no, fechas=none
fechas = st.session_state.fechas_correspondencia 

columnas_necesarias = ['ANO4','TRIMESTRE','PONDERA','CH06','CH04_str']
df_ind = cargar_parcial_csv(PATHS["individual"]["csv"], columnas_necesarias, fechas)

columnas_necesarias = ['ANO4','TRIMESTRE','PONDERA']
df_hog = cargar_parcial_csv(PATHS["hogar"]["csv"], columnas_necesarias, fechas)

# DataFrames vacios
if df_ind.empty or df_hog.empty:
    st.warning("No hay datos disponibles.")
    st.stop()

# -------------------------
# INTERFAZ DE USUARIO
# -------------------------

st.subheader("1.3.1 Exploración de la población según **edad y sexo** por año y trimestre.")

col1, col2 = st.columns(2)
with col1:
    año_selec = st.selectbox("Seleccioná un año", fechas_ind.keys())#     # Eligir año de las opciones disponibles
with col2:
    trim_selec = st.selectbox("Seleccioná un trimestre", fechas_ind[año_selec]) # Eligir trimestre disponible de ese año
    
df_filtrado = filtrar_individuos(df_ind, año_selec, trim_selec)
agrupado = agrupar_por_decada_y_genero(df_filtrado)

# with st.sidebar:
#     st.header("🎛️ Filtros")
#     año_selec = st.selectbox("Seleccioná un año", fechas_ind.keys())
#     trim_selec = st.selectbox("Seleccioná un trimestre", fechas_ind[año_selec])
#     df_filtrado = filtrar_individuos(df_ind, año_selec, trim_selec)
#     agrupado = agrupar_por_decada_y_genero(df_filtrado)

fig = graficar_barras_dobles(agrupado, año_selec, trim_selec, colores= ["#FFB6C1", "#6495ED"] )
st.pyplot(fig)

st.divider()

# --- Gráfico de distribución por sexo ---
st.subheader("Otro punto")
