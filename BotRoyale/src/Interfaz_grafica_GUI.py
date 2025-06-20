# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 13:45:35 2025

@author: ingro
"""

import os
import tkinter as tk
from PIL import Image, ImageTk
from bot import get_response

# Configurar ventana
ventana = tk.Tk()
ventana.title("Bot Royale")
ventana.geometry("600x800")
ventana.resizable(False, False)

# Imagen de fondo (path relativo al archivo)
BASE_DIR    = os.path.dirname(__file__)          # src/
ASSETS_DIR  = os.path.normpath(os.path.join(BASE_DIR, "..", "assets"))
ruta_img    = os.path.join(ASSETS_DIR, "bg.jpg")
img         = Image.open(ruta_img).resize((600, 800))
imagen_tk   = ImageTk.PhotoImage(img)

canvas = tk.Canvas(ventana, width=600, height=800)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=imagen_tk)

# Widgets de chat
chat_log    = tk.Text(ventana, bg="#f0f8ff", fg="#000", font=("Arial", 12), wrap=tk.WORD)
chat_log.config(state=tk.DISABLED)
entrada     = tk.Entry(ventana, width=65, font=("Arial", 12))
boton_env   = tk.Button(ventana, text="Enviar", font=("Arial", 10, "bold"), command=lambda: enviar())

canvas.create_window(300, 300, window=chat_log, width=500, height=350)
canvas.create_window(300, 680, window=entrada)
canvas.create_window(300, 720, window=boton_env)

def enviar():
    user_input = entrada.get().strip()
    if not user_input:
        return
    entrada.delete(0, tk.END)

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"Tú: {user_input}\n")

    respuesta = get_response(user_input)
    chat_log.insert(tk.END, f"Bot Royale: {respuesta}\n\n")
    chat_log.see(tk.END)
    chat_log.config(state=tk.DISABLED)

# Enviar también al presionar Enter
entrada.bind("<Return>", lambda event: enviar())

ventana.mainloop()
