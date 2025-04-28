import csv
'''Insuficiente:
    No tiene agua (IV6 = 3) o
    No tiene baño (IV8 = 2) o
    El desagüe es a hoyo en tierra (IV11 = 4).

Regular:
    Tiene agua pero fuera del terreno (IV6 = 2) o
    Agua no es de red pública (IV7 ≠ 1) o
    Baño fuera del terreno (IV9 = 3) o
    Piso de ladrillo suelto o tierra (IV3 = 3).

Saludables:
    Tiene agua dentro de la vivienda (IV6 = 1),
    Agua de red pública (IV7 = 1),
    Baño dentro de la vivienda (IV9 = 1),
    Piso de cemento/ladrillo fijo (IV3 = 2),
    Cualquier tipo de desagüe menos hoyo.

Buena:
    Igual que saludable y además desagüe a red pública (cloaca) (IV11 = 1) y piso de mosaico/madera/cerámica (IV3 = 1).
'''

def generate_column_CONDICION_DE_HABITABILIDAD(path_hogar):
    """
    Genera la columna CONDICION_DE_HABITABILIDAD según reglas basadas en IV6, IV7, IV8, IV9, IV11 y IV3.
    """

    with path_hogar.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        fieldnames = reader.fieldnames

        if "CONDICION_DE_HABITABILIDAD" not in fieldnames:
            fieldnames.append("CONDICION_DE_HABITABILIDAD")

        filas = []
        for row in reader:
            agua = row['IV6']         # 1: dentro vivienda, 2: dentro terreno, 3: fuera terreno
            origen_agua = row['IV7']  # 1: red pública, 2: bomba motor, 3: bomba manual
            tiene_banio = row['IV8']  # 1: sí, 2: no
            ubicacion_banio = row['IV9']  # 1: dentro vivienda, 2: dentro terreno, 3: fuera terreno
            desague_banio = row['IV11']   # 1: red pública, 2: cámara séptica, 3: pozo ciego, 4: hoyo
            piso = row['IV3']         # 1: piso bueno, 2: cemento, 3: tierra/ladrillo suelto
            inodoro = row ['IV10'] # 1: con boton con arrastre de agua, 2: sin boton con arrastre de agua (a balde), 3: letrina

            # Primero los casos insuficientes
            if (agua == '3' or tiene_banio == '2' or desague_banio == '4' or piso == '3'):
                row['CONDICION_DE_HABITABILIDAD'] = 'insuficiente'
            # Luego regular
            elif (agua == '2' or origen_agua in ['2', '3'] or ubicacion_banio == '3' or inodoro == 3):
                row['CONDICION_DE_HABITABILIDAD'] = 'regular'
            # Luego saludables
            elif (agua == '1' and origen_agua == '1' and ubicacion_banio == '1' and piso in ['1', '2'] and desague_banio in ['1', '2', '3']):
                row['CONDICION_DE_HABITABILIDAD'] = 'saludables'
            # Luego buena
            elif (agua == '1' and origen_agua == '1' and ubicacion_banio == '1' and desague_banio == '1' and piso == '1'):
                row['CONDICION_DE_HABITABILIDAD'] = 'buena'

            filas.append(row)

    with path_hogar.open('w', newline='', encoding='utf-8') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)

    print("✅ Se agregó la columna CONDICION_DE_HABITABILIDAD.")
