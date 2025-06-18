import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.loader import cargar_parcial_csv, cargar_json
from src.utils.constants import PATHS,PROJECT_PATH
from src.functions_streamlit import ingresos

st.title("Análisis de Ingresos de los Hogares")

st.info("""
**Nota metodológica:**  
Los resultados obtenidos no poseen valor estadístico. Los montos de la canasta básica corresponden a CABA, mientras que la EPH es nacional. Además, al filtrar sólo hogares de 4 integrantes sin considerar la cantidad de menores, la estimación no es totalmente representativa.
""")

columnas_necesarias=['ANO4','TRIMESTRE','IX_TOT','ITF','PONDIH']
df=cargar_parcial_csv(PATHS["hogar"]["csv"], usecols=columnas_necesarias)
fechas_disponibles=cargar_json(PATHS["hogar"]["json"])

# Se carga la canasta basica de alimentos
path_canasta=PROJECT_PATH / "files" / "valores-canasta-basica-alimentos-canasta-basica-total-mensual-2016.csv"
df_canasta=pd.read_csv(path_canasta,sep=',')
canasta_promedio=ingresos.procesar_canasta(df_canasta)

st.subheader("Selección de Año y Trimestre")

hogares_disponibles = {int(anio): trimestres for anio, trimestres in fechas_disponibles.items()}
todos_los_anios = list(range(2016, 2026))
anio_usuario = st.selectbox("Seleccione el año", todos_los_anios)
todos_los_trimestres = [1, 2, 3, 4]
trimestre_usuario = st.selectbox("Seleccione el trimestre", todos_los_trimestres)

if anio_usuario in hogares_disponibles and trimestre_usuario in hogares_disponibles[anio_usuario]:
    st.success(f"✅ Hay datos disponibles para el año {anio_usuario} y trimestre {trimestre_usuario}.")
else:
    st.warning(f"⚠ No hay datos para el año {anio_usuario} y trimestre {trimestre_usuario}.")

fila_canasta = canasta_promedio[
    (canasta_promedio['ANIO'] == anio_usuario) & 
    (canasta_promedio['TRIMESTRE'] == trimestre_usuario)
]

if fila_canasta.empty:
    st.warning(f"No hay datos de canasta básica para {anio_usuario} T{trimestre_usuario}.")
else:
    cbt=fila_canasta.iloc[0]['CBT']
    cbi=fila_canasta.iloc[0]['CBI']

    hogares_filtrados = ingresos.filtrar_hogares(df, anio_usuario, trimestre_usuario)
    resultados = ingresos.calcular_ingresos(hogares_filtrados, cbt, cbi)

    if resultados['total']==0:
        st.warning(f"No hay hogares de 4 integrantes para {anio_usuario} T{trimestre_usuario}.")
    else:
        st.subheader(f"Resultados para {anio_usuario} T{trimestre_usuario}")
        st.write(f"Total de hogares de 4 integrantes analizados: {int(resultados['total']):,}")
        st.write(f"Hogares que están por debajo de la línea de indigencia: **{int(resultados['indigencia']):,}**"
                 f" ({resultados['indigencia']/resultados['total']*100:.2f}%)")
        st.write(f"Hogares que están por debajo de la línea de pobreza: **{int(resultados['pobreza']):,}**"
                 f" ({resultados['pobreza']/resultados['total']*100:.2f}%)")

        # Agregamos el gráfico de barras
        st.subheader("Visualización gráfica")

        etiquetas = ['Indigencia', 'Pobreza (no indigentes)', 'No pobres']
        valores = [
            resultados['indigencia'],
            resultados['pobreza'],
            resultados['no_pobres']
        ]

        fig, ax = plt.subplots()
        barras = ax.barh(etiquetas, valores, color=['#FF6F61', '#FFA500', '#4CAF50'])
        ax.set_xlabel("Cantidad de hogares")

        for barra in barras:
            ancho = barra.get_width()#EL VALOR DE CADA BARRA
            ax.text(ancho, barra.get_y() + barra.get_height()/2, f'{int(ancho):,}', va='center')#CALCULA LA POSICION DEL TEXTO EN LA BARRA

        st.pyplot(fig)
