"""funciones para agregar columnas"""

import csv

def generar_columna_CH04_str(path_original, path_nuevo):
    """Se traduce los valores CH04 numéricos a "Masculino" y "Femenino" según corresponda. El resultado se debe 
    almacenar en una nueva columna llamada CH04_str.
    Recorre el archivo original y guarda cada linea, con la nueva columna, en una variable auxliar.
    Luego abre el archivo nuevo y carga con esta variable.
       """
    # leo el contenido y genero los datos nuevos en la memoria
    with path_original.open('r', encoding='utf-8') as entrada:

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
    with path_nuevo.open('w', newline = "", encoding='utf-8')as salida:
        writer = csv.DictWriter(salida, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(filas)

    print("✅ Se agregó la columna CH04_str.")
    