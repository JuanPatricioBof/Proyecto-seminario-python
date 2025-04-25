""" SECCION B : información a obtener: consultas al dataset principal del 1 al 8 """
import csv

from src.utils.constants import AGLOMERADOS_NOMBRES

def informar_aglomerados_porcentajes(file_csv):
    """ 5. Informar para cada aglomerado el porcentaje de viviendas ocupadas por sus propietarios. """

    aglomerados = {} # total = cant total de viviendas, cumple = cant de vivi ocupadas por el propietario
    
    with file_csv.open('r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo, delimiter=';')

        for row in reader:
            codigo_aglomerado = row['AGLOMERADO']
            cantidad = int(row['PONDERA']) # cantidad de viviendas

            # si el código no está en el diccionario lo agrego e inicializo
            if codigo_aglomerado not in aglomerados:
                aglomerados[codigo_aglomerado] = { 'total': 0, 'cumple': 0, 'porcentaje': 0.0}
            
            #sumo total 
            aglomerados[codigo_aglomerado]['total'] += cantidad
            
            #si cumple sumo
            if row['II7'] == '1' or row['II7'] == '2':
                aglomerados[codigo_aglomerado]['cumple'] += cantidad

    #calcular porcentaje
    for aglo in aglomerados:
        calculo = (aglomerados[aglo]['cumple'] / aglomerados[aglo]['total'] ) * 100
        aglomerados[aglo]['porcentaje'] = round(calculo, 2)     # redondeo con 2 decimales

    # imprime de forma ordenada
    print("De cada aglomerado el porcentaje de viviendas ocupadas por el propietario")
    for codigo_aglom in sorted(aglomerados, key = lambda x: int(x)):
        print(f'{AGLOMERADOS_NOMBRES[codigo_aglom]}: {aglomerados[codigo_aglom]['porcentaje']}%' )