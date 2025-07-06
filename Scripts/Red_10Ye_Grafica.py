import pandas as pd
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk import bigrams

# Configuración para la visualización de gráficos
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['text.color'] = 'black'

def load_excel_file():
    # Preguntar al usuario que seleccione el archivo Excel
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal
    archivo_excel = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsm")])
    root.destroy()

    if not archivo_excel:
        print("No se seleccionó ningún archivo.")
        return None

    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo_excel)

        # Obtener la lista de nombres de las columnas (años)
        columnas = df.columns.tolist()

       
        # Crear un diccionario para almacenar los textos por año
        textos_por_anio = {anio: "" for anio in columnas}

        # Iterar sobre las filas
        for index, row in df.iterrows():
            # Iterar sobre las columnas (años)
            for col in columnas:
                # Obtener el dato de la celda actual
                dato = row[col]

                # Verificar si el dato es un string (ignorar NaN)
                if isinstance(dato, str):
                    # Concatenar el texto de la celda actual al texto correspondiente al año
                    textos_por_anio[col] += dato.lower() + " "

        return textos_por_anio

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None

def get_target_ngrams():
    # Solicitar al usuario que ingrese un bigrama
    bigram = input("Ingrese un bigrama (Ejemplo: puerto vallarta): ").lower()

    # Solicitar al usuario que ingrese dos palabras
    word_1 = input("Ingrese la primera palabra objetivo: ").lower()
    word_2 = input("Ingrese la segunda palabra objetivo: ").lower()

    return bigram, word_1, word_2

def plot_target_ngrams(textos_por_anio, target_ngrams):
    # Listas para almacenar los conteos
    años = []
    bigram_counts = []
    word_1_counts = []
    word_2_counts = []

    # Iterar sobre los textos por año
    for año, texto in textos_por_anio.items():
        tokenized_words = [word for word in word_tokenize(texto) if word.isalpha()]
        tokenized_bigrams = list(bigrams(tokenized_words))

        # Obtener la frecuencia del bigrama y las palabras
        bigram_count = tokenized_bigrams.count(tuple(target_ngrams[0].split()))
        word_1_count = tokenized_words.count(target_ngrams[1])
        word_2_count = tokenized_words.count(target_ngrams[2])

        # Almacenar los resultados en las listas
        años.append(año)
        bigram_counts.append(bigram_count)
        word_1_counts.append(word_1_count)
        word_2_counts.append(word_2_count)

    # Configuración final
    plt.figure(figsize=(18, 9))

    # Plotear puntos para la frecuencia del bigrama y las palabras
    plt.scatter(años, bigram_counts, color='blue', label=f'{target_ngrams[0]}', s=400)
    plt.scatter(años, word_1_counts, color='green', label=f'{target_ngrams[1]}', s=400)
    plt.scatter(años, word_2_counts, color='orange', label=f'{target_ngrams[2]}', s=400)

    plt.title('Presencia de Palabras/Bigramas Objetivo a lo Largo de los Años')
    plt.xlabel('Año')
    plt.ylabel('Frecuencia')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    textos_por_anio = load_excel_file()

    if not textos_por_anio:
        return

    target_ngrams = get_target_ngrams()
    plot_target_ngrams(textos_por_anio, target_ngrams)

if __name__ == "__main__":
    main()
