import streamlit as st
import sys
sys.path.append("..") # Acceso a src

# Importar la función y las constantes
from src.dataset.generar_dataset import join_data
from src.functions_streamlit.carga import obtener_periodos
from src.utils.constants import DATA_OUT_PATH, DATA_PATH

st.title("📁 Carga de datos")

# Mostrar información sobre los periodos disponibles
resultado = obtener_periodos()
if resultado:
    primero, ultimo = resultado
    st.markdown(f"✅ El sistema contiene información desde el **0{primero[1]}/{primero[0]}** hasta el **0{ultimo[1]}/{ultimo[0]}**.")
else:
    st.warning("⚠️ No se encontraron archivos en la carpeta `data_eph`.")

# Botón para forzar la actualización del dataset
if st.button("🔄 Forzar actualización del dataset"):
    with st.spinner("Actualizando datasets..."):
        # Llamada a la función para generar los archivos CSV
        join_data()
    st.success("✅ Dataset actualizado correctamente.")
