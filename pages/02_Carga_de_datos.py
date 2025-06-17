import streamlit as st
import sys
sys.path.append("..") # Acceso a src

# Importar la función y las constantes
from src.dataset.generar_dataset import join_data
from src.functions_streamlit.carga import obtener_periodos, verificar_correspondencia
from src.utils.constants import DATA_OUT_PATH, DATA_PATH, PATHS
from src.utils.loader import cargar_datos_en_session

st.title("📁 Carga de datos")
if not PATHS["hogar"]["json"].exists() or not PATHS["individual"]["json"].exists():
    st.markdown("Los EPH no estas procesados, por favor presione este boton")
    if st.button("Procesar los EPH"):
        with st.spinner("Procesando datasets..."):
            # Llamada a la función para generar los archivos CSV
             join_data()
             st.success("✅ Dataset procesados correctamente.")
             st.rerun()
    st.stop()
             
cargar_datos_en_session()
#Se verifica si todos los archivos de individuos esten en hogares y viceversa 
lista_archivos_faltantes=verificar_correspondencia(PATHS["hogar"]["json"], PATHS["individual"]["json"])
if lista_archivos_faltantes:
    st.error("Archivos faltantes:")
    for archivo_faltante in lista_archivos_faltantes:
        st.write(f"- {archivo_faltante}")
else:
    st.success("CHEQUEO EXITOSO")
    st.write("No se encontraron inconsistencias entre los archivos")
    
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
         cargar_datos_en_session()
         st.info("Datos actualizados y cargados en la sesión.")
