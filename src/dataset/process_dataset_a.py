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
    # Informar el nombre del aglomerado con mayor cantidad de viviendas con más de dos ocupantes sin baño
    # 1. Abrir el archivo y leer el contenido:
    with path_procesado.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        
        # 2. Inicializar un diccionario para contar las viviendas sin baño por aglomerado:
        aglomerado_contador = {}
        
        for row in reader:
            # 4. Verificar si la vivienda tiene más de dos ocupantes y no tiene baño:
            if int(row['IX_TOT']) > 2 and row['IV8'] == '1':  # 1 indica que no tiene baño
                aglomerado = row['AGLOMERADO']
                pondera = int(row['PONDERA'])  # Número de hogares que respondieron lo mismo
                
                # 5. Contar la vivienda en el aglomerado correspondiente, ponderando por PONDERA:
                if aglomerado in aglomerado_contador:
                    aglomerado_contador[aglomerado] += pondera
                else:
                    aglomerado_contador[aglomerado] = pondera
    
    # 6. Encontrar el aglomerado con mayor cantidad de viviendas sin baño:
    if aglomerado_contador:
        max_aglomerado = max(aglomerado_contador, key=aglomerado_contador.get)
        max_count = aglomerado_contador[max_aglomerado]
        
        # 7. Imprimir el resultado con el nombre del aglomerado y la cantidad de viviendas ponderadas
        nombre_aglomerado = diccionario_aglomerados.get(str(max_aglomerado), "Desconocido")
        print(f"El aglomerado con mayor cantidad de viviendas sin baño y más de dos ocupantes es: {nombre_aglomerado} ({max_aglomerado}) con {max_count} viviendas.")
    else:
        print("No se encontraron viviendas que cumplan los requisitos.")


def informar_porcentaje_universitarios(path_procesado):
    # Diccionarios para acumular totales por aglomerado
    total_personas = {}
    personas_universitarias = {}

    with path_procesado.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')

        for row in reader:
            aglomerado = row['AGLOMERADO']
            nivel = row['NIVEL_ED']
            pondera = int(row['PONDERA'])

            if nivel not in {'1','2','3','4','5','6','7','9'} or not aglomerado:
                continue  # Saltear filas inválidas

            # Acumular total de personas
            total_personas[aglomerado] = total_personas.get(aglomerado, 0) + pondera

            # Acumular si tiene nivel universitario (5 o 6)
            if nivel in {'5', '6'}:
                personas_universitarias[aglomerado] = personas_universitarias.get(aglomerado, 0) + pondera

    print("Porcentaje de personas con nivel universitario o superior:\n")
    for aglo, total in total_personas.items():
        con_uni = personas_universitarias.get(aglo, 0)
        porcentaje = (con_uni / total) * 100 if total > 0 else 0
        nombre = diccionario_aglomerados.get(str(aglo), f"Aglomerado {aglo}")
        print(f"{nombre}: {porcentaje:.2f}%")
