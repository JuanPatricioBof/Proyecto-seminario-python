import csv
import json
from src.utils.constants import DATA_OUT_PATH
from collections import defaultdict
from pathlib import Path
from src.utils.constants import diccionario_aglomerados


def alfabetismo_por_ano(path_procesado):
    """1. Informar año tras año el porcentaje de personas mayores a 6 años que saben y no saben leer y escribir (último trimestre del año)"""
    json_individuos_path = DATA_OUT_PATH/"estructura_individuos.json"
    # Cargar el JSON con los trimestres disponibles
    with open(json_individuos_path, 'r', encoding='utf-8') as f:
        trimestres_por_anio = json.load(f)

    # Crear diccionario con el último trimestre disponible por año
    ultimos_trimestres = {
        anio: str(max(trimestres)) # usamos str porque en el CSV los trimestres son string
        for anio, trimestres in trimestres_por_anio.items()
    } 
    datos = {}
    with path_procesado.open('r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo, delimiter=';')
        for row in reader:
            try:
                ano = row['ANO4']
                trimestre = row['TRIMESTRE']
                edad_raw = row['CH06'].strip()
                ch09_raw = row['CH09'].strip()
                pondera_raw = row['PONDERA'].strip()

                if not (edad_raw.isdigit() and ch09_raw in ['1', '2'] and pondera_raw.isdigit()):
                    continue

                if trimestre != ultimos_trimestres.get(ano):
                    continue

                edad = int(edad_raw)
                ch09 = int(ch09_raw)
                pondera = int(pondera_raw)

                if edad <= 6:
                    continue

                if ano not in datos:
                    datos[ano] = []
                datos[ano].append((ch09, pondera))
            except:
                continue

    # Calcular e imprimir resultados
    for ano in sorted(datos):
        respuestas = datos[ano]
        total = sum(pondera for ch09, pondera in respuestas)
        si = sum(pondera for ch09, pondera in respuestas if ch09 == 1)
        no = sum(pondera for ch09, pondera in respuestas if ch09 == 2)

        porcentaje_si = (si / total) * 100 if total > 0 else 0
        porcentaje_no = (no / total) * 100 if total > 0 else 0

        print(f"Año {ano} (trimestre {ultimos_trimestres[ano]}):")
        print(f"  Sabe leer y escribir: {round(porcentaje_si, 2)}%")
        print(f"  No sabe leer y escribir: {round(porcentaje_no, 2)}%\n")


def extranjeros_con_estudios_universitarios(path_procesado):
    """Informa el porcentaje de personas no nacidas en Argentina con nivel universitario o superior para un año y trimestre específico"""
    json_individuos_path = DATA_OUT_PATH/"estructura_individuos.json"
     # Cargar años y trimestres válidos desde el JSON
    with open(json_individuos_path, 'r', encoding='utf-8') as f:
        estructura = json.load(f)

    try:
        ano_input = input("Ingrese el año: ").strip()
        if ano_input not in estructura:
            raise ValueError(f"Año inválido. Años disponibles: {', '.join(estructura.keys())}")

        trimestre_input = input("Ingrese el trimestre (1 a 4): ").strip()
            
        if trimestre_input not in estructura[ano_input]:
            raise ValueError(f"Trimestre inválido. Trimestres disponibles para el año {ano_input}: {estructura[ano_input]}")

    except ValueError as e:
        print(f"Error: {e}")
        return

    total_extranjeros = 0
    con_estudios_universitarios = 0

    with path_procesado.open('r', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo, delimiter=';')
        for row in reader:
            ano = row['ANO4'].strip()
            trimestre = row['TRIMESTRE'].strip()
            lugar_nacimiento = row['CH15'].strip()
            nivel_educativo = row['NIVEL_ED'].strip()
            pondera_raw = row['PONDERA'].strip()

            # Filtrar por año y trimestre
            if ano != ano_input or trimestre != trimestre_input:
                continue

            # Consideramos no nacidos en Argentina: códigos 4 y 5 (limítrofe y otro país)
            if lugar_nacimiento not in ['4', '5']:
                continue

            if not pondera_raw.isdigit():
                continue
            
            pondera = int(pondera_raw)
            total_extranjeros += pondera
            
            # Validar que el nivel educativo esté entre los que se consideran universitarios
            if nivel_educativo in ['5', '6']:  # Universitario incompleto o completo
                con_estudios_universitarios += pondera


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
    

def ranking_aglomerado_EJ4(hogar_path: Path, individual_path: Path):
    """
    Calcula y muestra el top 5 de aglomerados con mayor porcentaje de hogares
    que tienen 2 o más integrantes con estudios universitarios completos (NIVEL_ED=6).
    
    Args:
        DATA_OUT_PATH (Path): Ruta donde se encuentran los archivos procesados
                             'hogar_process.csv' e 'individual_process.csv'.
    """    
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
  """Informar el aglomerado con mayor cantidad de viviendas con más de dos ocupantes
y sin baño. Informar también la cantidad de ellas.""" 
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
    """ 7. Informar para cada aglomerado el porcentaje de personas que hayan cursado al
menos en nivel universitario o superior. """
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


# ----------------------------------SECCION B---------------------------------
def tabla_nivel_educativo_por_aglomerado_EJ_9B(individual_path):
    """Genera tabla de niveles educativos para un aglomerado específico."""
    
    # Pedir y normalizar input (elimina ceros izquierda para comparación)
    aglomerado_elegido = input("\nIngrese el código del aglomerado (ej: 2 o 02 para La Plata): ").strip().lstrip("0")
    if not aglomerado_elegido:  # Si ingresa "0" o ""
        aglomerado_elegido = "0"

    tabla = defaultdict(lambda: defaultdict(int))

    with open(individual_path, newline='', encoding='latin-1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Normaliza el aglomerado del CSV (elimina ceros izquierda)
            aglo_csv = row['AGLOMERADO'].lstrip("0") or "0"  # "02" -> "2", "00" -> "0"
            
            if aglo_csv != aglomerado_elegido:
                continue

            try:
                edad = int(row['CH06'])
                if edad < 18:
                    continue

                año = int(row['ANO4'])
                trimestre = int(row['TRIMESTRE'])
                nivel_ed = int(row['NIVEL_ED'])
                pondera = float(row['PONDERA'])

                clave = (año, trimestre)
                tabla[clave][nivel_ed] += pondera
            except (ValueError, KeyError):
                continue

    if not tabla:
        print(f"\nNo se encontraron datos para el aglomerado {aglomerado_elegido}")
        return

    # Mostrar resultados (similar a tu versión original)
    print(f"\nTabla para aglomerado {aglomerado_elegido}:")
    print("Año | Trimestre | Sin instr. | Prim. Inc. | Prim. Comp. | Sec. Inc. | Sec. Comp. | Sup. Univ.")
    for (año, trim) in sorted(tabla.keys(), reverse=True):
        niveles = tabla[(año, trim)]
        fila = [
            año,
            trim,
            f"{niveles.get(7, 0):,.0f}",
            f"{niveles.get(1, 0):,.0f}",
            f"{niveles.get(2, 0):,.0f}",
            f"{niveles.get(3, 0):,.0f}",
            f"{niveles.get(4, 0):,.0f}",
            f"{niveles.get(5, 0) + niveles.get(6, 0):,.0f}"
        ]
        print("{:<4} | {:<9} | {:<11} | {:<10} | {:<12} | {:<8} | {:<9} | {:<12}".format(*fila))
        
        
def informar_tabla_porcentaje_10B(file_csv_individuos):
    """Pedir al usuario que seleccione dos aglomerados y a partir de la información
contenida retornar una tabla que contenga el porcentaje de personas mayores de
edad con secundario incompleto."""
    """ Estructura de la variable tabla: 
    { 
        año: {
            trimestre: {
                    agloA: {total:0, cumple:0, porcentaje:0.0}
                    agloB:  {total:0, cumple:0, porcentaje:0.0}
                }
            trimestre:  {...}
        }
        año: {...} 
    }"""

    #muestro al usuario las opciones de aglomerado (imprimo diccionario de codigo:nombre)
    salida = ''
    for key in diccionario_aglomerados:
        salida += f'{key}: {diccionario_aglomerados[key]}, '     
    print(salida)
    
    #pido al usuario que ingrese data
    aglo_A = input("Ingrese código de aglomerado:_").zfill(2)
    aglo_B = input("Ingrese código de aglomerado:_").zfill(2)
    
    if aglo_A not in diccionario_aglomerados or aglo_B not in diccionario_aglomerados:
        print("Aglomerado/s inválido/s.")
        return
    
    tabla = {}

    # recorro el archivo procesado 
    print("Procesando archivo...")

    with file_csv_individuos.open('r', encoding='utf-8')as archivo:
        reader = csv.DictReader(archivo, delimiter=';')

        for row in reader:
            # si la fila es del aglomerado ingresado --> evaluo
            aglo = row['AGLOMERADO']
            cantidad = int(row['PONDERA'])
            
            # si es el aglomerado ingresado --> proceso
            if(aglo == aglo_A.lstrip("0") or aglo == aglo_B.lstrip("0") ):
                año = row['ANO4']
                trimestre = row['TRIMESTRE']

                #inicializo
                if año not in tabla:
                    tabla[año] = {}

                if trimestre not in tabla[año]:
                    tabla[año][trimestre] = {}

                if aglo not in tabla[año][trimestre]:
                    tabla[año][trimestre][aglo_A.lstrip("0")] = {'total': 0, 'cumple': 0, 'porcentaje': 0.0}
                    tabla[año][trimestre][aglo_B.lstrip("0")] = {'total': 0, 'cumple': 0, 'porcentaje': 0.0}
                
                # sumo el total de aglomerados
                tabla[año][trimestre][aglo]['total'] += cantidad
                # sumo los aglomerados que cumplen
                if (row['NIVEL_ED_str'] == 'Secundario incompleto') and ( int( row['CH06'] ) > 60 ):
                #if (row['NIVEL_ED'] == '3') and ( int( row['CH06'] ) > 60 ):
                    tabla[año][trimestre][aglo]['cumple'] += cantidad

    # calculo el porcentaje de aglomerado para cada trimestre y año
    print("Calculando porcentaje...")
    for año in tabla:
        for trimestre in tabla[año]:
            for aglo in tabla[año][trimestre]:
                total = tabla[año][trimestre][aglo]['total']
                if total != 0 : 
                    cumple = tabla[año][trimestre][aglo]['cumple']
                    calculo = (cumple / total) * 100
                    tabla[año][trimestre][aglo]['porcentaje'] = round(calculo,2)

    # mostrar informacion
    print("Mostrar información...")    
    # imprimo encabezado de tabla
    print(f'Año    Trimestre   {diccionario_aglomerados[aglo_A]}     {diccionario_aglomerados[aglo_B]}') 
    
    for año in sorted(tabla):
        for trimestre in sorted(tabla[año]):
            salida = (f'{año}   {trimestre}    ')
            for aglo in tabla[año][trimestre]:
                salida += str (tabla[año][trimestre][aglo]['porcentaje'] ) + '%    '
            print(salida)


def informar_aglomerados_punto11(path_procesado):
    """ . Informar el aglomerado con mayor cantidad de viviendas con más de dos ocupantes
y sin baño. Informar también la cantidad de ellas.
"""
    anio = input("Ingrese el año que desea consultar: ")
    if not anio.isdigit():
        print("Por favor, ingrese un año válido.")
        return

    datos = []
    with path_procesado.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        for row in reader:
            if row['ANO4'] == anio:
                datos.append(row)

    if not datos:
        print(f"No hay datos cargados para el año {anio}.")
        return

    # Como los datos están ordenados por año y trimestre en forma descendente,
    # el primer registro del año es del trimestre más reciente
    ultimo_trimestre = int(datos[0]['TRIMESTRE'])
    datos_ultimo_trimestre = [
        row for row in datos if int(row['TRIMESTRE']) == ultimo_trimestre
    ]

    viviendas_totales = {}
    viviendas_precarias = {}

    for row in datos_ultimo_trimestre:
        aglomerado = row['AGLOMERADO']
        tipo_material = row['material_techumbre'].strip().lower()

        try:
            pondera = int(row["PONDERA"])
        except ValueError:
            continue  # Saltar si el dato está mal cargado

        if aglomerado not in viviendas_totales:
            viviendas_totales[aglomerado] = 0
            viviendas_precarias[aglomerado] = 0

        viviendas_totales[aglomerado] += pondera
        if tipo_material=='material precario':
            viviendas_precarias[aglomerado] += pondera

    porcentajes = {}
    for aglomerado in viviendas_totales:
        total = viviendas_totales[aglomerado]
        precarias = viviendas_precarias[aglomerado]
        if total > 0:
            porcentajes[aglomerado] = (precarias / total) * 100

    porcentajes_validos = {
        aglo: porcentaje
        for aglo, porcentaje in porcentajes.items()
        if str(aglo) in diccionario_aglomerados
    }

    if not porcentajes_validos:
        print("No se encontraron aglomerados válidos con nombre para mostrar.")
        return

    max_aglomerado = max(porcentajes_validos, key=porcentajes_validos.get)
    min_aglomerado = min(porcentajes_validos, key=porcentajes_validos.get)

    nombre_max = diccionario_aglomerados[str(max_aglomerado)]
    nombre_min = diccionario_aglomerados[str(min_aglomerado)]

    print(f"\nTrimestre analizado: {ultimo_trimestre} del año {anio}")
    print("Porcentaje de viviendas con material precario por aglomerado:")

    for aglo, porcentaje in sorted(porcentajes_validos.items(), key=lambda x: x[1], reverse=True):
        nombre = diccionario_aglomerados[str(aglo)]
        print(f"  - {nombre}: {porcentaje:.2f}%")

    print(f"\nEl aglomerado con mayor porcentaje es {nombre_max} ({porcentajes_validos[max_aglomerado]:.2f}%)")
    print(f"El aglomerado con menor porcentaje es {nombre_min} ({porcentajes_validos[min_aglomerado]:.2f}%)")


def universitarios_en_viviendas_insuficientes(hogar_path: Path, individual_path: Path):
    """cantidad de personas que hayan cursado nivel universitario o superior y que vivan en una vivienda con CONDICION_DE_HABITABILIDAD insuficiente"""
    json_individuos_path = DATA_OUT_PATH/"estructura_individuos.json"
    json_hogares_path = DATA_OUT_PATH/"estructura_hogares.json"

    # Leer ambos JSON desde dentro de la función
    try:
        with open(json_individuos_path, encoding='utf-8') as f_ind:
            estructura_json_individuos = json.load(f_ind)

        with open(json_hogares_path, encoding='utf-8') as f_hog:
            estructura_json_hogares = json.load(f_hog)
    except FileNotFoundError as e:
        print(f"Error: {e.filename} no encontrado.")
        return

    # Pedir y validar input del usuario
    anio = input("Ingrese el año que desea consultar: ").strip()

    if anio not in estructura_json_individuos or anio not in estructura_json_hogares:
        print("El año no está disponible en ambos conjuntos de datos.")
        return

    # Obtener el último trimestre de ambos
    ult_trim_ind = max(estructura_json_individuos[anio], key=lambda t: int(t))
    ult_trim_hog = max(estructura_json_hogares[anio], key=lambda t: int(t))

    if ult_trim_ind != ult_trim_hog:
        print(f"Conflicto: El último trimestre en individuos es {ult_trim_ind}, pero en hogares es {ult_trim_hog}.")
        return
    
    ultimo_trimestre = ult_trim_ind

    # Filtrar viviendas con condición insuficiente del archivo de hogar
    codusus_insuficientes = set()
    with hogar_path.open(encoding='utf-8') as f_hog:
        reader = csv.DictReader(f_hog, delimiter=';')
        for row in reader:
            ano = row['ANO4'].strip()
            trimestre = row['TRIMESTRE'].strip()
            if ano == anio and trimestre == ultimo_trimestre:
                if row['CONDICION_DE_HABITABILIDAD'].strip().lower() == 'insuficiente':
                    codusus_insuficientes.add(row['CODUSU'].strip())

    # Leer archivo individual y acumular PONDERA si cumple condiciones
    total_ponderado = 0
    with individual_path.open(encoding='utf-8') as f_ind:
        reader = csv.DictReader(f_ind, delimiter=';')
        for row in reader:
            ano = row['ANO4'].strip()
            trimestre = row['TRIMESTRE'].strip()
            if ano == anio and trimestre == ultimo_trimestre:
                codusu = row['CODUSU'].strip()
                nivel_ed = row['NIVEL_ED'].strip()
                pondera = row['PONDERA'].strip()

                if codusu in codusus_insuficientes and nivel_ed in ['5', '6']:
                    if pondera.isdigit():
                        total_ponderado += int(pondera)

    print(f"\nAño {anio} - Trimestre {ultimo_trimestre}:")
    print(f"Cantidad de personas con nivel universitario o superior en viviendas  con condición insuficiente: {total_ponderado}")


def regiones_segun_porcentaje_inquilinos(hogar_path):
    """ Recibe la ruta al archivo e informa las regiones en orden
        descendiente según su porcentaje de inquilinos. 
        El porcentaje de inquilinos de cada región se calcula en base a la
        cantidad de inquilinos (valor 3 en la columna "II7") sobre la cantidad
        total de hogares de esa región. """

    def region_str(num_region):
        """Recibe el numero de región y lo traduce a texto según lo acordado en
            el diseño de la EPH. En caso de encontrar un valor no válido, marca
            la región como "Indefinida" """
        match num_region:
            case "1":
                ans = "Gran Buenos Aires"
            case "40":
                ans = "Noroeste"
            case "41":
                ans = "Noreste"
            case "42":
                ans = "Cuyo"
            case "43":
                ans = "Pampeana"
            case "44":
                ans = "Patagonia"
            case _:
                ans = "Indefinida"
        return ans

    try:
        with hogar_path.open("r", encoding = "utf-8") as file:
            csv_reader = csv.DictReader(file, delimiter = ";")
            header = csv_reader.fieldnames

            if header is None:
                # archivo vacio
                raise ErrorValue
            
            if not({"REGION","II7","PONDERA"}.issubset(header)):
                raise KeyError
            
            # data_hogar[region]: [cant_hogares_totales, cant_inquilinos]
            data_hogar = {}
            
            for row in csv_reader:
                region = row["REGION"]
                
                if(row["PONDERA"].isnumeric()):
                    # si no está cargada la región, la agrego
                    if not region in data_hogar:
                        data_hogar[region] = [0, 0] 

                    # guardo hogares totales
                    data_hogar[region][0] += int(row["PONDERA"])
                    # guardo inquilinos
                    if(row["II7"] == "3"):
                        data_hogar[region][1] += int(row["PONDERA"])

    except FileNotFoundError:
        print(f"Error: el archivo no fue encontrado")
    except PermissionError:
        print(f"Error: permiso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    except KeyError:
        print(f"Error de formato: faltan una o más columnas para el procesamiento")
    else:
        # ordeno en orden descendente según porcentaje
        data_hogar = dict(sorted(data_hogar.items(), key = lambda item: 
                         (float(item[1][1]*100)/float(item[1][0])), reverse = True))
        
        print("Regiones en orden según % de inquilinos")
        # Imprimo los datos ya ordenados
        for region in data_hogar:
            print(f"{region_str(region)}. ({(float(data_hogar[region][1]*100)/
            float(data_hogar[region][0]))}%)")
                

def jubilados_condicion_habitabilidad_insuficiente(hogar_path: Path, individual_path: Path):
    """ Informa, a partir de la información del último trimestre almacenado
        en el sistema (que se encuentra tanto en el csv de individuos como en el
        de hogares), una lista que para cada aglomerado indica el porcentaje
        de jubilados que viven en una vivienda con CONDICION_DE_HABITABILIDAD 
        insuficiente.
    """
    def generar_pares(anio_trimestre):
        """Recibe el diccionario de años y trimestres y devuelve una lista de tuplas (año, trimestre) 
        respetando el orden de la estructura original"""
        ans = []
        for anio in anio_trimestre:
            for trimestre in anio_trimestre[anio]:
                ans.append((anio,trimestre))
        return ans

    try:
        # abro los json para buscar el año y trimestre
        ruta_json_individual = DATA_OUT_PATH / 'estructura_individuos.json'
        ruta_json_hogar = DATA_OUT_PATH / 'estructura_hogares.json'
        with open(ruta_json_hogar,'r') as json_hogar, open(ruta_json_individual,'r') as json_individual:
            anio_trimestre_individual = json.load(json_individual)
            anio_trimestre_hogar = json.load(json_hogar)

        # genero dos listas de tuplas (año,trimestre) ordenadas descendentemente aprovechando el orden de los json      
        pares_individual = generar_pares(anio_trimestre_individual)
        pares_hogar = generar_pares(anio_trimestre_hogar)

        # busco la primera coincidencia entre los elementos de las listas 
        coincidencia = False
        for fecha in pares_individual:
            if fecha in pares_hogar:
                coincidencia = True
                anio = fecha[0]
                trimestre = fecha[1]
                break

        # si no encuentro un archivo hogar e individual del mismo trimestre,
        # no se pueden generar los datos
        if not(coincidencia):
            raise KeyError
        
        # abro los csv y genero los readers
        file_hogar = open(hogar_path,"r",encoding="utf-8")
        file_individual = open(individual_path,"r",encoding="utf-8")
        
        reader_h = csv.DictReader(file_hogar, delimiter=";")
        reader_i = csv.DictReader(file_individual, delimiter=";")
        
        header_h = reader_h.fieldnames
        header_i = reader_i.fieldnames

        # compruebo que los archivos no estén vacíos
        if((header_h is None) or (header_i is None)):
            raise ValueError

        # compruebo que existan todas las columnas que necesito
        if not({"ANO4","TRIMESTRE","PONDERA","CODUSU","ESTADO",
                "CAT_INAC"}.issubset(header_i)):
            raise KeyError

        if not({"ANO4","TRIMESTRE","PONDERA","CODUSU","AGLOMERADO",
                "CONDICION_DE_HABITABILIDAD"}.issubset(header_h)):
            raise KeyError
        
        # genero iteradores a las filas del año y trimestre a analizar
        filas_csv_hogar = filter(lambda fila : fila["ANO4"]==str(anio) and fila["TRIMESTRE"]==str(trimestre), reader_h)
        filas_csv_individual = filter(lambda fila : fila["ANO4"]==str(anio) and fila["TRIMESTRE"]==str(trimestre), reader_i)

        
        # guarda para cada CODUSU perteneciente a jubilados, la cantidad de jubilados (ponderacion)
        data_jubilados = {}
        for fila in filas_csv_individual:
            # compruebo si son jubilados y guardo la informacion en el diccionario
            if(fila["ESTADO"]=="3" and fila["CAT_INAC"] == "1" and fila["PONDERA"].isnumeric()):
                data_jubilados[fila["CODUSU"]] = int(fila["PONDERA"])

        file_individual.close()

        # guarda para cada nro de aglomerado, una lista con la cantidad total de
        # jubilados y la cantidad de jubilados con condicion de habitabilidad insuficiente
        jubilados_por_aglomerado = {}
        for fila in filas_csv_hogar:
            if(fila["CODUSU"] in data_jubilados and fila["PONDERA"].isnumeric()):
                cod = fila["CODUSU"]
                aglomerado = fila["AGLOMERADO"]
                ponderacion = int(fila["PONDERA"])

                # si todavía no se cargó informacion del aglomerado, lo agrego
                if not(aglomerado in jubilados_por_aglomerado):
                    jubilados_por_aglomerado[aglomerado] = [0,0]  
            
                # sumo al total de jubilados
                jubilados_por_aglomerado[aglomerado][0] += data_jubilados[cod] * ponderacion

                # sumo a la cant de jubilados con condicion insuficiente
                if(fila["CONDICION_DE_HABITABILIDAD"]=="insuficiente"):
                    jubilados_por_aglomerado[aglomerado][1] += data_jubilados[cod] * ponderacion

        file_hogar.close()

    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura al archivo denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    except KeyError:
        print(f"Error: faltan datos para el procesamiento")
    except Exception as e:
        print(f"Error: {e}")
    else:
        #imprimo el porcentaje para cada aglomerado
      #  print(data_jubilados)
        print(f"Porcentaje de jubilados con condicion de habitabilidad insuficiente según región ("
              f"año: {anio}, trimestre: {trimestre})")
        for nro_aglomerado in diccionario_aglomerados:
            if not(nro_aglomerado in jubilados_por_aglomerado):
                print(f"{diccionario_aglomerados[nro_aglomerado]}: sin datos")
            else:
                # porcentaje = condicion_insuficiente*100 / total
                porcentaje = (jubilados_por_aglomerado[nro_aglomerado][1]*100)/(jubilados_por_aglomerado[nro_aglomerado][0])
                print(f"{diccionario_aglomerados[nro_aglomerado]}: {porcentaje}%")
