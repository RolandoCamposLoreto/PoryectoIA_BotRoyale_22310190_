# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 14:48:24 2025

@author: ingro
"""

# src/chatbot_helper.py
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_json(name):
    path = os.path.join(DATA_DIR, f"{name}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# Carga global — debe coincidir con la estructura de cada archivo JSON

intents        = load_json("intents")["intents"]           # porque tu intents.json tiene { "intents": [...] }
cards          = load_json("cards")                         # si cards.json es directamente lista []
mazos          = load_json("mazos")["mazos"]
arenas         = load_json("arenas")["arenas"]
cofres         = load_json("cofres")["cofres"]
chistes        = load_json("chistes")["chistes"]
conversaciones = load_json("conversaciones")["conversaciones"]
sinonimos      = load_json("sinonimos")["sinonimos"]
trivia         = load_json("trivia")["trivia"]
balance_changes= load_json("balance_changes")["balance_changes"]
glosario       = load_json("glosario")["glosario"]
jugadores      = load_json("jugadores")["jugadores"]
