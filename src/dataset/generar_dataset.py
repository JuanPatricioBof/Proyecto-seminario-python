import csv
import json
from pathlib import Path
from src.utils.constants import DATA_PATH, DATA_OUT_PATH


def leer_eph(path_archivo: Path):
    """Función generadora que lee lée los eph"""

    archivo_eph = path_archivo.open('r', encoding='utf-8')
    reader = csv.DictReader(archivo_eph, delimiter=';')
    try:
        for registro in reader:
            yield registro
    except Exception as e:
        raise Exception(f"Problemas con el generador del archivo {path_archivo.name}: {e}")
    finally:
        archivo_eph.close()


def verificar_anio_trimestre(path_archivo: Path, anio, trimestre) -> bool:
    """Consulta en el json si el archivo fue agregado al dataset único"""

    info_anio_trimestre = {}
    existe_anio_trimestre = False
    try:
        with path_archivo.open('r', encoding='utf-8') as archivo:
            info_anio_trimestre = json.load(archivo)
            if anio in info_anio_trimestre:
                if trimestre in info_anio_trimestre[anio]:
                    existe_anio_trimestre = True
                else:
                    info_anio_trimestre[anio].append(trimestre)
            else:
                info_anio_trimestre[anio] = [trimestre]
    except FileNotFoundError:
        info_anio_trimestre = {anio: [trimestre]}
    finally:
        try:
            # Ordenar JSON
            info_anio_trimestre = {
                anio: sorted(trimestres, key=int, reverse=True)
                for anio, trimestres in sorted(info_anio_trimestre.items(), key=lambda x: -int(x[0]))
            }
            # Guardar JSON actualizado
            with path_archivo.open('w', encoding='utf-8') as archivo:
                json.dump(info_anio_trimestre, archivo, indent=2)
        except Exception as e:
            raise Exception(f"Error al escribir en el archivo {path_archivo.name}: {e}")

    return existe_anio_trimestre # FIX: No agregar el año y trimestre si no existe hasta que el recorrido de la eph finalice OK


def join_data():
    """Crea dataset único de para encuesta de hogares y para encuesta de individuos.
    También crea un json para cada tipo de encuesta donde se registran los años y trimestres procesados.
    """

    path_csv = {'hogar': DATA_OUT_PATH / "usu_hogar.csv", 'individual': DATA_OUT_PATH / "usu_individual.csv"}
    path_json = {'hogar':DATA_OUT_PATH / "estructura_hogares.json", 'individual': DATA_OUT_PATH / "estructura_individuos.json"}
    patron_hogar = "hogar"
    patron_individual = ["individual","persona"]

    for path_archivo in DATA_PATH.glob(f'**/*.txt'):
        try:
            eph_actual = leer_eph(path_archivo)
        except ValueError as e:
            continue

        if patron_hogar in path_archivo.name.lower(): # TODO Cambiar
            eph_header = next(eph_actual)
            primer_registro = next(eph_actual)
            anio = primer_registro["ANO4"]
            trimestre = primer_registro["TRIMESTRE"]
            if not verificar_anio_trimestre(path_json['hogar'], anio, trimestre):
                try:
                    with path_csv['hogar'].open('a', newline='', encoding='utf-8') as f_csv_ind:
                            writer_csv = csv.DictWriter(f_csv_ind, delimiter=';', fieldnames=eph_header)
                            if f_csv_ind.tell() == 0:
                                writer_csv.writeheader()
                            writer_csv.writerow(primer_registro)
                            for registro in eph_actual:
                                writer_csv.writerow(registro)
                except Exception as e:
                    raise Exception(f"Error al escribir en el archivo {path_csv['hogar'].name}: {e}")
    
        elif any(p in path_archivo.name.lower() for p in patron_individual): # TODO Cambiar
            eph_header = next(eph_actual)
            primer_registro = next(eph_actual)
            anio = primer_registro["ANO4"]
            trimestre = primer_registro["TRIMESTRE"]
            if not verificar_anio_trimestre(path_json['individual'], anio, trimestre):
                try:
                    with path_csv['individual'].open('a', newline='', encoding='utf-8') as f_csv_ind:
                            writer_csv = csv.DictWriter(f_csv_ind, delimiter=';', fieldnames=eph_header)
                            if f_csv_ind.tell() == 0:
                                writer_csv.writeheader()

                            writer_csv.writerow(primer_registro)
                            for registro in eph_actual:
                                writer_csv.writerow(registro)
                except Exception as e:
                    raise Exception(f"Error al escribir en el archivo {path_csv['individual'].name}: {e}")

        else:
            raise ValueError(f"El archivo {path_archivo.name} no es un archivo válido de EPH.")


