""" SECCION B : información a obtener: consultas al dataset principal del 1 al 8 """
import csv
from collections import defaultdict
from src.utils.constants import diccionario_aglomerados

def alfabetismo_por_ano(path_procesado):
    """1. Informar año tras año el porcentaje de personas mayores a 6 años que saben y no saben leer y escribir (último trimestre del año)"""
    datos = {}
    with path_procesado.open('r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo, delimiter=';')
        for row in reader:
            try:
                ano = row['ANO4']
                trimestre = row['TRIMESTRE']
                edad_raw = row['CH06'].strip()
                ch09_raw = row['CH09'].strip()

                if not edad_raw.isdigit() or ch09_raw not in ['1', '2']:
                    continue

                edad = int(edad_raw)
                ch09 = int(ch09_raw)

                if edad <= 6:
                    continue

                clave = (ano, trimestre)
                if clave not in datos:
                    datos[clave] = []
                datos[clave].append(ch09)
            except:
                continue

    # Guardar el último trimestre por año
    ultimo_trimestre_por_anio = {}
    for (ano, trimestre) in datos:
        if ano not in ultimo_trimestre_por_anio:
            ultimo_trimestre_por_anio[ano] = trimestre

    # Calcular e imprimir resultados
    for ano in sorted(ultimo_trimestre_por_anio):
        trimestre = ultimo_trimestre_por_anio[ano]
        respuestas = datos[(ano, trimestre)]
        total = len(respuestas)
        si = respuestas.count(1)
        no = respuestas.count(2)

        porcentaje_si = (si / total) * 100 if total > 0 else 0
        porcentaje_no = (no / total) * 100 if total > 0 else 0

        print(f"Año {ano} (trimestre {trimestre}):")
        print(f"  Sabe leer y escribir: {round(porcentaje_si, 2)}%")
        print(f"  No sabe leer y escribir: {round(porcentaje_no, 2)}%\n")

def extranjeros_con_estudios_universitarios(path_procesado):
    # Pedir año y trimestre al usuario
    ano_input = input("Ingrese el año: ").strip()
    trimestre_input = input("Ingrese el trimestre (1 a 4): ").strip()

    total_extranjeros = 0
    con_estudios_universitarios = 0

    with path_procesado.open('r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo, delimiter=';')
        for row in reader:
            ano = row['ANO4'].strip()
            trimestre = row['TRIMESTRE'].strip()
            lugar_nacimiento = row['CH15'].strip()
            nivel_educativo = row['NIVEL_ED'].strip()

            # Filtrar por año y trimestre
            if ano != ano_input or trimestre != trimestre_input:
                continue

            # Consideramos no nacidos en Argentina: códigos 4 y 5 (limítrofe y otro país)
            if lugar_nacimiento not in ['4', '5']:
                continue

            # Validar que el nivel educativo esté entre los que se consideran universitarios
            if nivel_educativo in ['5', '6']:  # Universitario incompleto o completo
                con_estudios_universitarios += 1

            total_extranjeros += 1

    if total_extranjeros == 0:
        print("No se encontraron personas extranjeras para ese año y trimestre.")
        return

    porcentaje = (con_estudios_universitarios / total_extranjeros) * 100
    print(f"Para el año {ano_input}, trimestre {trimestre_input}:")
    print(f"El {round(porcentaje, 2)}% de las personas no nacidas en Argentina tienen estudios universitarios o superiores.")

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
