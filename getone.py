import json
import subprocess
import os

# 1. URL del video específico
video_url = "https://www.youtube.com/watch?v=3lZwlJua44k&list=RDAC5m5vfFooI&index=3" # ¡Cambia esta URL por el video que te interese!
output_filename_base = " La Historia ÉPICA de las Tácticas del Fútbol " # Nombre base para el archivo de salida (sin extensión)

# Idiomas de los subtítulos a intentar descargar (puedes ajustar esto)
# Puedes usar 'es' (español), 'en' (inglés), 'auto' (generados automáticamente), etc.
subtitle_languages = "es,en,auto"

print(f"Intentando obtener transcripciones para: {video_url}")

try:
    # 2. Ejecutar yt-dlp para obtener metadata y subtítulos incrustados en JSON
    # -J: Salida en formato JSON
    # --write-subs: Descarga los subtítulos disponibles
    # --sub-langs: Especifica los idiomas de los subtítulos a descargar
    # --skip-download: No descarga el archivo de video en sí
    # --embed-subs: Intenta incrustar los subtítulos en el JSON de salida
    # NOTA: --embed-subs funciona mejor con --write-info-json, no directamente con -J para obtener el texto plano.
    # Es más fácil descargar el archivo de subtítulos y luego leerlo.

    # Vamos a cambiar el enfoque: descargar el archivo de subtítulos directamente y leerlo.
    # Esto es más confiable para obtener el texto plano.

    # Definir la ruta donde se guardará el archivo de subtítulos temporalmente
    temp_dir = "temp_subs"
    os.makedirs(temp_dir, exist_ok=True) # Crea el directorio si no existe

    # Comando para descargar los subtítulos al directorio temporal
    # --output: Define el patrón del nombre de archivo de salida
    #          '%(id)s' es el ID del video, '%(ext)s' es la extensión, '%(title)s' es el título
    #          '%(ext)s' es para la extensión del subtítulo (ej. srt, vtt)
    # --convert-subs all: Intenta convertir los subtítulos a todos los formatos disponibles (aunque aquí especificamos el preferido)
    # --sub-format vtt/srt/best: Puedes especificar un formato si lo prefieres, o dejar que yt-dlp elija 'best'.
    # Usaremos --output para controlar dónde se guardan y cómo se nombran.
    output_template = os.path.join(temp_dir, "%(title)s.%(ext)s") # Guardará como 'Título del Video.es.vtt' o .srt

    print(f"Descargando subtítulos a: {temp_dir}")
    command = [
        "yt-dlp",
        "--write-subs",
        "--sub-langs", subtitle_languages,
        "--skip-download",
        "--output", output_template,
        "--sub-format", "vtt", # Intentamos VTT porque es fácil de parsear, puedes probar 'srt'
        video_url
    ]

    # Ejecutar el comando para descargar los subtítulos
    subprocess.run(command, check=True) # 'check=True' levantará una excepción si el comando falla

    # 3. Leer y procesar el archivo de subtítulos
    # Necesitamos encontrar el archivo recién descargado.
    # yt-dlp nombra el archivo de subtítulos usando el título del video y el idioma.
    # Una forma de encontrarlo es listar los archivos en temp_dir y buscar el .vtt o .srt

    transcription_text = ""
    downloaded_subtitle_path = None

    # Primero, obtener la metadata del video para inferir el nombre del archivo de subtítulos
    # Esto es más robusto que adivinar el nombre.
    metadata_result = subprocess.run(
        ["yt-dlp", "--skip-download", "-J", video_url],
        capture_output=True,
        text=True,
        check=True
    )
    video_metadata = json.loads(metadata_result.stdout)
    video_title = video_metadata.get("title", "unknown_video_title").replace(os.sep, "_").replace("/", "_") # Limpiar el título para usarlo en nombres de archivo

    # Buscar el archivo de subtítulos en el directorio temporal
    # La extensión dependerá de lo que yt-dlp realmente descargó (vtt, srt)
    possible_extensions = ["vtt", "srt"]
    for ext in possible_extensions:
        expected_filename_pattern = f"{video_title}.{subtitle_languages.split(',')[0].strip()}.{ext}" # Intenta con el primer idioma y extensión
        downloaded_subtitle_path = os.path.join(temp_dir, expected_filename_pattern)
        if os.path.exists(downloaded_subtitle_path):
            break
        else:
            # Fallback: A veces yt-dlp guarda con 'auto' si no hay idioma específico o con el idioma exacto.
            # Podríamos buscar cualquier archivo .vtt o .srt en temp_dir que contenga el título del video.
            for fname in os.listdir(temp_dir):
                if video_title in fname and (fname.endswith(".vtt") or fname.endswith(".srt")):
                    downloaded_subtitle_path = os.path.join(temp_dir, fname)
                    break
            if downloaded_subtitle_path and os.path.exists(downloaded_subtitle_path):
                break
    
    if downloaded_subtitle_path and os.path.exists(downloaded_subtitle_path):
        print(f"Subtítulos encontrados en: {downloaded_subtitle_path}")
        with open(downloaded_subtitle_path, "r", encoding="utf-8") as f:
            subtitle_content = f.read()

        # Simple procesamiento para extraer solo el texto de VTT/SRT
        # Esto es muy básico y puede necesitar mejoras para un parsing robusto.
        lines = subtitle_content.split('\n')
        for line in lines:
            # Ignorar líneas vacías, marcas de tiempo, y metadatos VTT/SRT
            if "-->" not in line and not line.strip().isdigit() and line.strip() != "" and "WEBVTT" not in line and "Kind: captions" not in line and "Language:" not in line:
                transcription_text += line.strip() + " "
        
        # Eliminar el archivo de subtítulos temporal
        os.remove(downloaded_subtitle_path)
        os.rmdir(temp_dir) # Eliminar el directorio si está vacío
        print(f"Archivo de subtítulos temporal '{downloaded_subtitle_path}' eliminado.")

    else:
        print("No se encontraron archivos de subtítulos descargados para procesar.")
        transcription_text = "No se pudo obtener la transcripción."


    # Guardar la transcripción en un archivo de texto
    output_file_path = f"{output_filename_base}_{video_title}.txt"
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(transcription_text.strip())

    print(f"Transcripción guardada en: {output_file_path}")

except subprocess.CalledProcessError as e:
    print(f"Error al ejecutar yt-dlp: {e}")
    print(f"Salida de error de yt-dlp:\n{e.stderr}")
except FileNotFoundError:
    print("Error: 'yt-dlp' no se encontró. Asegúrate de que está instalado y en tu PATH.")
    print("Puedes instalarlo con: pip install yt-dlp")
except json.JSONDecodeError:
    print("Error: No se pudo decodificar la salida JSON de yt-dlp.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")