
import pandas as pd
import re
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt
from collections import defaultdict
from nltk.tokenize import word_tokenize
import spacy



#PENDIENTE
#Hay que mejorar este script  porque los pasteles y las barras funcionan 
#pero hay que darle el buen enfoque y uso

# Load the Spanish language model from SpaCy
nlp = spacy.load("es_core_news_sm")

# Map POS tags from SpaCy to Spanish
pos_mapping = {
    'ADJ': 'Adjetivo',
    'ADP': 'Adposición',
    'ADV': 'Adverbio',
    'AUX': 'Verbo auxiliar',
    'CONJ': 'Conjunción',
    'CCONJ': 'Conjunción de coordinación',
    'DET': 'Determinante',
    'INTJ': 'Interjección',
    'NOUN': 'Sustantivo',
    'NUM': 'Número',
    'PART': 'Partícula',
    'PRON': 'Pronombre',
    'PROPN': 'Nombre propio',
    'PUNCT': 'Puntuación',
    'SCONJ': 'Conjunción subordinada',
    'SYM': 'Símbolo',
    'VERB': 'Verbo',
    'X': 'Otros',
}

# Set the font family and other adjustments for plots
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['text.color'] = 'black'


def load_text_file():
    # Ask the user to select the text file
    root = Tk()
    root.withdraw() # Hide the main window
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


def clean_text(text):
    # Perform a more thorough cleaning of the words
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

def get_pos_tags(text):
    # Use SpaCy to obtain the grammatical tags
    doc = nlp(text)
    pos_tags = [pos_mapping.get(token.pos_, token.pos_) for token in doc]
    return pos_tags


def plot_most_common_words_with_pos(words, frequencies, pos_tags, title):
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(words)), frequencies, color='#1f77b4')
    plt.title(title)
    plt.xlabel('Word')
    plt.ylabel('Frequency')

    for i, (word, freq, pos_tag) in enumerate(zip(words, frequencies, pos_tags)):
        plt.text(i, freq + 0.1, f"{pos_tag}", ha='center', va='bottom', rotation=45, color='black')

    plt.legend(['Words'])
    plt.xticks(range(len(words)), words, rotation=45)


def plot_most_common_terminations(terminations, frequencies):
    plt.figure(figsize=(8, 8))
    plt.pie(frequencies, labels=terminations, autopct='%1.1f%%')
    plt.title('The 5 words with the highest percentages')


def main():
    # Load the content of the text file
    text = load_text_file()

    if not text:
        return

    # Obtain grammatical tags with SpaCy
    pos_tags = get_pos_tags(text)
    # Advanced tokenization
    words = word_tokenize(text)

    # Clean the words
    cleaned_words = [word for word in words if len(word) >= 4]

    # Create a dictionary to store the frequencies of the words
    word_frequencies = defaultdict(int)

    # Iterate over the words in the text file
    for word in cleaned_words:
        word_frequencies[word] += 1

    # Get the 10 most repeated words
    most_common_words = sorted(word_frequencies, key=word_frequencies.get, reverse=True)[:10]
    word_frequencies_values = [word_frequencies[word] for word in most_common_words]

    # Create a bar chart for the 10 most repeated words with grammatical tags
    plot_most_common_words_with_pos(most_common_words, word_frequencies_values, pos_tags, 'The 10 most repeated words')

    # Rest of the code...

    # Create a dictionary to store the frequencies of the terminations
    termination_frequencies = defaultdict(int)

    # Iterate over the words in the text file
    for word in cleaned_words:
        # Get the termination of the word
        termination = re.findall(r'[^\s]+$', word)[0]
        termination_frequencies[termination] += 1

    # Get the 5 most used terminations
    most_common_terminations = sorted(termination_frequencies, key=termination_frequencies.get, reverse=True)[:5]
    termination_frequencies_values = [termination_frequencies[termination] for termination in most_common_terminations]

    # Create a pie chart for the 5 most used terminations
    plot_most_common_terminations(most_common_terminations, termination_frequencies_values)

    # Create a dictionary to store the frequencies of the words
    frequencies = dict()

    # Ask the user to enter a word
    word_to_search = input("Enter the word you want to search for: ")

    # Create a scatter plot graph that only shows the searched word
    plt.figure(figsize=(10, 6))
    for i, word in enumerate(cleaned_words):
        if word_to_search == word:
            plt.scatter(i, word_frequencies[word], color='#1f77b4')
    plt.title('Frequency of the word "{}"'.format(word_to_search))
    plt.xlabel('Words')

    plt.show()
    plt.show()
    plt.show()


if __name__ == "__main__":
    main()
#
#This code has been updated with proper commenting to make it easier to understand. Comments should be clear and concise. Staying focused is very important for your career.