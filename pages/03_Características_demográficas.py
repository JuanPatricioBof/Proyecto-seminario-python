import sys
sys.path.append("..") # Acceso a src
import streamlit as st
from src.utils.loader import cargar_parcial_csv, cargar_json
from src.functions_streamlit.demografia import filtrar_individuos, agrupar_por_decada_y_genero, graficar_barras_dobles, obtener_ultima_fecha, agrupar_por_aglomerado, convertir_a_dataframe_formateado
from src.utils.constants import PATHS


# --- Configuración de la página ---
st.set_page_config(
    page_title="Demografía",      # Cambialo según la página
    #page_icon="📊",               # Podés usar emojis distintos en cada página
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CARGA DE DATOS
# -------------------------

# CH06 = edad(int); CH04_str = sexo(str); AGLOMERADO = codigo de aglomerado(int); PONDERA = cant personas (int)
columnas_necesarias = ['ANO4','TRIMESTRE','PONDERA','CH06','CH04_str','AGLOMERADO']
df_ind = cargar_parcial_csv(PATHS["individual"]["csv"], columnas_necesarias)

if df_ind.empty:
    st.warning("No hay datos disponibles.")
    st.stop()

fechas_ind = cargar_json(PATHS["individual"]["json"]) # Fechas disponibles

# -------------------------
# INTERFAZ DE USUARIO
# -------------------------

st.subheader("Exploración de la población según edad y sexo.")

col1, col2 = st.columns(2)
with col1:
    año_selec = st.selectbox("Seleccioná un año", fechas_ind.keys())#     # Eligir año de las opciones disponibles
with col2:
    trim_selec = st.selectbox("Seleccioná un trimestre", fechas_ind[año_selec]) # Eligir trimestre disponible de ese año

df_por_fecha = filtrar_individuos(df_ind, año_selec, trim_selec)

# if df_por_fecha.empty:
#     st.warning("No hay datos para el año y trimestre seleccionados.")
#     st.stop()

poblacion_por_decada_genero = agrupar_por_decada_y_genero(df_por_fecha)

# if poblacion_por_decada_genero.empty:
#     st.warning("No se pudo calcular la población por década y género.")
#     st.stop()

fig = graficar_barras_dobles(poblacion_por_decada_genero, año_selec, trim_selec, colores= ["#FFB6C1", "#6495ED"] )
st.pyplot(fig)


st.divider()


ultima_fecha = obtener_ultima_fecha(fechas_ind)

df_ultima_fecha = filtrar_individuos(df_ind, ultima_fecha[0], ultima_fecha[1])

promedios = agrupar_por_aglomerado(df_ultima_fecha)

# if promedios.empty:
#     st.warning("No se pudo calcular el promedio por aglomerado.")
#     st.stop()

df_promedios = convertir_a_dataframe_formateado(promedios)

st.subheader("Promedio de edades por aglomerados.")

st.markdown(f'Se muestra información de la EPH mas reciente AÑO {ultima_fecha[0]} T{ultima_fecha[1]}')


# ----opcion para deslizar-----
st.dataframe(df_promedios.reset_index(drop=True))
# ---- opcion estatica------
#st.table(df_promedios.set_index("Aglomerado")) # muestra tabla sin indice
