""" SECCION B : información a obtener: consultas al dataset principal del 1 al 8 """
import csv
from collections import defaultdict
from src.utils.constants import diccionario_aglomerados

def ano_y_trimestre_menor_desocupacion_PB_EJ3(path_procesado):
    """3. Informar el ano y trimestre donde hubo menos desocupacion"""
    ano_trimestres= {}
    with path_procesado.open('r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo,delimiter=';')
        for row in reader:
            ano=row['ANO4']
            trimestre=row['TRIMESTRE']
            condicion=row['ESTADO']
            pondera = int(row['PONDERA'])
            if condicion=='2': #Desocupado
                clave = (ano,trimestre)
                if clave not in ano_trimestres:
                    ano_trimestres[clave]= 0
                ano_trimestres[clave] +=pondera
    # Buscar la clave(ano, trimestre) con menor decupacion
    menor_clave = min(ano_trimestres, key=ano_trimestres.get)
    menor_valor = ano_trimestres[menor_clave]
    print(f"El menor nivel de desocupacion fue en el ano {menor_clave[0]}, trimestre {menor_clave[1]}")
    
def ranking_aglomerado_EJ4(DATA_OUT_PATH):
    hogar_path = DATA_OUT_PATH / "hogar_process.csv"
    individual_path = DATA_OUT_PATH / "individual_process.csv"
    
    # 1. Contar universitarios por hogar (CODUSU)
    universitarios_por_hogar = defaultdict(int)

    with open(individual_path, newline='', encoding='utf-8') as f_ind:
        reader = csv.DictReader(f_ind, delimiter=';')
        for row in reader:
            codusu = row.get('CODUSU')
            nivel_ed = row.get('NIVEL_ED')
            if codusu and nivel_ed == '6':
                universitarios_por_hogar[codusu] += 1

    # 2. Contar hogares por aglomerado
    total_hogares = defaultdict(int)
    hogares_calificados = defaultdict(int)

    with open(hogar_path, newline='', encoding='utf-8') as f_hog:
        reader = csv.DictReader(f_hog, delimiter=';')
        for row in reader:
            codusu = row.get('CODUSU')
            aglomerado = row.get('AGLOMERADO')

            if not codusu or not aglomerado:
                continue  # saltear si falta info

            total_hogares[aglomerado] += 1

            if universitarios_por_hogar.get(codusu, 0) >= 2:
                hogares_calificados[aglomerado] += 1

    # 3. Calcular porcentajes
    ranking = []
    for aglo in total_hogares:
        total = total_hogares[aglo]
        calificados = hogares_calificados.get(aglo, 0)
        porcentaje = (calificados / total) * 100 if total > 0 else 0
        codigo_aglo = str(aglo).zfill(2)  # <- clave formateada
        nombre_aglo = diccionario_aglomerados.get(codigo_aglo, f"Aglomerado {codigo_aglo}")
        ranking.append((nombre_aglo, porcentaje))

    # 4. Ordenar por porcentaje descendente y mostrar top 5
    ranking.sort(key=lambda x: x[1], reverse=True)

    print("Top 5 aglomerados con mayor porcentaje de hogares con ≥2 universitarios completos:\n")
    for nombre_aglo, pct in ranking[:5]:
        print(f"{nombre_aglo}: {pct:.2f}%")
            

def informar_aglomerados_porcentajes_5B(file_csv):
    """ 5. Informar para cada aglomerado el porcentaje de viviendas ocupadas por sus propietarios. """

    aglomerados = {} # { codigo_aglomerado : {total: 0, cumple: 0, porcentaje: 0.0} ...}
    
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
        total = aglomerados[aglo]['total'] 
        if total != 0: 
            cumple = aglomerados[aglo]['cumple'] 
            calculo = (cumple / total ) * 100
            aglomerados[aglo]['porcentaje'] = round(calculo, 2)     # redondeo con 2 decimales

    # imprime de forma ordenada segun el codigo de aglomerado
    print("De cada aglomerado el porcentaje de viviendas ocupadas por el propietario")
    
    for codigo_aglom in sorted(aglomerados, key = lambda x: int(x)):
        print(f'{diccionario_aglomerados[codigo_aglom.zfill(2)]}: {aglomerados[codigo_aglom]['porcentaje']}%' )

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
                pondera = int(row['PONDERA'])  # Número de hogares que respondieron lo mismo


                #5. Contar la vivienda en el aglomerado correspondiente:
                if aglomerado in aglomerado_contador:
                     aglomerado_contador[aglomerado] += pondera
                else:
                     aglomerado_contador[aglomerado] = pondera
    #6. Encontrar el aglomerado con mayor cantidad de viviendas sin baño:
  max_aglomerado = max(aglomerado_contador, key=aglomerado_contador.get)
  max_count = aglomerado_contador[max_aglomerado]
  print(f"El aglomerado con mayor cantidad de viviendas sin baño y más de dos ocupantes es:{diccionario_aglomerados[str(max_aglomerado).zfill(2)]}({max_aglomerado}) con {max_count} viviendas.")
    
def informar_nivel_universitario(path_procesado):
    total_por_aglomerado = {}
    universitarios_por_aglomerado = {}

    with path_procesado.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        for row in reader:
            aglomerado = row['AGLOMERADO']
            nivel = row['NIVEL_ED'].strip()
            pondera=int(row["PONDERA"]) #Tomamos la Ponderacion

            if aglomerado not in total_por_aglomerado:
                total_por_aglomerado[aglomerado] = 0
                universitarios_por_aglomerado[aglomerado] = 0

            total_por_aglomerado[aglomerado] += pondera

            if nivel in {'5', '6'}:  # Universitario incompleto o completo
                universitarios_por_aglomerado[aglomerado] += pondera

    

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
