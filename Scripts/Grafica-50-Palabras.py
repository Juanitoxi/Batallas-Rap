from textblob import TextBlob
import pandas as pd
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter


#Este script grafica las palabras mas usadas a partir de un .TXT.
#7-7-25-6:25am estamos actualizando el script con fines de mejoras



# Download stopwords if not already downloaded
import nltk
nltk.download('stopwords')

# Load stopwords in Spanish
stop_words = set(stopwords.words('spanish'))

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
        print("No se ha selecionado ningun archivo.")
        return None

    try:
        with open(selected_file, 'r', encoding="utf-8") as file:
            return file.read().lower().strip()
    except Exception as e:
        print(f"Error al cargar archivo: {e}")
        return None

def get_sentiment(sentence):
    analysis = TextBlob(sentence)
    return analysis.sentiment.polarity

def process_text(text):
    # Tokenize sentences
    sentences = sent_tokenize(text) if text else []

    # Tokenize words and remove stopwords
    tokenized_words = [word for sentence in sentences for word in word_tokenize(sentence) if word.isalpha() and word not in stop_words]

    # Get sentiment polarity for each word
    sentiments = [get_sentiment(word) for word in tokenized_words]

    return sentiments, tokenized_words



def plot_most_frequent_words(words):
    # Count word occurrences
    word_counts = Counter(words)

    # Get the 50 most frequent words
    most_common_words = word_counts.most_common(50)

    # Separate words and their counts
    top_words, counts = zip(*most_common_words)

    # Plot the 50 most frequent words
    plt.figure(figsize=(12, 6))
    plt.bar(top_words, counts, color='blue')
    plt.title('50 Palabras Más Frecuentes en toda la batalla')
    plt.xlabel('Palabra')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def main():
    text = load_text_file()

    if not text:
        return

    sentiments, words = process_text(text)

    
    # Plot the 50 most frequent words
    plot_most_frequent_words(words)

if __name__ == "__main__":
    main()
