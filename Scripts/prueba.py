import cv2
import os

def recortar_caras(imagen_path, guardar_path):
    imagen = cv2.imread(imagen_path)
    
    # Preprocesamiento opcional, por ejemplo, ajuste de contraste
    # imagen = cv2.convertScaleAbs(imagen, alpha=1.2, beta=10)

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Ajustar parámetros de detectMultiScale
    clasificador_cara = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    caras = clasificador_cara.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(160, 160))

    for i, (x, y, w, h) in enumerate(caras):
        # Postprocesamiento opcional, por ejemplo, ampliar la región de la cara
        # x = max(0, x - 10)
        # y = max(0, y - 10)
        # w = min(imagen.shape[1] - x, w + 20)
        # h = min(imagen.shape[0] - y, h + 20)

        cara_recortada = imagen[y:y+h, x:x+w]
        cv2.imwrite(f'{guardar_path}/cara_{i + 1}.png', cara_recortada)

# Directorio que contiene las imágenes
directorio_imagenes = 'C:\\Users\\alber\\Documents\\Personal\\Doker\\input'

# Directorio para guardar las caras recortadas
directorio_guardado = 'C:\\Users\\alber\\Documents\\Personal\\Doker\\output'

if not os.path.exists(directorio_guardado):
    os.makedirs(directorio_guardado)

for archivo in os.listdir(directorio_imagenes):
    if archivo.endswith('.jpg') or archivo.endswith('.png'):
        imagen_path = os.path.join(directorio_imagenes, archivo)
        recortar_caras(imagen_path, directorio_guardado)

print("Proceso completado.")
