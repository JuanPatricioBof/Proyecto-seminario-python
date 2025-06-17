import streamlit as st

st.set_page_config(
     page_title="EncuestAR",      # Cambialo según la página
     page_icon="📊",               # Podés usar emojis distintos en cada página
     layout="wide",
     initial_sidebar_state="expanded"
)

st.title('Encuest.AR')
st.markdown('Esta aplicacion permite analizar la Encuesta Permanente de Hogares (EPH) en Argentina.')
st.subheader('¿QUE ES LA EPH?')
st.markdown("""
La Encuesta Permanente de Hogares (EPH) es un programa nacional de produccion permanente de indicadores sociales cuyo objetivo es conocer las caracteristicas socioeconomicas de la poblacion.
Es realizada en forma conjunta por el Instituto Nacional de Estadística y Censos (INDEC) y las Direcciones Provinciales de Estadistica(DPE).""")

st.subheader(" ¿QUE CONTIENE LA EPH?")
st.markdown("""
La EPH contiene información sobre hogares y personas, incluyendo datos demográficos, educativos, laborales y de ingresos.""")

st.subheader("OBJETIVOS DE LA EPH")
st.markdown("""
- Proporcionar informacion estadistica sobre la situacion economica,social y demografica de la poblacion.
- Medir indicadores claves como la tasa de empleo, la tasa de desempleo y la pobreza.
- Evaluar el impacto de politicas publicas y programas sociales.
- Entender la relacion de la poblacion con el mercado laboral y la economia en general.""")