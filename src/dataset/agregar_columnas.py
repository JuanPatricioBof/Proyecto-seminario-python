"""Aqui encontramos las dos funciones que agregar columnas al archivo unico."""

import csv
from src.utils.constants import DATA_OUT_PATH


def generar_columnas_csv_individual():
    """Lee un CSV original y crea uno nuevo con columnas adicionales."""

    archivo_original = DATA_OUT_PATH / "usu_individual.csv"
    archivo_nuevo = DATA_OUT_PATH / "individual_process.csv"

    try:
        with archivo_original.open('r', encoding='utf-8') as entrada, \
            archivo_nuevo.open('w', newline='', encoding='utf-8') as salida:
            
            reader = csv.DictReader(entrada, delimiter=';')

            nuevas_columnas = ['CH04_str', 'NIVEL_ED_str', 'CONDICION_LABORAL', 'UNIVERSITARIO']
            nuevo_header = reader.fieldnames + nuevas_columnas
            
            writer = csv.DictWriter(salida, delimiter=';', fieldnames=nuevo_header)
            writer.writeheader()
            
            for fila in reader:
                # CH04: sexo
                fila['CH04_str'] = 'Masculino' if fila['CH04'] == '1' else 'Femenino'

                # NIVEL_ED: nivel educativo
                match fila['NIVEL_ED']:
                    case '1': fila['NIVEL_ED_str'] = "Primario incompleto"
                    case '2': fila['NIVEL_ED_str'] = "Primario completo"
                    case '3': fila['NIVEL_ED_str'] = "Secundario incompleto"
                    case '4': fila['NIVEL_ED_str'] = "Secundario completo"
                    case '5' | '6': fila['NIVEL_ED_str'] = "Superior o universitario"
                    case _: fila['NIVEL_ED_str'] = "Desconocido"

                # CONDICION_LABORAL con if/elif en vez de match
                estado = fila.get('ESTADO')
                cat_ocup = fila.get('CAT_OCUP')

                if estado == '1' and cat_ocup in ['1', '2']:
                    fila['CONDICION_LABORAL'] = 'Ocupado autónomo'
                elif estado == '1' and cat_ocup in ['3', '4', '9']:
                    fila['CONDICION_LABORAL'] = 'Ocupado dependiente'
                elif estado == '2':
                    fila['CONDICION_LABORAL'] = 'Desocupado'
                elif estado == '3':
                    fila['CONDICION_LABORAL'] = 'Inactivo'
                else:
                    fila['CONDICION_LABORAL'] = 'Sin información'

                # UNIVERSITARIO (ejemplo: 1:Sí, 0: No, 2: no aplica)            
                if int(fila['CH06']) > 60:
                    # Mayor de edad
                    if(fila["NIVEL_ED"] == "6" or (fila["CH12"] == "8" or (fila["CH12"] == "7" and fila["CH13"] == "1"))):
                        fila["UNIVERSITARIO"] = '1'  # sí
                    else:
                        fila["UNIVERSITARIO"] = '0'  # no
                else:
                    fila['UNIVERSITARIO'] = '2'
                
                writer.writerow(fila)
    except Exception as e:
        print(f'Error {e}.')


def generar_columnas_individual():
    """En esta función agrego columnas nuevas al dataset unido de individual.
    La primera columna que agrego lo hago a partir del original y el nuevo.
    El resto lo sobreescribo en el nuevo.
    """
    path_archivo_unico = DATA_OUT_PATH / "usu_individual.csv"
    path_archivo_procesado = DATA_OUT_PATH / "individual_process.csv"
    
    generar_columna_CH04_str(path_archivo_unico, path_archivo_procesado )
    generate_columna_NIVEL_ED_str(path_archivo_procesado)
    generate_columna_CONDICION_LABORAL(path_archivo_procesado)
    generar_columna_universitario_completo(path_archivo_procesado)
    
