# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 19:07:29 2025

@author: ingro
"""

# src/database.py
from chatbot_helper import load_json

db = {
    "intents": load_json("intents")["intents"],
    "cards": load_json("cards"),
    "mazos": load_json("mazos")["mazos"],
    "arenas": load_json("arenas")["arenas"],
    "cofres": load_json("cofres")["cofres"],
    "chistes": load_json("chistes")["chistes"],
    "conversaciones": load_json("conversaciones")["conversaciones"],
    "sinonimos": load_json("sinonimos"),
    "trivia": load_json("trivia")["trivia"],
    "balance_changes": load_json("balance_changes")["balance_changes"],
    "glosario": load_json("glosario")["glosario"],
    "jugadores": load_json("jugadores")["jugadores"],
}
