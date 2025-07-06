import os
from tkinter import filedialog, Tk
from pydub import AudioSegment


#este script separa el audio en 1.30 segundos


# Crear una ventana emergente para que el usuario seleccione la carpeta de entrada
root = Tk()
root.withdraw()  # Ocultar la ventana principal

# Pedir al usuario que seleccione una carpeta de entrada
selected_folder = filedialog.askdirectory()
if not selected_folder:
    print("No se seleccionó ninguna carpeta de entrada.")
else:
    # Asegurarse de que la carpeta de salida exista o crearla si no existe
    output_folder = 'C:\\Users\\alber\\Documents\\Personal\\Proyecto_Rap_Palabras\\Audio\\divisiones'
    os.makedirs(output_folder, exist_ok=True)

    # Iterar sobre los archivos de audio en la carpeta seleccionada
    for filename in os.listdir(selected_folder):
        if filename.endswith('.wav'):  # Ajusta la extensión del audio según tus necesidades
            input_audio_path = os.path.join(selected_folder, filename)

            # Cargar el archivo de audio
            audio = AudioSegment.from_file(input_audio_path)

            # Duración deseada para cada parte (en milisegundos)
            segment_duration = 90 * 1000  # 1 minuto y 30 segundos en milisegundos

            # Calcular la cantidad de segmentos
            num_segments = len(audio) // segment_duration

            # Iterar sobre los segmentos y guardar cada uno
            for i in range(num_segments):
                # Calcular el inicio y fin de cada segmento
                start_time = i * segment_duration
                end_time = (i + 1) * segment_duration

                # Extraer el segmento de audio
                segment = audio[start_time:end_time]

                # Guardar el segmento en un nuevo archivo
                output_filename = f'{os.path.splitext(filename)[0]}_segment_{i + 1}.wav'
                output_path = os.path.join(output_folder, output_filename)
                segment.export(output_path, format='wav')
                print(f'Segmento {i + 1} de {filename} guardado en: {output_path}')

    print("Proceso completado.")

root.destroy()  # Cerrar la ventana emergente
