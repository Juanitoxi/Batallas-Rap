import os
from pydub import AudioSegment
import speech_recognition as sr
from tkinter import filedialog

# Pedir al usuario que seleccione una carpeta de entrada
selected_folder = filedialog.askdirectory()
if not selected_folder:
    print("No se seleccionó ninguna carpeta.")
    exit()

# Inicializa el reconocedor
recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000

# Solicitar al usuario que ingrese el nombre del archivo de salida
output_filename = input("Ingrese el nombre del archivo: ")

# Crea la ruta absoluta para el archivo de salida
output_path = os.path.join(
    'C:\\Users\\alber\\Documents\\cloud\\profe\\',
    output_filename + '.txt'
)

# Procesa todos los archivos de audio en la carpeta seleccionada
for filename in os.listdir(selected_folder):
    if filename.endswith(('.wav', '.mp3', '.ogg', '.flac')):  # Ajusta las extensiones según tus necesidades
        audio_path = os.path.join(selected_folder, filename)

        # Carga el archivo de audio y conviértelo a formato WAV
        audio = AudioSegment.from_file(audio_path)

        # Escucha el audio y realiza el reconocimiento de voz
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        try:
            # Realiza la transcripción del audio
            transcription = recognizer.recognize_google(audio, language="es-ES")

            # Agrega la transcripción al archivo de salida
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(f'{transcription}\n')
        except sr.UnknownValueError:
            print(f"No se pudo entender el audio en {filename}")
        except sr.RequestError as e:
            print(f"Error en la solicitud para {filename}: {e}")

# Procesa todos los archivos de texto en la carpeta seleccionada
for filename in os.listdir(selected_folder):
    if filename.endswith('.txt'):  # Ajusta la extensión según tus necesidades
        text_file_path = os.path.join(selected_folder, filename)

        # Lee el contenido del archivo de texto
        with open(text_file_path, 'r', encoding='utf-8') as text_file:
            content = text_file.read()

            # Agrega el contenido al archivo de salida
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(f'{content}\n')

print("Proceso completado.")
