import sys
sys.path.append("..")
import streamlit as st
from src.utils.loader import cargar_parcial_csv, cargar_json
from src.functions_streamlit.demografia import filtrar_por_fecha, agrupar_por_decada_y_genero, graficar_barras_dobles, obtener_ultima_fecha, agrupar_por_aglomerado, convertir_a_dataframe_formateado, filtrar_por_aglomerado, calcular_dependencia_demografica, armar_grafico_dependencia, calcular_media_y_mediana_edad
from src.utils.constants import PATHS, diccionario_aglomerados


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
    año_selec = st.selectbox("Seleccioná un año", fechas_ind.keys())
with col2:
    trim_selec = st.selectbox("Seleccioná un trimestre", fechas_ind[año_selec])

df_por_fecha = filtrar_por_fecha(df_ind, año_selec, trim_selec)

poblacion_por_decada_genero = agrupar_por_decada_y_genero(df_por_fecha)

fig = graficar_barras_dobles(poblacion_por_decada_genero, año_selec, trim_selec, colores= ["#FFB6C1", "#6495ED"] )
st.pyplot(fig)


st.divider()


año_reciente, trim_reciente = obtener_ultima_fecha(fechas_ind)

df_ultima_fecha = filtrar_por_fecha(df_ind, año_reciente, trim_reciente)

promedios = agrupar_por_aglomerado(df_ultima_fecha)

df_promedios = convertir_a_dataframe_formateado(promedios)

st.subheader("Promedio de edades por aglomerados.")

st.markdown(f'Se muestra información de la EPH mas reciente AÑO {año_reciente} T{trim_reciente}')

st.dataframe(df_promedios.reset_index(drop=True))


st.divider()


st.subheader("Evolución de la dependencia demográfica para cada año y trimestre.")

if "aglo_seleccionado" not in st.session_state:
    st.session_state.aglo_seleccionado = "Seleccionar..."

# Obtiene los cod de aglomerados disponibles formateados '02' para poder accederlo 
cod_aglos = sorted(df_ind['AGLOMERADO'].dropna().astype(int).astype(str).str.zfill(2).unique().tolist())
opciones_aglos = ["Seleccionar..."] + cod_aglos # Agregamos una opción inicial

select_aglo = st.selectbox(
    "Seleccione un aglomerado", 
    opciones_aglos,
    index=opciones_aglos.index(st.session_state.aglo_seleccionado),
    format_func=lambda cod: diccionario_aglomerados.get(cod, f"Aglomerado {cod}") if cod != "Seleccionar..." else cod,
)
# Actualizás el valor si cambió
if select_aglo != st.session_state.aglo_seleccionado:
    st.session_state.aglo_seleccionado = select_aglo

if st.session_state.aglo_seleccionado != "Seleccionar...":

    st.write("Seleccionó: ",diccionario_aglomerados.get(st.session_state.aglo_seleccionado))
    
    df_aglo = filtrar_por_aglomerado(df_ind, int(st.session_state.aglo_seleccionado))

    df_dep = calcular_dependencia_demografica(df_aglo)
    
    grafico_dependencia = armar_grafico_dependencia(df_dep, select_aglo)

    st.pyplot(grafico_dependencia)


st.divider()


df_resultado = calcular_media_y_mediana_edad(df_ind)

st.subheader("Media y mediana de edad por año y trimestre")

st.write("Media: es el promedio de edades.")
st.write("Mediana: el valor del medio (50%) si se ordenan todas las edades")

st.dataframe(df_resultado)
