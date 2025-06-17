import pandas as pd

def obtener_estadisticas_empleo(df, codigo_aglomerado):
    """Obtiene estadísticas de empleo para un aglomerado específico y devuelve el porcentaje de ocupados, etiquetas y tamaños para un gráfico de torta"""
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)
    df['CONDICION_LABORAL'] = df['CONDICION_LABORAL'].str.strip()

    df_aglo = df[df['AGLOMERADO'] == codigo_aglomerado]

    if df_aglo.empty or 'PONDERA' not in df_aglo.columns:
        return 0, [], []

    total_personas = df_aglo['PONDERA'].sum()

    ocupados_validos = ['Ocupado autónomo', 'Ocupado dependiente']
    df_ocupados = df_aglo[df_aglo['CONDICION_LABORAL'].isin(ocupados_validos)].copy()

    total_ocupados = df_ocupados['PONDERA'].sum()

    if total_ocupados == 0 or total_personas == 0:
        return 0, [], []

    porcentaje_ocupados = round((total_ocupados / total_personas) * 100, 1)

    mapeo = {1: 'Estatal', 2: 'Privado', 3: 'Otro'}
    df_ocupados['TIPO_EMPLEO'] = df_ocupados['PP04A'].map(mapeo)

    conteo = df_ocupados.groupby('TIPO_EMPLEO')['PONDERA'].sum()

    labels = conteo.index.tolist()
    sizes = [round((v / total_ocupados) * 100, 1) for v in conteo.values]

    return porcentaje_ocupados, labels, sizes
