# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 13:55:49 2025

@author: ingro
"""
# src/training_data.py

import nltk
from nltk.stem.lancaster import LancasterStemmer
from chatbot_helper import intents, sinonimos

stemmer = LancasterStemmer()

def preprocess():
    """Devuelve (words, labels, docs_x, docs_y) listos para entrenamiento."""
    words, labels, docs_x, docs_y = [], [], [], []

    for intent in intents:
        tag = intent.get("tag")
        if not tag:
            # Ignorar entradas sin tag
            print(f"Skipping item without tag: {intent}")
            continue
        labels.append(tag)

        for pattern in intent.get("patterns", []):
            # Normaliza sinónimos
            text = pattern.lower()
            for key, variants in sinonimos.items():
                for alt in variants:
                    text = text.replace(alt, key)
            # Tokenizar
            tokens = nltk.word_tokenize(text)
            docs_x.append(tokens)
            docs_y.append(tag)
            words.extend(tokens)

    # Limpiar, stemmizar y ordenar vocabulario
    words = sorted({stemmer.stem(w.lower()) for w in words if w.isalnum()})
    labels = sorted(set(labels))

    return words, labels, docs_x, docs_y

if __name__ == "__main__":
    # Para probar rápidamente
    w, l, dx, dy = preprocess()
    print(f"Vocab size: {len(w)}, Labels: {l}")