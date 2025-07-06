import os
import tkinter as tk
from tkinter import filedialog, Scale, StringVar, OptionMenu
import pyttsx3

#con esta libreria podremos hacer variaos analisis siguiendo la logica
#como tener una lectura de un texto largo



def ajustar_velocidad(audio_path, factor):
    pass  # No es necesario ajustar la velocidad en este caso

def convertir_texto_a_voz(texto, voz_seleccionada):
    engine = pyttsx3.init()

    # Seleccionar la voz deseada
    engine.setProperty('voice', voz_seleccionada)

    # Ajustar la velocidad de reproducción (opcional)
    engine.setProperty('rate', 200)  # Ajusta la velocidad de reproducción (valor predeterminado: 200)

    engine.say(texto)
    engine.runAndWait()

def seleccionar_archivo():
    # Mostrar el cuadro de diálogo para seleccionar el archivo
    ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo de texto", filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo:
        # Actualizar la etiqueta con la ruta seleccionada
        etiqueta_ruta.config(text=ruta_archivo)
        # Leer el contenido del archivo seleccionado
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            texto = archivo.read()
        # Convertir texto a voz
        voz_seleccionada = seleccion_voz.get()  # Obtener la voz seleccionada en el menú desplegable
        convertir_texto_a_voz(texto, voz_seleccionada)

# Obtener lista de voces disponibles
def obtener_voces_disponibles():
    engine = pyttsx3.init()
    return [voice.id for voice in engine.getProperty('voices')]

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Convertir texto a voz")

# Botón para seleccionar el archivo
boton_seleccionar = tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo)
boton_seleccionar.pack(pady=100)

# Etiqueta para mostrar la ruta del archivo seleccionado
etiqueta_ruta = tk.Label(ventana, text="", wraplength=400)
etiqueta_ruta.pack()

# Obtener lista de voces disponibles
opciones_voces = obtener_voces_disponibles()

# Variable para almacenar la voz seleccionada
seleccion_voz = StringVar(ventana)
seleccion_voz.set(opciones_voces[0])  # Establecer la primera voz como predeterminada

# Menú desplegable para seleccionar la voz
menu_voces = OptionMenu(ventana, seleccion_voz, *opciones_voces)
menu_voces.pack(pady=10)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
