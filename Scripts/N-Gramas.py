import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import nltk
from tkinter import filedialog, Tk

# Descargar punkt si aún no está descargado
nltk.download('punkt')

def pedir_info():
    try:
        # Pedir al usuario que seleccione el archivo de texto
        selected_file = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if not selected_file:
            print("No se seleccionó ningún archivo de texto.")
            return None

        # Cargar el archivo de texto con la transcripción de la batalla de rap
        with open(selected_file, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

def contar_ngramas(texto, n):
    try:
        # Tokenización y normalización
        palabras_filtradas = [palabra.lower() for palabra in word_tokenize(texto) if palabra.isalpha()]

        # Generar n-gramas y conteo de frecuencia
        n_gramas = list(ngrams(palabras_filtradas, n))
        frecuencia = {n_grama: n_gramas.count(n_grama) for n_grama in set(n_gramas)}

        # Crear DataFrame
        df = pd.DataFrame(list(frecuencia.items()), columns=[f'{n}-grama', 'Frecuencia'])
        df = df.sort_values(by='Frecuencia', ascending=False)
        return df
    except Exception as e:
        print(f"Error al contar n-gramas: {e}")
        return None

# Ejemplo de uso
texto_ejemplo = pedir_info()

if texto_ejemplo:
    print("\nTexto cargado exitosamente.\n")

    # Ejemplo de uso para bigramas (n=2)
    resultado_bigramas = contar_ngramas(texto_ejemplo, 2)
    if resultado_bigramas is not None:
        print("Bigramas:")
        print(resultado_bigramas)

    # Ejemplo de uso para trigramas (n=3)
    resultado_trigramas = contar_ngramas(texto_ejemplo, 3)
    if resultado_trigramas is not None:
        print("\nTrigramas:")
        print(resultado_trigramas)

    # Ejemplo de uso para 4-gramas (n=4)
    resultado_4gramas = contar_ngramas(texto_ejemplo, 4)
    if resultado_4gramas is not None:
        print("\n4-gramas:")
        print(resultado_4gramas)

    # Ejemplo de uso para 5-gramas (n=5)
    resultado_5gramas = contar_ngramas(texto_ejemplo, 5)
    if resultado_5gramas is not None:
        print("\n5-gramas:")
        print(resultado_5gramas)
