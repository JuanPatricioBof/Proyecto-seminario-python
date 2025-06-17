import pandas as pd
import matplotlib.pyplot as plt


def filtrar_individuos(df, año, trimestre, edad_min=0, edad_max=110):
    filtro = (
        (df["ANO4"] == año) &
        (df["TRIMESTRE"] == trimestre) &
        (df["CH06"] >= edad_min) &
        (df["CH06"] <= edad_max)
    )
    return df[filtro]


def agrupar_por_decada_y_genero(df):
    """Agrupa por década y genero
      Retorna un DataFrame donde las filas son las décadas y las columnas son los géneros:
       CH06	    Femenino	Masculino
       0	    12345	    11340
       10	    15023	    14876
       20	    16789	    16112
    """
    agrupado = (
        df
        .groupby([
            (df["CH06"] // 10 * 10),   # Década
            df["CH04_str"]            # Género
        ])["PONDERA"]
        .sum()
        .unstack(fill_value=0) # Cada género en una columna
    )
    return agrupado


def graficar_barras_dobles(agrupado, año, trimestre, colores=None):
    """Graficamos las columnas (sexos) por fila (décadas)"""
 
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0e1117')
    
    ax.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.legend(title='Sexo', facecolor='#0e1117', edgecolor='white', labelcolor='white', title_fontsize=10)

    agrupado.plot(kind='bar', ax=ax, color=colores)

    ax.set_title(f'Distribución por edad y sexo {año} T{trimestre}')
    ax.set_xlabel('Década de edad')
    ax.set_ylabel('Población ponderada')
    ax.legend(title='Sexo')
    ax.set_ylim(0, agrupado.max().max() * 1.15)
    plt.xticks(rotation=0)

    # Agregamos las etiquetas a cada barra
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', fontsize=8, label_type='edge', padding=2, rotation=90, color='white')

    return fig