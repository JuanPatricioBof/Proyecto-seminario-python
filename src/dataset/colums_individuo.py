import csv
from pathlib import Path

# ruta a copia provisional para testear el funcionamiento de la funcion
ruta_datos = Path().resolve().parent.parent
ruta_datos = ruta_datos / "files" / "data_eph" / "EPH_usu_3er_Trim_2024_txt" 
ruta_individual = ruta_datos / "usu_individual_T324_copia.txt"

def generar_universitario_completo(path_csv_individual):
    """ genera una nueva columna llamada UNIVERSITARIO numérica que indica si
    una persona mayor de edad ha completado el como mínimo el nivel universitario (1:
    Sí, 0: No, 2: no aplica). """

    header = []
    # re-escribo el encabezado agregando la nueva columna
    with open(path_csv_individual, "r+") as file:
        csv_reader = csv.reader(file,delimiter=";")
        header = next(csv_reader)
        if not "UNIVERSITARIO" in header:  # chequeo que no exista para evitar columnas duplicadas
            header.append("UNIVERSITARIO")
        csv_writer = csv.writer(file,delimiter=";")
        csv_writer.writerow(header) # no esta funcionando, no actualiza el encabezado

  
    # completo los datos de la nueva columna
    with open(path_csv_individual, "r+") as file:
        csv_reader = csv.DictReader(file,delimiter=";")
        csv_writer = csv.DictWriter(file,fieldnames=header,delimiter=";")  # funciona ?
        for row in csv_reader:
            actualizar = row
            print(actualizar) # debugeo
            edad = str(row["CH06"])
            if(edad.isnumeric):
                if(int(edad) >= 18):
                    if((row["CH12"] in {"7", "8"} and row["CH13"] == "1") or row["NIVEL_ED"] == "6"):
                        actualizar["UNIVERSITARIO"] = "1"
                    else:
                        actualizar["UNIVERSITARIO"] = "0"
            else:
                actualizar["UNIVERSITARIO"] = "2" # necesario pasarlo como str?
            csv_writer.writerow(actualizar)
    
    print("columna generada")

# codigo provisional para testear el funcionamiento de la funcion
print(ruta_individual)
generar_universitario_completo(ruta_individual)