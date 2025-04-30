import csv

def generate_column_tipo_hogar(archivo_original, archivo_procesado):
    #Se debe generar una nueva columna llamada TIPO_HOGAR que indica el tipo de hogar:
    #"Unipersonal" (una persona).
    #"Nuclear" (2 a 4 personas).
    #"Extendido" (5 o más personas).
    #Abrir el archivo y leer el contenido:
    with archivo_original.open('r',encoding='utf-8') as file_csv:
        reader=csv.DictReader(file_csv,delimiter=';')
        fieldnames=reader.fieldnames

        #Se agrega la nueva columna
        if('tipo_hogar') not in fieldnames:
            fieldnames.append('tipo_hogar')
    
        filas=[]
        for row in reader:
            if int(row['IX_TOT'])==1:
                row['tipo_hogar']='Unipersonal'
            elif 2<= int(row['IX_TOT'])<=4:
                row['tipo_hogar']='Nuclear'
            else:
                row['tipo_hogar']='Extendido'
            filas.append(row)

    # Sobrescribir el archivo con los datos nuevos
    with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)
    print("✅ Se agregó la columna tipo_hogar con valores traducidos.")
    

def generate_column_material_techumbre(archivo_procesado):
    #Se debe generar una nueva columna llamada MATERIAL_TECHUMBRE que indica el tipo de hogar basado en el campo V4:
    #- 5 a 7: "Material precario".
    #- 1 a 4: "Material durable".
    # 9: “No aplica”.
    with archivo_procesado.open('r',encoding='utf-8')as file_csv:
        reader=csv.DictReader(file_csv,delimiter=';')
        fieldnames=reader.fieldnames

        #Se agrega la nueva columna
        if('material_techumbre') not in fieldnames:
            fieldnames.append('material_techumbre')
        filas=[]
        for row in reader:
            if row['IV4'].strip() in ['5','6','7']:
                row['material_techumbre']='Material precario'
            elif row['IV4'].strip() in ['1','2','3','4']:
                row['material_techumbre']='Material durable'
            elif row['IV4'].strip()=='9':
                row['material_techumbre']='No aplica'
            
            filas.append(row)
    with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(filas)
    print("✅ Se agregó la columna material_techumbre con valores traducidos.")


def generate_column_CONDICION_DE_HABITABILIDAD(archivo_procesado):
    """
    Genera la columna CONDICION_DE_HABITABILIDAD según reglas basadas en IV6, IV7, IV8, IV9, IV11 y IV3.
    Insuficiente:
    (IV6 = 3) o (IV8 = 2) o (IV11 = 4) o (IV3 ≠ 1 y 2) o (IV9 = 3) o (IV7 ≠ 1, 2 y 3).
    Regular:
    (IV6 = 2) o (IV7 = 3) o (IV9 = 2) o (IV10 = 2 y 3) o (IV11 = 2 y 3) o (IV3 ≠ 1 y 2).
    Saludables:
    (IV6 = 1 y 2) y (IV7 = 1 y 2) y (IV8 = 1) y (IV9 = 1) y (IV3 = 1 y 2) y (IV11 = 1 y 2) y (IV10 = 1)
    Buena: 
    (IV6 = 1) y (IV7 = 1) y (IV8 = 1) y (IV9 = 1) y (IV3 = 1) y (IV11 = 1) y (IV10 = 1)
    """
    with archivo_procesado.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        fieldnames = reader.fieldnames

        if ('CONDICION_DE_HABITABILIDAD') not in fieldnames:
            fieldnames.append('CONDICION_DE_HABITABILIDAD')

        filas = []
        for row in reader:
            agua = row['IV6']         # 1: dentro vivienda, 2: dentro terreno, 3: fuera terreno
            origen_agua = row['IV7']  # 1: red pública, 2: bomba motor, 3: bomba manual
            tiene_banio = row['IV8']  # 1: sí, 2: no
            ubicacion_banio = row['IV9']  # 1: dentro vivienda, 2: dentro terreno, 3: fuera terreno
            desague_banio = row['IV11']   # 1: red pública, 2: cámara séptica, 3: pozo ciego, 4: hoyo
            piso = row['IV3']         # 1: piso bueno, 2: cemento, 3: tierra/ladrillo suelto
            inodoro = row ['IV10'] # 1: con boton con arrastre de agua, 2: sin boton con arrastre de agua (a balde), 3: letrina

            # Primero los casos buena
            if (agua == '1' and origen_agua =='1' and tiene_banio == '1' and ubicacion_banio == '1' and desague_banio == '1' and piso == '1' and inodoro == '1'):
                row['CONDICION_DE_HABITABILIDAD'] = 'buena'
            # Luego saludables
            elif (agua in ['1', '2'] and origen_agua in ['1','2'] and tiene_banio =='1' and ubicacion_banio == '1' and piso in ['1', '2'] and desague_banio in ['1', '2'] and inodoro == '1'):
                row['CONDICION_DE_HABITABILIDAD'] = 'saludables'
            # Luego regular
            elif (agua == '2' or origen_agua == '3' or ubicacion_banio == '2' or inodoro in ['2', '3'] or desague_banio in  ['2', '3'] or piso not in ['1', '2']):
                row['CONDICION_DE_HABITABILIDAD'] = 'regular'            
            # Luego casos insuficientes
            elif (agua == '3' or tiene_banio == '2' or desague_banio == '4' or piso not in ['1', '2'] or ubicacion_banio == '3' or origen_agua not in ['1', '2', '3']):
                row['CONDICION_DE_HABITABILIDAD'] = 'insuficiente'

            filas.append(row)

    with archivo_procesado.open('w', newline="", encoding='utf-8') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)

    print("✅ Se agregó la columna CONDICION_DE_HABITABILIDAD.")