def generar_columnas_csv_hogar():
    """Lee el archivo 'usu_hogar.csv' y genera un nuevo archivo 'hogar_process.csv' con columnas adicionales, 
       las cuales son:
        - TIPO_HOGAR (Unipersonal / Nuclear / Extendido)
        - MATERIAL_TECHUMBRE (Material Precario / Material durable / No aplica)
        - DENSIDAD_HOGAR (Bajo / Medio / Alto / Desconocido)
        - CONDICION_DE_HABITABILIDAD (Insuficiente / Regular / Saludable / Buena)
        """
    
    archivo_original = DATA_OUT_PATH / 'usu_hogar.csv'
    archivo_nuevo = DATA_OUT_PATH / 'hogar_process.csv'
    try:
        with archivo_original.open('r', encoding='utf-8') as entrada, \
                archivo_nuevo.open('w', newline='', encoding='utf-8') as salida:
                reader = csv.DictReader(entrada, delimiter=';')

                nuevas_columnas = ['TIPO_HOGAR', 'MATERIAL_TECHUMBRE', 'DENSIDAD_HOGAR', 'CONDICION_DE_HABITABILIDAD']
                nuevo_header = reader.fieldnames + nuevas_columnas
                
                writer = csv.DictWriter(salida, delimiter=';', fieldnames=nuevo_header)
                writer.writeheader()
                
                for fila in reader:
                    #logica de cada columna

                    # columna TIPO_HOGAR (según la cantidad de miembros)    
                    if int(fila['IX_TOT'])==1:
                        fila['TIPO_HOGAR']='Unipersonal'
                    elif 2<= int(fila['IX_TOT'])<=4:
                        fila['TIPO_HOGAR']='Nuclear'
                    else:
                        fila['TIPO_HOGAR']='Extendido'

                    # columna MATERIAL_TECHUMBRE    
                    if fila['IV4'].strip() in ['5','6','7']:
                        fila['MATERIAL_TECHUMBRE']='Material precario'
                    elif fila['IV4'].strip() in ['1','2','3','4']:
                        fila['MATERIAL_TECHUMBRE']='Material durable'
                    elif fila['IV4'].strip()=='9':
                        fila['MATERIAL_TECHUMBRE']='No aplica'  

                    # columna DENSIDAD_HOGAR
                    miembros = fila["IX_TOT"]
                    habitaciones = fila["IV2"]
                    if(miembros.isnumeric() and habitaciones.isnumeric()):
                        miembros = int(miembros)
                        habitaciones = int(habitaciones)
                        if(miembros < habitaciones):
                            # Menos de un miembro por habitación
                            fila["DENSIDAD_HOGAR"] = "Bajo"
                        elif(miembros <= habitaciones*2):
                            # Entre 1 y 2 miembros por habitación
                            fila["DENSIDAD_HOGAR"] = "Medio"
                        else:
                            # Más de dos miembros por habitación
                            fila["DENSIDAD_HOGAR"] = "Alto"
                    else:
                        # Faltan datos o están mal cargados
                        fila["DENSIDAD_HOGAR"] = "Desconocido"

                    # columna CONDICION_DE_HABITABILIDAD
                    agua = fila['IV6']
                    origen_agua = fila['IV7']
                    tiene_banio = fila['IV8']
                    ubicacion_banio = fila['IV9']
                    desague_banio = fila['IV11']
                    piso = fila['IV3']
                    inodoro = fila['IV10']

                    fila['CONDICION_DE_HABITABILIDAD'] = clasificar_condicion_habitabilidad(agua, origen_agua, tiene_banio, ubicacion_banio, desague_banio, piso, inodoro)

                    writer.writerow(fila)
    except Exception as e:
        print(f'Error {e}.')

            

def generar_columnas_hogar():
    """En esta función agrego columnas nuevas al dataset unido hogar.
    La primera columna que agrego lo hago a partir del original y el nuevo.
    El resto lo sobreescrivo en el nuevo.
    """
    path_archivo_unico = DATA_OUT_PATH / "usu_hogar.csv"
    path_archivo_procesado = DATA_OUT_PATH / "hogar_process.csv"
    
    #llamo a funciones de agregar columnas
    generate_column_tipo_hogar(path_archivo_unico, path_archivo_procesado)    
    generate_column_material_techumbre(path_archivo_procesado)
    generar_columna_densidad_hogar(path_archivo_procesado)
    generate_column_CONDICION_DE_HABITABILIDAD(path_archivo_procesado)


# --------------Funciones para agregar columnas individuos----------------


