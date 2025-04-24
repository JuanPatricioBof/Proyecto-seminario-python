import csv
def generate_column_tipo_hogar(PATH_ARCHIVO_ORIGINAL, PATH_ARCHIVO_PROCESADO):
    #Se debe generar una nueva columna llamada TIPO_HOGAR que indica el tipo de hogar:
   #"Unipersonal" (una persona).
    #"Nuclear" (2 a 4 personas).
     #"Extendido" (5 o más personas).
#Abrir el archivo y leer el contenido:
  with PATH_ARCHIVO_ORIGINAL.open('r',encoding='utf-8') as file_csv:
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
  with PATH_ARCHIVO_PROCESADO.open('w', newline = "", encoding='utf-8')as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)
  print("✅ Se agregó la columna tipo_hogar con valores traducidos.")
    

def generate_column_material_techumbre(PATH_ARCHIVO_PROCESADO):
#Se debe generar una nueva columna llamada MATERIAL_TECHUMBRE que indica el tipo de hogar basado en el campo V4:
#- 5 a 7: "Material precario".
#- 1 a 4: "Material durable".
# 9: “No aplica”.
  with PATH_ARCHIVO_PROCESADO.open('r',encoding='utf-8')as file_csv:
    reader=csv.DictReader(file_csv,delimiter=';')
    fieldnames=reader.fieldnames

    #Se agrega la nueva columna
    if('material_techumbre') not in fieldnames:
        fieldnames.append('material_techumbre')
    filas=[]
    for row in reader:
        if row['V4'] in ['5','6','7']:
            row['material_techumbre']='Material precario'
        elif row['V4'] in ['1','2','3','4']:
            row['material_techumbre']='Material durable'
        elif row['V4']=='9':
            row['material_techumbre']='No aplica'
        filas.append(row)
  with PATH_ARCHIVO_PROCESADO.open('w', newline = "", encoding='utf-8')as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)
  print("✅ Se agregó la columna material_techumbre con valores traducidos.")
