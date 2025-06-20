# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 14:53:06 2025

@author: ingro
"""

# src/fetch_data.py
import requests, json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_cards():
    """Descarga la lista de cartas desde StatsRoyale (o tu API preferida)."""
    url = "https://statsroyale.com/api/v1/cards"
    resp = requests.get(url)
    resp.raise_for_status()
    cards = resp.json()
    with open(os.path.join(DATA_DIR, "cards.json"), "w", encoding="utf-8") as f:
        json.dump({"cards": cards}, f, indent=2, ensure_ascii=False)
    print(f"Guardadas {len(cards)} cartas en data/cards.json")

if __name__ == "__main__":
    fetch_cards()
