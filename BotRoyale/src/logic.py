# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 13:58:04 2025

@author: ingro
"""

# src/logic.py
def check_special_commands(text):
    t = text.lower()
    if t in ["salir", "adiós", "bye"]:
        return "¡Hasta luego! Que ganes muchas partidas."
    # Puedes inyectar aquí reglas para sugerir mazos, estadísticas, etc.
    return None