def generar_columna_CH04_str(archivo_original, archivo_procesado):
    """Se traduce los valores CH04 numéricos a "Masculino" y "Femenino" según corresponda. El resultado se debe 
    almacenar en una nueva columna llamada CH04_str.
    Recorre el archivo original y guarda cada linea, con la nueva columna, en una variable auxliar.
    Luego abre el archivo nuevo y carga con esta variable.
       """
    try:
        # leo el contenido y genero los datos nuevos en la memoria
        with archivo_original.open('r', encoding='utf-8') as entrada:

            reader = csv.DictReader(entrada, delimiter=';')
            fieldnames = reader.fieldnames  # obtiene el encabezado
            
            if fieldnames is None:
                raise ValueError
            
            # Agrego la nueva columna si no está
            if "CH04_str" not in fieldnames:
                fieldnames.append("CH04_str")
            
            #cargo todos los datos en una lista que representan las las filas del archivo
            filas = [] 
            for row in reader:
                row['CH04_str'] = ('Masculino' if row['CH04']=='1' else 'Femenino')
                filas.append(row)

    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            # cargo los datos nuevos en el archivo nuevo de individual
            with archivo_procesado.open('w', newline = "", encoding='utf-8')as salida:
                writer = csv.DictWriter(salida, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: acceso de escritura denegado")
        else:
            print("✅ Se agregó la columna CH04_str.")


def generate_columna_NIVEL_ED_str(path_nuevo):
    """Se traduce los valores NIVEL_ED numéricos a descripciones en formato texto según las reglas especificadas.
       El resultado se debe almacenar en una nueva columna llamada NIVEL_ED_str.
    """
    try:
        # leo el contenido y genero los datos nuevos en la memoria
        with path_nuevo.open('r', encoding='utf-8') as file_csv:

            reader = csv.DictReader(file_csv, delimiter=';')
            fieldnames = reader.fieldnames
            
            if fieldnames is None:
                raise ValueError
        

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
    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            # Sobrescribir el archivo con los datos nuevos
            with path_nuevo.open('w', newline="", encoding='utf-8') as file_csv:
                writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: acceso de escritura denegado")
        else:
            print("✅Se agrego la columna NIVEL_ED_str")


def generate_columna_CONDICION_LABORAL(path_nuevo):
    """Agrega una columna llamada CONDICION_LABORAL con valores de texto según las reglas dadas."""

    try:
        with path_nuevo.open('r', encoding='utf-8') as file_csv:
            reader = csv.DictReader(file_csv, delimiter=';')
            fieldnames = reader.fieldnames

            if fieldnames is None:
                raise ValueError
            
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

    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            with path_nuevo.open('w', newline='', encoding='utf-8') as file_csv:
                writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: acceso de escritura denegado")
        else:
            print("✅Se agrega la columna CONDICION_LABORAL")


def generar_columna_universitario_completo(path_nuevo):
    """ genera una nueva columna llamada UNIVERSITARIO numérica que
    indica si una persona mayor de edad ha completado, como mínimo, el
    nivel universitario. 
    
    Los valores de la columna son:
    - "1": Sí.
    - "0": No.
    - "2": No aplica.
    - "": Indefinido (sin información suficiente).

    Para la generación se utilizan las columnas "NIVEL_ED", "CH12" y
    "CH13".

    Se considera que la persona completó el nivel universitario si
    cumple al menos una de las siguientes condiciones:
    - Su nivel educativo está registrado como universitario completo
    (valor 6 en la columna "NIVEL_ED").
    - Cursó por última vez el nivel universitario o superior (valor
    7 u 8 en la columna "CH12"), y, en caso de haber cursado por último
    el nivel universitario, completó ese nivel. (valor 7 en la columna
     "CH12" y valor 1 en la columna "CH13").

    Si la columna ya existe, actualiza los datos de la misma.
    """

    # accedo al encabezado y a las filas del archivo
    try:
        with open(path_nuevo, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file,delimiter=";")
            header = csv_reader.fieldnames
            if header is None:
                raise ValueError
                
            rows = list(csv_reader)
            
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró")
    except PermissionError:
        print(f"Error: Acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        # No hubo excepciones
        # Actualizo el encabezado
        if not "UNIVERSITARIO" in header:
            header.append("UNIVERSITARIO")

        # compruebo que el archivo contenga las columnas necesarias
        if not {"CH06", "CH12", "NIVEL_ED"}.issubset(header):
            print(f"Error: no se encontraron una o más columnas necesarias"
                    " para el procesamiento")
        else:
            # actualizo las filas
            for row in rows:
                edad = row["CH06"]
                if(edad.isnumeric()):
                    if(int(edad) >= 18):
                        if(row["NIVEL_ED"] == "6" or (row["CH12"] == "8" or
                          (row["CH12"] == "7" and row["CH13"] == "1"))):
                            row["UNIVERSITARIO"] = "1"  # sí
                        else:
                            row["UNIVERSITARIO"] = "0"  # no
                    else:
                        row["UNIVERSITARIO"] = "2"  # no aplica
                else:
                    row["UNIVERSITARIO"] = "" # indefinido

            # sobreescribo el archivo con los cambios
            try:
                with open(path_nuevo, "w", encoding="utf-8", newline = "") as file:
                    csv_writer = csv.DictWriter(file, fieldnames=header,
                                                delimiter=";")
                    csv_writer.writeheader()
                    csv_writer.writerows(rows)
            except PermissionError:
                print(f"Error. El archivo no puede ser sobreeescrito")
            else:
                print(f"✅Se agregó la columna UNIVERSITARIO_COMPLETO")


# --------------Funciones para agregar columnas hogar----------------


def generate_column_tipo_hogar(archivo_original, archivo_procesado):
    """Se debe generar una nueva columna llamada TIPO_HOGAR que indica el tipo de hogar:
    "Unipersonal" (una persona).
    "Nuclear" (2 a 4 personas).
    "Extendido" (5 o más personas)."""

    try:
        #Abrir el archivo y leer el contenido:
        with archivo_original.open('r',encoding='utf-8') as file_csv:
            reader=csv.DictReader(file_csv,delimiter=';')
            fieldnames=reader.fieldnames
            if fieldnames is None:
                raise ValueError
            
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
              
    except FileNotFoundError:
        print(f"Error: el archivo no fue encontrado") 
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        # Sobrescribir el archivo con los datos nuevos
        try:
            with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
                writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: permiso de escritura denegado")
        else:
            print("✅ Se agregó la columna tipo_hogar con valores traducidos.")
        

def generate_column_material_techumbre(archivo_procesado):
    #Se debe generar una nueva columna llamada MATERIAL_TECHUMBRE que indica el tipo de hogar basado en el campo V4:
    #- 5 a 7: "Material precario".
    #- 1 a 4: "Material durable".
    # 9: “No aplica”.
    try:
        with archivo_procesado.open('r',encoding='utf-8')as file_csv:
            reader=csv.DictReader(file_csv,delimiter=';')
            fieldnames=reader.fieldnames

            if fieldnames is None:
                raise ValueError
            
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

    except FileNotFoundError:
        print(f"Error: el archivo no fue encontrado")
    except PermissionError:
        print(f"Error: permiso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
                    writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
                    writer.writeheader()
                    writer.writerows(filas)
        except PermissionError:
            print(f"Error: el acceso de escritura denegado")
        else:
            print("✅ Se agregó la columna material_techumbre con valores traducidos.")


def generar_columna_densidad_hogar(path_copia_hogar):
    """ Genera una nueva columna denominada DENSIDAD_HOGAR según el
        siguiente criterio:

        Bajo: menos de 1 persona por habitación.
        Medio: entre 1 y 2 personas por habitación.
        Alto: más de 2 personas por habitación.
        Desconocido: información insuficiente.

        Para la generación se utilizan las columnas IX_TOT, que indica
        la cantidad total de miembros del hogar, e IV2, que indica la
        cantidad de habitaciones de la vivienda (sin contar baño/s,
        cocina, pasillo/s, lavadero, garage). En caso de faltar la
        información de alguna de las columnas o estar mal cargadas, la
        nueva columna se marca como 'Desconocido'.

        En caso de ya existir, la columna se actualiza."""
    try:
        with open(path_copia_hogar, "r", encoding="utf-8") as file:

            # Guardo el encabezado y una lista con las filas
            csv_reader = csv.DictReader(file, delimiter=";")
            header = csv_reader.fieldnames
            rows = list(csv_reader)
        
        if header is None:
            raise ValueError
    
    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso al archivo denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        # Actualizo el encabezado en caso de ser necesario
        if not "DENSIDAD_HOGAR" in header:
            header.append("DENSIDAD_HOGAR")

        # Compruebo que existan las columnas necesarias
        if not {"IX_TOT","IV2"}.issubset(header):
                print(f"Error: falta una o más columnas para el procesamiento"
                    " de los datos")
        else:
            # Actualizo las filas calculando la densidad según
            # La cantidad de miembros y habitaciones
            for row in rows:
                miembros = row["IX_TOT"]
                habitaciones = row["IV2"]
                if(miembros.isnumeric() and habitaciones.isnumeric()):
                    miembros = int(miembros)
                    habitaciones = int(habitaciones)
                    if(miembros < habitaciones):
                        row["DENSIDAD_HOGAR"] = "Bajo"
                    elif(miembros <= habitaciones*2):
                        row["DENSIDAD_HOGAR"] = "Medio"
                    else:
                        # Más de dos miembros por habitación
                        row["DENSIDAD_HOGAR"] = "Alto"
                else:
                    # Faltan datos o están mal cargados
                    row["DENSIDAD_HOGAR"] = "Desconocido"

            # Sobreescirbo el archivo con los datos actualizados
            try:
                with open(path_copia_hogar, "w", newline = "") as file:
                    csv_writer = csv.DictWriter(file, fieldnames=header, delimiter=";")
                    csv_writer.writeheader()
                    csv_writer.writerows(rows)
            except PermissionError:
                print(f"Error. Acceso de escritura denegado")
            else:
                print(f"✅ Se agregó la columna DENSIDAD_HOGAR")


def clasificar_condicion_habitabilidad(agua, origen_agua, tiene_banio, ubicacion_banio, desague_banio, piso, inodoro):
    """
    Genera la columna CONDICION_DE_HABITABILIDAD según reglas basadas en IV6, IV7, IV8, IV9, IV11 y IV3.
    Insuficiente:
    (IV6 = 3) o (IV8 = 2) o (IV11 = 4) o (IV3 ≠ 1 y 2) o (IV9 = 3) o (IV7 ≠ 1, 2 y 3).
    Regular:
    (IV6 = 2) o (IV7 = 3) o (IV9 = 2) o (IV10 = 2 y 3) o (IV11 = 2 y 3) o (IV3 ≠ 1 y 2).
    Saludable:
    (IV6 = 1 y 2) y (IV7 = 1 y 2) y (IV8 = 1) y (IV9 = 1) y (IV3 = 1 y 2) y (IV11 = 1 y 2) y (IV10 = 1)
    Buena: 
    (IV6 = 1) y (IV7 = 1) y (IV8 = 1) y (IV9 = 1) y (IV3 = 1) y (IV11 = 1) y (IV10 = 1)
    """
    # Condición BUENA
    if (agua == '1' and origen_agua == '1' and tiene_banio == '1' and
        ubicacion_banio == '1' and desague_banio == '1' and piso == '1' and inodoro == '1'):
        return 'buena'

    # Condición SALUDABLE
    elif (agua in ['1', '2'] and origen_agua in ['1', '2'] and tiene_banio == '1' and
          ubicacion_banio == '1' and desague_banio in ['1', '2'] and piso in ['1', '2'] and inodoro == '1'):
        return 'saludable'

    # Condición REGULAR
    elif ((agua == '2' or origen_agua == '3' or inodoro in ['2', '3'] or ubicacion_banio == '2' or
           desague_banio in ['2', '3'] or piso not in ['1', '2'])):
        return 'regular'

    # Condición INSUFICIENTE
    elif (agua == '3' or tiene_banio == '2' or desague_banio == '4' or
          piso not in ['1', '2'] or ubicacion_banio == '3' or origen_agua not in ['1', '2', '3']):
        return 'insuficiente'


def generate_column_CONDICION_DE_HABITABILIDAD(archivo_procesado):
    """Genera la columna CONDICION_DE_HABITABILIDAD según reglas basadas en IV6, IV7, IV8, IV9, IV11 y IV3."""
    with open(archivo_procesado, 'r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        fieldnames = reader.fieldnames

        if 'CONDICION_DE_HABITABILIDAD' not in fieldnames:
            fieldnames.append('CONDICION_DE_HABITABILIDAD')

        filas = []
        for row in reader:
            agua = row['IV6']
            origen_agua = row['IV7']
            tiene_banio = row['IV8']
            ubicacion_banio = row['IV9']
            desague_banio = row['IV11']
            piso = row['IV3']
            inodoro = row['IV10']

            row['CONDICION_DE_HABITABILIDAD'] = clasificar_condicion_habitabilidad(agua, origen_agua, tiene_banio, ubicacion_banio, desague_banio, piso, inodoro)

            filas.append(row)

    with open(archivo_procesado, 'w', newline='', encoding='utf-8') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)

    print("✅ Se agregó la columna CONDICION_DE_HABITABILIDAD.")
