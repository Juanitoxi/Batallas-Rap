import json

# Definir la estructura de datos
data = []

# Ruta al archivo de texto
archivo_texto = "C:\\Users\\alber\\Documents\\Personal\\Proyecto_Rap_Palabras\\TXT\\Transcripciones\\2018_Wos_VS_Aczino.txt"
                                                                                                
# Leer el archivo de texto y procesar cada línea
with open(archivo_texto, 'r', encoding='utf-8') as file:
    for line in file:
        # Separar la línea en partes utilizando ':' como separador
        partes = line.strip().split(':')

        # Extraer información de las partes
        if len(partes) == 2:
            info, texto = partes[0], partes[1]

            # Separar la información según el formato específico
            partes_info = info.split('_')

            # Verificar si la información cumple con el formato esperado
            if len(partes_info) == 4:
                año, user, round_num, formato = partes_info
                clave = f"{user}_{round_num}_{formato}"

                # Agregar la información al diccionario
                data.append({
                    'Año': año,
                    'Usuario': user,
                    'Round': round_num,
                    'Formato': formato,
                    'Texto': texto
                })

# Guardar el diccionario como JSON
archivo_json = input("Nombra a tu JSON: ")
with open(archivo_json, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

print(f"Datos convertidos y guardados en {archivo_json}")
