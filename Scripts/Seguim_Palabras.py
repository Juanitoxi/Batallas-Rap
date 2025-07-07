import pandas as pd
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams

#Revisar si quitamos o no las STOPWORDS
#En general es la joyita de la corona


# Set the font family and other adjustments for plots
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['text.color'] = 'black'

def load_text_file():
    # Ask the user to select the text file
    root = Tk()
    root.withdraw()  # Hide the main window
    selected_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    root.destroy()

    if not selected_file:
        print("No file was selected.")
        return None

    try:
        with open(selected_file, 'r', encoding="utf-8") as file:
            return file.read().lower().strip()
    except Exception as e:
        print(f"Error loading the file: {e}")
        return None

def get_target_ngrams():
    # Solicitar al usuario que ingrese un bigrama
    bigram = input("Ingrese un bigrama (Ejemplo: YO SOY): ").lower()

    # Solicitar al usuario que ingrese dos palabras
    word_1 = input("Ingrese la primera palabra objetivo: ").lower()
    word_2 = input("Ingrese la segunda palabra objetivo: ").lower()

    return bigram, word_1, word_2

def plot_target_ngrams(text, target_ngrams):
    tokenized_words = [word for word in word_tokenize(text) if word.isalpha()]
    tokenized_bigrams = list(bigrams(tokenized_words))

    # Obtener los índices del bigrama
    bigram_indices = [i for i, bigram in enumerate(tokenized_bigrams) if bigram == tuple(target_ngrams[0].split())]

    # Obtener los índices de las dos palabras
    next_word_indices = [[i for i, word in enumerate(tokenized_words) if word == target] for target in target_ngrams[1:]]

    plt.figure(figsize=(12, 2))  # Reducir la altura de la figura

    # Plotear puntos para el bigrama
    if bigram_indices:
        plt.scatter(bigram_indices, [2] * len(bigram_indices), label=target_ngrams[0], s=550)

    # Plotear puntos para las dos palabras
    for i, indices in enumerate(next_word_indices):
        if indices:  # Verificar si hay ocurrencias de la palabra objetivo
            plt.scatter(indices, [1 - i] * len(indices), label=target_ngrams[i + 1], s=550)

    plt.title('Presencia de Palabras/Bigramas Objetivo a lo Largo del Texto')
    plt.xlabel('Índice de Palabra/Bigrama')
    plt.yticks([], [])  # Eliminar las etiquetas del eje Y
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    text = load_text_file()

    if not text:
        return

    target_ngrams = get_target_ngrams()
    plot_target_ngrams(text, target_ngrams)

if __name__ == "__main__":
    main()
