import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
from src.utils.loader import cargar_datos_en_session
from src.functions_streamlit.demografia import filtrar_individuos, agrupar_por_decada_y_genero, graficar_barras_dobles

colores = ["#FFB6C1", "#6495ED"]  # rosa claro y celeste pastel

# Configuración de la página
st.set_page_config(
    page_title="Demografía",      # Cambialo según la página
    #page_icon="📊",               # Podés usar emojis distintos en cada página
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CARGA CON SESSION STATE
# -------------------------
cargar_datos_en_session()

df_ind = st.session_state.df_individuos # DataFrame individuos
df_hog = st.session_state.df_hogares # DataFrame hogares
fechas_ind = st.session_state.fechas_individuos # Json individuos
fechas_hog = st.session_state.fechas_hogares # Json hogares

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