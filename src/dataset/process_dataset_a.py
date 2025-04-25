""" SECCION B : información a obtener: consultas al dataset principal del 1 al 8
"""
import csv
from utils.constants import diccionario_aglomerados
def informar_aglomerado_punto6(path_procesado):
 #Informar el nombre del  aglomerado con mayor cantidad de viviendas con más de dos ocupantes  sin baño. Informar también la cantidad de ellas.
  

 # 1. Abrir el archivo y leer el contenido:
  with path_procesado.open('r',encoding='utf-8') as file_csv:
        reader=csv.DictReader(file_csv,delimiter=';')
        fieldnames=reader.fieldnames
        #2. Inicializar un diccionario para contar las viviendas sin baño por aglomerado:
        aglomerado_contador = {}
     
        for row in reader:
            #4. Verificar si la vivienda tiene más de dos ocupantes y no tiene baño:
            if int(row['IX_TOT']) > 2 and row['IV8'] == '2':
                aglomerado = row['AGLOMERADO']
                #5. Contar la vivienda en el aglomerado correspondiente:
                if aglomerado in aglomerado_contador:
                    aglomerado_contador[aglomerado] += 1
                else:
                    aglomerado_contador[aglomerado] = 1
    #6. Encontrar el aglomerado con mayor cantidad de viviendas sin baño:
  max_aglomerado = max(aglomerado_contador, key=aglomerado_contador.get)
  max_count = aglomerado_contador[max_aglomerado]
  print(f"El aglomerado con mayor cantidad de viviendas sin baño y más de dos ocupantes es:{diccionario_aglomerados[str(max_aglomerado)]}({max_aglomerado}) con {max_count} viviendas.")
    
def informar_aglomerado_punto7(path_procesado):
#Informar para cada aglomerado el porcentaje de personas que hayan cursado al menos en nivel universitario o superior.
 personas_total={}
 personas_universitarias={}
 with path_procesado.open('r',encoding='utf-8') as file_csv:
     reader=csv.DictReader(file_csv,delimiter=';')
     for row in reader:
         aglomerado=row['AGLOMERADO']
         nivel=row['NIVEL_ED']
         if aglomerado not in personas_total:
            personas_total[aglomerado]=0
            personas_universitarias[aglomerado]=0
         
         personas_total[aglomerado]+=1
         if nivel in ['5','6']:
            personas_universitarias[aglomerado]+=1
 print("Porcentaje de personas que han cursado al menos el nivel universitario o superior por aglomerado:")
 for aglomerado in personas_total:
    porcentaje=personas_universitarias[aglomerado]/personas_total[aglomerado]*100
    nombre=diccionario_aglomerados.get(aglomerado, "Desconocido")
    print(f"{nombre}({aglomerado}): {porcentaje:.2f}%")