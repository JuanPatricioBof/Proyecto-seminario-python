# app.py
import streamlit as st
from pathlib import Path
from src.utils.constants import DATA_OUT_PATH, JSON_INDIVIDUOS_PATH
from src.functions_streamlit.educacion import cargar_datos, procesar_niveles_educativos, crear_grafico_barras, cargar_json

# Configuración inicial
st.set_page_config(layout="wide")
st.title("📊 Nivel Educativo de la Población Argentina (EPH)")

# 1. Cargar datos
data_path = DATA_OUT_PATH / "individual_process.csv"
df = cargar_datos(data_path)

# 3. Sidebar con filtros
with st.sidebar:
    st.header("Filtros")
    
    # Cargamos los años disponibles
    años_disponibles = cargar_json(JSON_INDIVIDUOS_PATH)
    
    if not años_disponibles:
        st.warning("No se pudieron cargar los periodos disponibles")
    else:
        # Selector de año
        año_seleccionado = st.selectbox(
            "Seleccione el año",
            options=años_disponibles,
            index=0  # Selecciona el año más reciente por defecto
        )

# 3. Procesamiento de datos
conteo_educativo = procesar_niveles_educativos(df, año_seleccionado)

# 4. Visualización
st.subheader("Distribución Educativa Detallada")
fig = crear_grafico_barras(conteo_educativo, año_seleccionado)
st.plotly_chart(fig, use_container_width=True)
