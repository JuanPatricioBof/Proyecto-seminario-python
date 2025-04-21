"""funciones para agregar columnas"""

import csv

def generate_column_CH04_str(path_individual):
    """Se traduce los valores CH04 numéricos a "Masculino" y "Femenino" según corresponda. El resultado se debe 
    almacenar en una nueva columna llamada CH04_str.
       """
    """
    Si querés modificar el archivo original, lo más seguro es:
        -Escribir en un archivo temporal.
        -Luego sobrescribir el original con ese archivo modificado.
    Pero acá lo hago sobrescribiendo sin archivo temporal, 
        -leo el contenido
        -genero el nuevo
        -abro nuevamente y lo sobreescribo
    el problema de esta forma es que no es eficiente para un archivo muy grande ya que utiliza mucha ram, 
    porque el generado lo guarda en memoria, osea en ram
    """
    # leo el contenido y genero los datos nuevos en la memoria
    with path_individual.open('r', encoding='utf-8') as file_csv:

        reader = csv.DictReader(file_csv, delimiter=';')
        fieldnames = reader.fieldnames

        # Agrego la nueva columna si no está
        if "CH04_str" not in fieldnames:
            fieldnames.append("CH04_str")
        
        filas = [] # para guargar los datos nuevos
        for row in reader:
            row['CH04_str'] = ('Masculino' if row['CH04']=='1' else 'Femenino')
            filas.append(row)
    
    # Sobrescribir el archivo con los datos nuevos
    with path_individual.open('w', newline = "", encoding='utf-8')as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(filas)

    print("✅ Se agregó la columna CH04_str con valores traducidos.")
    