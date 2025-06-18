import pandas as pd

def calcular_trimestre(mes):
    if mes in [1, 2, 3]:
        return 1
    elif mes in [4, 5, 6]:
        return 2
    elif mes in [7, 8, 9]:
        return 3
    else:
        return 4

def procesar_canasta(canasta_df):
    canasta_df = canasta_df.copy()

    # Convertir indice_tiempo a datetime
    canasta_df['indice_tiempo'] = pd.to_datetime(canasta_df['indice_tiempo'])

    # Extraer año y trimestre
    canasta_df['ANIO'] = canasta_df['indice_tiempo'].dt.year
    canasta_df['MES'] = canasta_df['indice_tiempo'].dt.month
    canasta_df['TRIMESTRE'] = canasta_df['MES'].apply(calcular_trimestre)

    # Renombrar columnas relevantes
    canasta_df['CBT'] = canasta_df['canasta_basica_total']
    canasta_df['CBI'] = canasta_df['linea_indigencia']

    # Agrupar por año y trimestre sacando promedio
    canasta_promedio = canasta_df.groupby(['ANIO', 'TRIMESTRE']).agg({
        'CBT': 'mean',
        'CBI': 'mean'
    }).reset_index()

    return canasta_promedio

def filtrar_hogares(hogares_df, anio, trimestre):
    hogares_4 = hogares_df[hogares_df['IX_TOT'] == 4]
    filtrado = hogares_4[(hogares_4['ANO4'] == anio) & (hogares_4['TRIMESTRE'] == trimestre)]
    return filtrado

def calcular_pobreza(hogares_filtrados, cbt, cbi):
    if hogares_filtrados.empty:
        return {
            'total': 0,
            'indigencia': 0,
            'pobreza': 0,
            'no_pobres': 0
        }

    # Clasificar hogares según ITF vs CBI/CBT
    hogares_filtrados['clasificacion'] = hogares_filtrados['ITF'].apply(
        lambda x: 'indigencia' if x < cbi else ('pobreza' if x < cbt else 'no_pobres')
    )

    # Calcular los totales ponderados
    resumen = hogares_filtrados.groupby('clasificacion')['PONDERA'].sum().to_dict()

    total = hogares_filtrados['PONDERA'].sum()
    indigencia = resumen.get('indigencia', 0)
    pobreza = resumen.get('pobreza', 0)
    no_pobres = resumen.get('no_pobres', 0)

    return {
        'total': total,
        'indigencia': indigencia,
        'pobreza': pobreza,
        'no_pobres': no_pobres
    }
