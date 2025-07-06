import pandas as pd
from tkinter import filedialog, Tk

def imprimir_palabras(palabras_por_anio, año):
    if año in palabras_por_anio:
        print(f"Palabras del año {año}: {palabras_por_anio[año]}")
    else:
        print("Año no encontrado en el archivo.")

# Crear una ventana emergente para que el usuario seleccione el archivo
root = Tk()
root.withdraw()  # Ocultar la ventana principal

# Pedir al usuario que seleccione el archivo
archivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsm")])

# Verificar si se seleccionó un archivo
if not archivo:
    print("No se seleccionó ningún archivo.")
else:
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo)

        # Obtener la lista de nombres de las columnas (años)
        columnas = df.columns.tolist()

        
        # Crear un diccionario para almacenar las listas de palabras de cada año
        palabras_por_anio = {anio: [] for anio in columnas}

        # Iterar sobre las filas
        for index, row in df.iterrows():
            # Iterar sobre las columnas (años)
            for col in columnas:
                # Obtener el dato de la celda actual
                dato = row[col]

                # Verificar si el dato es un string (ignorar NaN)
                if isinstance(dato, str):
                    # Dividir las palabras por espacios y agregarlas a la lista correspondiente al año
                    palabras_por_anio[col].extend(dato.split())

        # Ciclo para seguir preguntando al usuario
        while True:
            # Solicitar al usuario que ingrese el año que desea imprimir
            año_a_imprimir = input("Ingresa el año que deseas imprimir (o 'exit' para salir): ")

            # Verificar si el usuario desea salir
            if año_a_imprimir.lower() == 'exit':
                break

            # Convertir la entrada del usuario a un entero y llamar a la función de impresión
            try:
                año_a_imprimir = int(año_a_imprimir)
                imprimir_palabras(palabras_por_anio, año_a_imprimir)
            except ValueError:
                print("Entrada inválida. Ingresa un año válido o 'exit' para salir.")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
