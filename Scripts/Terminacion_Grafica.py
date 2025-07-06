import pandas as pd
from tkinter import filedialog, Tk
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict

terminations = ['ar', 'ro', 'mo', 'er', 'ir', 'or', 'al', 'ista', 'ción', 'ón', 'ble', 'aje', 'ible']



def load_text_file():
    # Lista de terminaciones a buscar
    
    # Pedir al usuario que seleccione el archivo de texto
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal
    selected_file = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    root.destroy()

    if not selected_file:
        print("No se seleccionó ningún archivo.")
        return None

    # Leer el contenido del archivo de texto
    with open(selected_file, 'r', encoding='utf-8') as file:
        # Convertir el texto a una lista de palabras
        words = file.read().lower().strip().split()
    
    # Filtrar las palabras que terminan con las terminaciones deseadas
    filtered_words = [word for word in words if any(word.endswith(termination) for termination in terminations)]

    # Crear un diccionario de frecuencias
    frequencies = defaultdict(int)
    for word in filtered_words:
        frequencies[word] += 1

    # Obtener las longitudes y terminaciones de las palabras
    word_lengths = [len(word) for word in filtered_words]
    word_terminations = [word[-2:] if len(word) >= 2 else '' for word in filtered_words]

    # Crear un DataFrame con las palabras, frecuencias, longitudes y terminaciones
    df = pd.DataFrame({
        'Palabra': filtered_words,
        'Frecuencia': [frequencies[word] for word in filtered_words],
        'Longitud': word_lengths,
        'Terminacion': word_terminations
    })

    #
    # Crear un gráfico de dispersión con Seaborn
    plt.figure(figsize=(16, 8))
    scatterplot = sns.scatterplot(x='Longitud', y='Frecuencia', hue='Terminacion', data=df, alpha=0.5, s=50)

    # Añadir texto con las terminaciones a cada punto en el gráfico
    for line in range(0, df.shape[0]):
        scatterplot.text(df['Longitud'][line], df['Frecuencia'][line], df['Terminacion'][line], 
                         horizontalalignment='center', verticalalignment='center',
                         color='black', fontsize=25, weight='bold')

    # Título y etiquetas de los ejes
    plt.title('Dispersión de Frecuencia vs Longitud de Palabras con Terminaciones')
    plt.xlabel('Longitud de Palabras')
    plt.ylabel('Frecuencia')

    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()

# Llamada a la función para cargar y visualizar el archivo
load_text_file()
