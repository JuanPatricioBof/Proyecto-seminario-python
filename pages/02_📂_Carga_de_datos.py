import streamlit as st
import os
import sys
from pathlib import Path
from src.utils.constants import SRC_PATH
# Asegurar acceso al módulo src
sys.path.append(str(SRC_PATH))


# Importar la función y las constantes

import dataset.generate_dataset as join
from function_streamlit import function_p2  
from utils.constants import DATA_OUT_PATH, DATA_PATH

st.title("📁 Carga de datos")

# Mostrar información sobre los periodos disponibles
resultado = function_p2.obtener_periodos()
if resultado:
    primero, ultimo = resultado
    st.markdown(f"✅ El sistema contiene información desde el **0{primero[1]}/{primero[0]}** hasta el **0{ultimo[1]}/{ultimo[0]}**.")
else:
    st.warning("⚠️ No se encontraron archivos en la carpeta `data_eph`.")

# Botón para forzar la actualización del dataset
if st.button("🔄 Forzar actualización del dataset"):
    with st.spinner("Actualizando datasets..."):
        # Llamada a la función para generar los archivos CSV
        join.join_data("hogar")
        join.join_data("individual")
    st.success("✅ Dataset actualizado correctamente.")
