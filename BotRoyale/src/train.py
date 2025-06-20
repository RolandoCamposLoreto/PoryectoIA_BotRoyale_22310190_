# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 13:59:08 2025

@author: ingro
"""

# src/train.py

import os
import pickle
import numpy as np
import tflearn
import tensorflow as tf
from training_data import preprocess, stemmer

# Ruta base para el modelo
MODEL_PATH = "../models/model.tflearn"

# 1. Preprocesar datos
words, labels, docs_x, docs_y = preprocess()

# 2. Crear training y output
training, output = [], []
out_empty = [0] * len(labels)
for i, doc in enumerate(docs_x):
    doc_stems = [stemmer.stem(x.lower()) for x in doc]
    bag = [1 if w in doc_stems else 0 for w in words]
    row = out_empty[:]
    row[labels.index(docs_y[i])] = 1
    training.append(bag)
    output.append(row)
training = np.array(training)
output   = np.array(output)

# 3. Construir la red neuronal
tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(words)])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(labels), activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)

# 4. Intentar cargar checkpoint
loaded = False
# tflearn guarda archivos model.tflearn.*, así que comprobamos uno de ellos
if os.path.exists(MODEL_PATH + ".index"):
    try:
        model.load(MODEL_PATH)
        print("✅ Modelo cargado correctamente desde checkpoint.")
        loaded = True
    except Exception as e:
        print("⚠️ Hubo un error cargando el checkpoint:", e)
        print("   Vamos a entrenar desde cero en una sesión nueva.")

# 5. Entrenar (si no cargó) y guardar
if not loaded:
    model.fit(training, output, n_epoch=500, batch_size=8, show_metric=True)
    model.save(MODEL_PATH)
    print("✅ Modelo entrenado y guardado en", MODEL_PATH)

# 6. Guardar vocabulario y etiquetas
with open("../models/vars.pkl", "wb") as f:
    pickle.dump((words, labels), f)
print("✅ Variables (words, labels) guardadas en vars.pkl.")