import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
from src.utils.loader import cargar_parcial_csv, cargar_json
from src.functions_streamlit.demografia import filtrar_individuos, agrupar_por_decada_y_genero, graficar_barras_dobles
from src.utils.constants import DATA_OUT_PATH, PATHS

colores = ["#FFB6C1", "#6495ED"]  # rosa claro y celeste pastel

# Configuración de la página
st.set_page_config(
    page_title="Demografía",      # Cambialo según la página
    #page_icon="📊",               # Podés usar emojis distintos en cada página
    layout="wide",
    initial_sidebar_state="expanded"
)

# AGREGAR para que solo cargue si los archivos existen
#if st.session_state.datos_cargados:

df_ind = cargar_parcial_csv(PATHS["individual"]["csv"], ['PONDERA','ANO4','TRIMESTRE','CH06']) # DataFrame individuos
df_hog = cargar_parcial_csv(PATHS["hogar"]["csv"], ['PONDERA','ANO4','TRIMESTRE']) # DataFrame hogares
fechas_ind = cargar_json(PATHS["individual"]["json"]) # Json individuos
fechas_hog = cargar_json(PATHS["hogar"]["json"]) # Json hogares

# -------------------------
# INTERFAZ DE USUARIO
# -------------------------

st.title("📊Características demográficas.")

#st.subheader("1.3.1 Exploración de la población según **edad y sexo** por año y trimestre.")
with st.expander("1.3.1 Exploración de la población según **edad y sexo** por año y trimestre."):

    col1, col2 = st.columns(2)
    with col1:
        año_selec = st.selectbox("Seleccioná un año", fechas_ind.keys())#     # Eligir año de las opciones disponibles

    with col2:
        trim_selec = st.selectbox("Seleccioná un trimestre", fechas_ind[año_selec]) # Eligir trimestre disponible de ese año

    df_filtrado = filtrar_individuos(df_ind, año_selec, trim_selec)
    agrupado = agrupar_por_decada_y_genero(df_filtrado)

    fig = graficar_barras_dobles(agrupado, año_selec, trim_selec, colores=["#FF69B4", "#1E90FF"])
    st.pyplot(fig)

with st.expander("1.3.2 Informar..."):
    st.write("Proximamente...")