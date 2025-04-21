import csv

def generate_columna_NIVEL_ED_str(path_individual):
    """Se traduce los valores NIVEL_ED numéricos a descripciones en formato texto según las reglas especificadas.
       El resultado se debe almacenar en una nueva columna llamada NIVEL_ED_str.
    """
    # leo el contenido y genero los datos nuevos en la memoria
    with path_individual.open('r', encoding='utf-8') as file_csv:

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
    with path_individual.open('w', newline="", encoding='utf-8') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(filas)

 

