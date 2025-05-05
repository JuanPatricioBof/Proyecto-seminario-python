"""funciones para agregar columnas"""

import csv

def generar_columna_CH04_str(archivo_original, archivo_procesado):
    """Se traduce los valores CH04 numéricos a "Masculino" y "Femenino" según corresponda. El resultado se debe 
    almacenar en una nueva columna llamada CH04_str.
    Recorre el archivo original y guarda cada linea, con la nueva columna, en una variable auxliar.
    Luego abre el archivo nuevo y carga con esta variable.
       """
    # leo el contenido y genero los datos nuevos en la memoria
    with archivo_original.open('r', encoding='utf-8') as entrada:

        reader = csv.DictReader(entrada, delimiter=';')
        fieldnames = reader.fieldnames  # obtiene el encabezado
        
        # Agrego la nueva columna si no está
        if "CH04_str" not in fieldnames:
            fieldnames.append("CH04_str")
        
        #cargo todos los datos en una lista que representan las las filas del archivo
        filas = [] 
        for row in reader:
            row['CH04_str'] = ('Masculino' if row['CH04']=='1' else 'Femenino')
            filas.append(row)
    
    # cargo los datos nuevos en el archivo nuevo de invividual
    with archivo_procesado.open('w', newline = "", encoding='utf-8')as salida:
        writer = csv.DictWriter(salida, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(filas)

    print("✅ Se agregó la columna CH04_str.")

def generate_columna_NIVEL_ED_str(path_nuevo):
    """Se traduce los valores NIVEL_ED numéricos a descripciones en formato texto según las reglas especificadas.
       El resultado se debe almacenar en una nueva columna llamada NIVEL_ED_str.
    """
    # leo el contenido y genero los datos nuevos en la memoria
    with path_nuevo.open('r', encoding='utf-8') as file_csv:

        reader = csv.DictReader(file_csv, delimiter=';')
        fieldnames = reader.fieldnames

        # Agrego la nueva columna si no está
        if "NIVEL_ED_str" not in fieldnames:
            fieldnames.append("NIVEL_ED_str")
        
        filas = []  # para guardar los datos nuevos
        for row in reader:
            # Traducir los valores de NIVEL_ED
            nivel_ed = row['NIVEL_ED']
            if nivel_ed == '1':
                row['NIVEL_ED_str'] = "Primario incompleto"
            elif nivel_ed == '2':
                row['NIVEL_ED_str'] = "Primario completo"
            elif nivel_ed == '3':
                row['NIVEL_ED_str'] = "Secundario incompleto"
            elif nivel_ed == '4':
                row['NIVEL_ED_str'] = "Secundario completo"
            elif nivel_ed in ['5', '6']:
                row['NIVEL_ED_str'] = "Superior o universitario"
            else:
                row['NIVEL_ED_str'] = "Desconocido"  # Por si hay algún valor fuera de las reglas

            filas.append(row)
    
    # Sobrescribir el archivo con los datos nuevos
    with path_nuevo.open('w', newline="", encoding='utf-8') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(filas)
    print("✅ Se agrego la columna NIVEL_ED_str")



def generate_columna_CONDICION_LABORAL(path_nuevo):
    """Agrega una columna llamada CONDICION_LABORAL con valores de texto según las reglas dadas."""

    with path_nuevo.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        fieldnames = reader.fieldnames

        if "CONDICION_LABORAL" not in fieldnames:
            fieldnames.append("CONDICION_LABORAL")

        filas = []
        for row in reader:
            estado = row['ESTADO']
            cat_ocup = row['CAT_OCUP']

            if estado == '1' and cat_ocup in ('1', '2'):
                row['CONDICION_LABORAL'] = "Ocupado autónomo"
            elif estado == '1' and cat_ocup in ('3', '4', '9'):
                row['CONDICION_LABORAL'] = "Ocupado dependiente"
            elif estado == '2':
                row['CONDICION_LABORAL'] = "Desocupado"
            elif estado == '3':
                row['CONDICION_LABORAL'] = "Inactivo"
            elif estado == '4':
                row['CONDICION_LABORAL'] = "Fuera de categoría/sin información"
            else:
                row['CONDICION_LABORAL'] = "Sin información"

            filas.append(row)

    with path_nuevo.open('w', newline='', encoding='utf-8') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)
    print("✅Se agrega la columna CONDICION_LABORAL")




