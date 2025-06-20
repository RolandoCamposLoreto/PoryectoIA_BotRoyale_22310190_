# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 15:01:13 2025

@author: ingro
"""

# src/utils.py

import json
import re

def load_sinonimos(path="../data/sinonimos.json"):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["sinonimos"]  # 👈 aquí sí usamos la clave "sinonimos"

def preprocess_input(text, sinonimos):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    for palabra, lista in sinonimos.items():
        for sinonimo in lista:
            if sinonimo in text:
                text = text.replace(sinonimo, palabra)
    return text
