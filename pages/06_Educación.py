# app.py
import streamlit as st
from src.utils.constants import DATA_OUT_PATH, PATHS
from src.functions_streamlit.educacion import  procesar_niveles_educativos, crear_grafico_barras
from src.utils.loader import cargar_parcial_csv, cargar_json

# Configuración inicial
st.set_page_config(layout="wide")
st.title("📊 Nivel Educativo de la Población Argentina (EPH)")

#  Cargar datos
# Acceder a los DataFrames
df_ind = cargar_parcial_csv(PATHS["individual"]["csv"], ['PONDERA','ANO4','NIVEL_ED']) # DataFrame individuos

fechas_ind = cargar_json(PATHS["individual"]["json"]) # Json individuos
 

#  Sidebar con filtros
with st.sidebar:
    st.header("Filtros")
    
    # Cargamos los años disponibles
    años_disponibles = fechas_ind
    
    if not años_disponibles:
        st.warning("No se pudieron cargar los periodos disponibles")
    else:
        # Selector de año
        año_seleccionado = st.selectbox(
            "Seleccione el año",
            options=años_disponibles,
            index=0  # Selecciona el año más reciente por defecto
        )

#  Procesamiento de datos
conteo_educativo = procesar_niveles_educativos(df_ind, año_seleccionado)

#  Visualización
st.subheader("Distribución Educativa Detallada")
fig = crear_grafico_barras(conteo_educativo, año_seleccionado)
st.plotly_chart(fig, use_container_width=True)
