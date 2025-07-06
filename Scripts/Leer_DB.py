import pandas as pd
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt
from collections import defaultdict

terminations = ['ar', 'ro', 'mo', 'er', 'ir', 'or', 'al', 'ista', 'ción', 'ón', 'ble', 'aje', 'ible']



def load_text_file():
    # Pedir al usuario que seleccione el archivo de texto
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal
    selected_file = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    root.destroy()

    if not selected_file:
        print("No se seleccionó ningún archivo.")
        return None
    
    try:
        # Leer el contenido del archivo de texto
        with open(selected_file, 'r', encoding='utf-8') as file:
            # Convertir el texto a una lista de palabras
            words = file.read().lower().strip().split()
    except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return None

    # Crear una lista de palabras limpias
    cleaned_words = [word for word in words if word.isalpha()]

    # Crear un diccionario de frecuencias
    frequencies = defaultdict(int)
    for word in cleaned_words:
        frequencies[word] += 1

    # Obtener las longitudes de las palabras
    word_lengths = [len(word) for word in cleaned_words]

    # Crear un DataFrame con las palabras, frecuencias y longitudes
    df = pd.DataFrame({'Palabra': cleaned_words, 'Frecuencia': [frequencies[word] for word in cleaned_words], 'Longitud': word_lengths})

    # Crear un gráfico de dispersión
    plt.figure(figsize=(12, 6))
    plt.scatter(df['Longitud'], df['Frecuencia'], color='#1f77b4', alpha=0.5)

    # Título y etiquetas de los ejes
    plt.title('Dispersión de Frecuencia vs Longitud de Palabras')
    plt.xlabel('Longitud de Palabras')	
    plt.ylabel('Frecuencia')

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()

# Llamada a la función para cargar y visualizar el archivo
load_text_file()