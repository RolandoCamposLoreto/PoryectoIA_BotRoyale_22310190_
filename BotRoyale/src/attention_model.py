# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 14:04:39 2025

@author: ingro
"""

# attention_model.py
# Modelo avanzado con LSTM + Mecanismo de Atención para un chatbot

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Attention, Bidirectional, Concatenate
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json
import pickle

# Carga los intents (asegúrate de tener intents.json con muchos ejemplos)
with open('../data/intents.json', encoding='utf-8') as f:
    data = json.load(f)

# Extrae datos
texts = []
labels = []
all_labels = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        texts.append(pattern)
        labels.append(intent['tag'])
    all_labels.append(intent['tag'])

# Tokeniza texto
tokenizer = Tokenizer(oov_token='<OOV>')
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, padding='post')

# Tokeniza etiquetas
label_tokenizer = Tokenizer()
label_tokenizer.fit_on_texts(labels)
label_seq = np.array(label_tokenizer.texts_to_sequences(labels)) - 1

# Parametros
vocab_size = len(tokenizer.word_index) + 1
output_dim = len(set(labels))
input_len = padded_sequences.shape[1]

# Define el modelo con atención
input_layer = Input(shape=(input_len,))
embedding = Embedding(input_dim=vocab_size, output_dim=64)(input_layer)
bi_lstm = Bidirectional(LSTM(64, return_sequences=True))(embedding)

# Atención
context_vector = Attention()([bi_lstm, bi_lstm])
concat = Concatenate()([context_vector, bi_lstm[:, -1, :]])
dense = Dense(64, activation='relu')(concat)
output = Dense(output_dim, activation='softmax')(dense)

model = Model(inputs=input_layer, outputs=output)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Entrena el modelo
model.fit(padded_sequences, label_seq, epochs=50, verbose=1)

# Guarda todo
model.save('../models/attention_model.keras')
with open('../models/tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
with open('../models/label_tokenizer.pkl', 'wb') as f:
    pickle.dump(label_tokenizer, f)
