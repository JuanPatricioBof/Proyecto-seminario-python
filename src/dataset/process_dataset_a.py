""" SECCION B : información a obtener: consultas al dataset principal del 1 al 8 """
import csv

from src.utils.constants import diccionario_aglomerados

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
        print(f'{diccionario_aglomerados[codigo_aglom]}: {aglomerados[codigo_aglom]['porcentaje']}%' )

def informar_aglomerado_punto6(path_procesado):
#Informar el nombre del  aglomerado con mayor cantidad de viviendas con más de dos ocupantes  sin baño. Informar también la cantidad de ellas.
 
# 1. Abrir el archivo y leer el contenido:
  with path_procesado.open('r',encoding='utf-8') as file_csv:
        reader=csv.DictReader(file_csv,delimiter=';')
        fieldnames=reader.fieldnames
        #2. Inicializar un diccionario para contar las viviendas sin baño por aglomerado:
        aglomerado_contador = {}
     
        for row in reader:
            #4. Verificar si la vivienda tiene más de dos ocupantes y no tiene baño:
            if int(row['IX_TOT']) > 2 and row['IV8'] == '2':
                aglomerado = row['AGLOMERADO']
                #5. Contar la vivienda en el aglomerado correspondiente:
                if aglomerado in aglomerado_contador:
                    aglomerado_contador[aglomerado] += 1
                else:
                    aglomerado_contador[aglomerado] = 1
    #6. Encontrar el aglomerado con mayor cantidad de viviendas sin baño:
  max_aglomerado = max(aglomerado_contador, key=aglomerado_contador.get)
  max_count = aglomerado_contador[max_aglomerado]
  print(f"El aglomerado con mayor cantidad de viviendas sin baño y más de dos ocupantes es:{diccionario_aglomerados[str(max_aglomerado)]}({max_aglomerado}) con {max_count} viviendas.")
    


import csv

def informar_nivel_universitario(path_procesado):
    total_por_aglomerado = {}
    universitarios_por_aglomerado = {}

    with path_procesado.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        for row in reader:
            aglomerado = row['AGLOMERADO']
            nivel = row['NIVEL_ED'].strip()

            if aglomerado not in total_por_aglomerado:
                total_por_aglomerado[aglomerado] = 0
                universitarios_por_aglomerado[aglomerado] = 0

            total_por_aglomerado[aglomerado] += 1

            if nivel in {'5', '6'}:  # Universitario incompleto o completo
                universitarios_por_aglomerado[aglomerado] += 1

    

    print("\nPorcentaje de personas con nivel universitario o superior:\n")
    for aglo in total_por_aglomerado:
        if str(aglo) in diccionario_aglomerados:
            total = total_por_aglomerado[aglo]
            uni = universitarios_por_aglomerado[aglo]

            # Si el total es mayor que 1, calculamos el porcentaje
            if total > 1:
                porcentaje = (uni / total) * 100
                nombre = diccionario_aglomerados[str(aglo)]
                print(f"{nombre}: {porcentaje:.2f}%")
            else:
                print(f"{diccionario_aglomerados[str(aglo)]}: No suficiente data para calcular porcentaje.")

