import os
from tkinter import filedialog, Tk
from moviepy.editor import VideoFileClip

# Crear una ventana emergente para que el usuario seleccione la carpeta de entrada
root = Tk()
root.withdraw()  # Ocultar la ventana principal

# Pedir al usuario que seleccione una carpeta de entrada
selected_folder = filedialog.askdirectory()
if not selected_folder:
    print("No se seleccionó ninguna carpeta de entrada.")
else:
    # Asegurarse de que la carpeta de salida exista o crearla si no existe
    output_audio_folder = 'C:\\Users\\alber\\documents\\personal\\proyecto_rap_palabras\\audio'  # Carpeta de salida para los archivos de audio
    if not os.path.exists(output_audio_folder):
        os.makedirs(output_audio_folder)

    # Recorrer los archivos de video en la carpeta seleccionada
    for filename in os.listdir(selected_folder):
        if filename.endswith(('.mkv', ".mp4")):  # Ajusta la extensión del video según tus necesidades
            video_path = os.path.join(selected_folder, filename)
            audio_path = os.path.join(output_audio_folder, os.path.splitext(filename)[0] + '.wav')

            # Abrir el video y extraer el audio en formato WAV
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio

            # Guardar el audio en el formato deseado (WAV)
            audio_clip.write_audiofile(audio_path, codec='pcm_s16le')

            print(f"Audio extraído y guardado en: {audio_path}")

    print("Proceso completado.")

root.destroy()  # Cerrar la ventana emergente
