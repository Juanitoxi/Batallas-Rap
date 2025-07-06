import json
import subprocess

# URL del canal de YouTube
name_channel = "RedBullBatalla"
channel_url = "https://www.youtube.com/@RedBullBatalla/videos" # Reemplaza esta URL con la URL real del canal de YouTube que quieres usar

# Número de resultados que queremos
num_results = 20

# Ejecutar yt-dlp para obtener metadata de los primeros 'num_results' videos
# Usamos '--playlist-end' para limitar el número de videos
result = subprocess.run(
    ["yt-dlp", "--playlist-end", str(num_results), "-J", channel_url],
    capture_output=True,
    text=True
)

# Convertir la salida en JSON
data = json.loads(result.stdout)

# Crear un array con títulos y enlaces
video_info = [
    {
        "title": entry.get("title", "Sin título"),
        "url": entry.get("webpage_url", "")
    }
    for entry in data.get("entries", [])
]

# Guardar como archivo .json
with open(f"links_{name_channel}.json", "w", encoding="utf-8") as f:
    json.dump(video_info, f, ensure_ascii=False, indent=2)

print(f"Archivo JSON 'links_{name_channel}.json' creado con éxito con los primeros {num_results} videos.")