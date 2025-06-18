import streamlit as st
import pandas as pd
from pathlib import Path
from src.utils.constants import DATA_OUT_PATH
from src.functions_streamlit.empleo import cargar_datos, cargar_metadata, mapear_nivel_educativo, format_number

# Configuración inicial
st.set_page_config(page_title="Actividad y Empleo - EPH", page_icon="📊")
st.title("Desocupados por Nivel Educativo (EPH)")
st.markdown("### Distribución de personas desocupadas según nivel educativo alcanzado")

# Cargar datos
df = cargar_datos(DATA_OUT_PATH / 'individual_process.csv')
if df is None:
    st.stop()

metadata = cargar_metadata(DATA_OUT_PATH / 'estructura_individuos.json')
if not metadata:
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Filtros")
    anos_disponibles = sorted([int(a) for a in metadata.keys()], reverse=True)
    ano_seleccionado = st.selectbox("Año", anos_disponibles)
    trimestres_disponibles = sorted([int(t) for t in metadata[str(ano_seleccionado)]])
    trimestre_seleccionado = st.selectbox("Trimestre", trimestres_disponibles)

# Filtrado
datos_filtrados = df[
    (df['ANO4'] == ano_seleccionado) & 
    (df['TRIMESTRE'] == trimestre_seleccionado) & 
    (df['ESTADO'] == 2)
]

if datos_filtrados.empty:
    st.warning(f"No hay desocupados para {ano_seleccionado} T{trimestre_seleccionado}")
    st.stop()

conteo = datos_filtrados.groupby('NIVEL_ED')['PONDERA'].sum().round().astype(int)
conteo = mapear_nivel_educativo(conteo, conteo.values)

# Visualización
st.subheader(f"Desocupados - {ano_seleccionado} T{trimestre_seleccionado}")

# Gráfico y métricas
col1, col2 = st.columns([3, 1])
with col1:
    st.bar_chart(conteo)
with col2:
    st.metric("Total", f"{conteo.sum():,.0f}".replace(",", "."))

df_resultado = pd.DataFrame({
    'Nivel Educativo': conteo.index,
    'Cantidad': conteo.values,
    'Porcentaje': (conteo.values / conteo.sum() * 100).round(1)
})

st.dataframe(
    df_resultado.style.format({
        'Cantidad': format_number,
        'Porcentaje': "{:.1f}%"
    }).hide(axis="index"),
    use_container_width=True,
    height=min(400, 35 * len(conteo) + 35)
)

st.caption(f"Fuente: EPH-INDEC | Años disponibles: {', '.join(str(a) for a in anos_disponibles)}")
