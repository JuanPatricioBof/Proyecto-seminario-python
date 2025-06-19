import streamlit as st
import sys
sys.path.append("..") # Acceso a src

# Importar la función y las constantes
from src.dataset.generar_dataset import join_data
from src.functions_streamlit.carga import obtener_periodos, verificar_correspondencia
from src.utils.constants import DATA_OUT_PATH, DATA_PATH, PATHS
from src.dataset.agregar_columnas import generar_columnas_csv_individual,generar_columnas_csv_hogar
from src.utils.loader import cargar_fechas_correspondencia_en_session

st.title("📁 Carga de datos")  # Título principal de la página

## ----------------------------
## SECCIÓN 1: VERIFICACIÓN INICIAL DE ARCHIVOS
## ----------------------------

# Comprobar si los archivos JSON base existen
if not PATHS["hogar"]["json"].exists() or not PATHS["individual"]["json"].exists():
    st.markdown("Los EPH no están procesados, por favor presione este botón")
    
    # Botón para iniciar el procesamiento
    if st.button("Procesar los EPH"):
        with st.spinner("Procesando datasets..."):
            # Procesamiento inicial de datos
            join_data()  # Función principal de unión de datos
            
            # Generar archivos CSV si no existen
            if not PATHS["hogar"]["csv"].exists():
                generar_columnas_csv_hogar()
            if not PATHS["individual"]["csv"].exists():
                generar_columnas_csv_individual()
            
            st.success("✅ Datasets procesados correctamente.")
            st.rerun()  # Recargar la página para reflejar cambios
    
    st.stop()  # Detener ejecución si no hay archivos base

## ----------------------------
## SECCIÓN 2: CARGA DE PERIODOS DISPONIBLES
## ----------------------------

# Carga inicial de periodos disponibles (con spinner visual)
with st.spinner("Cargando periodos disponibles..."):
    cargar_fechas_correspondencia_en_session()  # Carga en session_state

## ----------------------------
## SECCIÓN 3: VERIFICACIÓN DE CORRESPONDENCIA
## ----------------------------

# Comprobar consistencia entre archivos de hogares e individuos
lista_tupla_tipo_archivos_faltantes = verificar_correspondencia(
    PATHS["hogar"]["json"], 
    PATHS["individual"]["json"]
)

if lista_tupla_tipo_archivos_faltantes:
    # Mostrar errores si hay inconsistencias
    st.error("Archivos faltantes:")
    for año, trimestre, tipo in lista_tupla_tipo_archivos_faltantes:
        st.markdown(f"• Falta en {tipo}: Año {año}, Trimestre {trimestre}")
else:
    # Mensaje de éxito si todo está completo
    st.success("✓ Chequeo de correspondencia exitoso")
    st.write("No se encontraron inconsistencias entre los archivos")

## ----------------------------
## SECCIÓN 4: INFORMACIÓN DE PERIODOS
## ----------------------------

# Obtener y mostrar el rango temporal disponible
resultado = obtener_periodos()
if resultado:
    primero, ultimo = resultado
    st.markdown(
        f"**Rango temporal disponible:**\n\n"
        f"• **Primer periodo:** 0{primero[1]}/{primero[0]}\n"
        f"• **Último periodo:** 0{ultimo[1]}/{ultimo[0]}"
    )
else:
    st.warning("⚠️ No se encontraron archivos en la carpeta `data_eph`.")

## ----------------------------
## SECCIÓN 5: ACTUALIZACIÓN MANUAL
## ----------------------------

# Botón para forzar actualización completa
if st.button("🔄 Forzar actualización del dataset"):
    with st.spinner("Actualizando datasets..."):
        # Reprocesar todos los datos
        join_data()
        
        # Limpiar caché de fechas si existe
        if 'fechas_correspondencia' in st.session_state:
            del st.session_state.fechas_correspondencia
        cargar_fechas_correspondencia_en_session(forzar_actualizacion=True)
        st.success("✅ Dataset actualizado correctamente.")