# def join_data():
#     """Genera archivos CSV y JSON unificados"""
#     # Configuración de paths (igual que antes)
#     path_csv_hogares = DATA_OUT_PATH / "usu_hogar.csv"
#     path_csv_individuos = DATA_OUT_PATH / "usu_individual.csv"
#     path_json_individuos = DATA_OUT_PATH / "estructura_individuos.json"
#     path_json_hogares = DATA_OUT_PATH / "estructura_hogares.json"
#     patron_nombre_individuos = "individual"
#     patron_nombre_hogares = "hogar"
#     estructura_json_individuos = defaultdict(list)
#     estructura_json_hogares = defaultdict(list)
#     encabezado_hogares = None
#     encabezado_individuos = None
#     es_nuevo_hogares = not path_csv_hogares.exists() or path_csv_hogares.stat().st_size == 0
#     es_nuevo_individuos = not path_csv_individuos.exists() or path_csv_individuos.stat().st_size == 0
#     # Procesar archivos
#     for path_archivo in DATA_PATH.glob(f'*.txt'):
#      # Chequeo estricto de encabezados
#         if patron_nombre_individuos in path_archivo.name:

#              with path_archivo.open('r', encoding='utf-8') as f:
#                 reader = csv.DictReader(f, delimiter=';')
#                 if any(h in [None, ''] for h in reader.fieldnames):
#                     continue  # Pasa al siguiente archivo
#                 # Verificacion  para el primer archivo 
#                 if encabezado_individuos is None:
#                      encabezado_individuos=reader.fieldnames
#                 # Verificación para archivos posteriores
#                 elif encabezado_individuos != reader.fieldnames:
#                     continue
#                 primera_fila=next(reader)
#                 ano=primera_fila["ANO4"]
#                 trimestre=primera_fila["TRIMESTRE"]
#                 if trimestre not in estructura_json_individuos[ano]:
#                     estructura_json_individuos[ano].append(trimestre)
#                     with open(path_csv_individuos, 'a', newline='', encoding='utf-8') as f_csv_ind:
#                          writer_csv = csv.DictWriter(f_csv_ind,delimiter=';',fieldnames=reader.fieldnames)
#                          if  es_nuevo_individuos :
#                              writer_csv.writeheader()
#                          # Escribir CSV 
#                          writer_csv.writerow(primera_fila)
#                          for fila in reader:
#                             writer_csv.writerow(fila)
                        
#         elif patron_nombre_hogares in path_archivo.name:
#             with path_archivo.open('r', encoding='utf-8') as f:
#                 reader = csv.DictReader(f, delimiter=';')
#                 if any(h in [None, ''] for h in reader.fieldnames):
#                     continue  # Pasa al siguiente archivo
#                 # Verificacion  para el primer archivo 
#                 if encabezado_hogares is None:
#                      encabezado_hogares=reader.fieldnames
#                 # Verificación para archivos posteriores
#                 elif encabezado_hogares != reader.fieldnames:
#                     continue
#                 primera_fila=next(reader)
#                 ano=primera_fila["ANO4"]
#                 trimestre=primera_fila["TRIMESTRE"]
#                 if trimestre not in estructura_json_hogares[ano]:
#                     estructura_json_hogares[ano].append(trimestre)
#                     with open(path_csv_hogares, 'a', newline='', encoding='utf-8') as f_csv_hog:
#                          writer_csv = csv.DictWriter(f_csv_hog,delimiter=';',fieldnames=reader.fieldnames)
#                          # Escribir CSV 
#                          if es_nuevo_hogares:
#                             writer_csv.writeheader()
#                          writer_csv.writerow(primera_fila)
#                          for fila in reader:
#                             writer_csv.writerow(fila)
#         else:
#             continue
#     # Escribir JSON      
#     estructura_json_individuos = {
#         año: sorted(trimestres, key=int, reverse=True)
#         for año, trimestres in sorted(estructura_json_individuos.items(), key=lambda x: -int(x[0]))
#     }
#     estructura_json_hogares = {
#         año: sorted(trimestres, key=int, reverse=True)
#         for año, trimestres in sorted(estructura_json_hogares.items(), key=lambda x: -int(x[0]))
#     }
#     with path_json_individuos.open('w', encoding='utf-8') as f:
#         json.dump(estructura_json_individuos, f, indent=2)   
#     with path_json_hogares.open('w', encoding='utf-8') as f:
#         json.dump(estructura_json_hogares, f, indent=2)
#     print(f"Archivos generados exitosamente")

