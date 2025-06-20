# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 14:02:03 2025

@author: ingro
"""

# src/bot.py
import os
import pickle
import random
import numpy as np
import tflearn
import tensorflow as tf
import unicodedata
import re
import difflib
from nltk.stem.lancaster import LancasterStemmer
from chatbot_helper import (
    intents, cards, mazos, arenas, cofres,
    chistes, conversaciones, sinonimos,
    trivia, balance_changes, glosario, jugadores
)
from utils import preprocess_input

# Rutas absolutas
BASE_DIR   = os.path.dirname(__file__)
MODELS_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'models'))
VARS_FILE  = os.path.join(MODELS_DIR, 'vars.pkl')
MODEL_FILE = os.path.join(MODELS_DIR, 'model.tflearn')

stemmer = LancasterStemmer()

# Cargar vocabulario y etiquetas
try:
    words, labels = pickle.load(open(VARS_FILE, 'rb'))
    print(f'✔️  Cargadas vars: {len(words)} palabras, {len(labels)} etiquetas')
except Exception as e:
    print(f'⚠️  Error cargando vars.pkl: {e}')
    words, labels = [], []

# Definir arquitectura
tf.compat.v1.reset_default_graph()
net = tflearn.input_data(shape=[None, len(words)])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(labels), activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net)

# Cargar modelo
if os.path.exists(MODEL_FILE + '.index'):
    try:
        model.load(MODEL_FILE)
        print('✔️  Modelo cargado correctamente.')
    except Exception as e:
        print(f'⚠️  Error cargando modelo: {e}')
else:
    print('⚠️  No se encontró checkpoint, el modelo no está cargado.')

# Normalización de texto
def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'(.)\1+', r'\1', texto)
    return texto.strip()

# Listas y stemmer
saludos = ['hola', 'qué onda', 'que ondas', 'qué tal', 'buenas', 'hey',
           'buen día', 'buenas tardes', 'buenas noches']

last_msg = ''
current_context = ''
user_name = None

mazo_respuestas = [
    'Claro, aquí tienes un mazo que te puede funcionar bien.',
    '¡Perfecto! Te recomiendo este mazo para defensa.',
    'Aquí va un mazo que muchos usan con éxito.',
    '¿Quieres un mazo ofensivo o defensivo? Te puedo ayudar con ambos.'
]

# Funciones utilitarias
def contiene_saludo(msg: str) -> bool:
    return any(s in msg for s in saludos)

def es_risa(msg: str) -> bool:
    t = ''.join(c for c in msg.lower() if c.isalpha() or c.isspace())
    return bool(re.fullmatch(r'(j[ae]+)+', t))

def parece_aleatorio(msg: str) -> bool:
    palabras = msg.split()
    comunes = ['hola','que','qué','xd','jaja','jeje','ok','si','sí']
    if any(p in palabras for p in comunes): return False
    if len(palabras)==1 and palabras[0].isalpha() and len(palabras[0])<=6:
        return True
    for junk in ['asdf','xyz','qwerty','pelota','banana','tacos','pato','coco']:
        if junk in msg: return True
    return False

def es_confirmacion(msg: str) -> bool:
    conf = ['sí','si','claro','por favor','porfa','obvio','dale','ok','perfecto','de una']
    return any(c in msg for c in conf)

def bag_of_words(s: str) -> np.ndarray:
    stems = [stemmer.stem(w) for w in s.lower().split()]
    return np.array([1 if w in stems else 0 for w in words])

def crear_mazo_con_carta(carta_fija_nombre, cartas_disponibles, tamano_mazo=8):
    nombre = carta_fija_nombre.lower()
    fija = next((c for c in cartas_disponibles if c['nombre'].lower()==nombre), None)
    if not fija: return None
    otras = [c for c in cartas_disponibles if c['nombre'].lower()!=nombre]
    if len(otras) < tamano_mazo-1:
        return [fija['nombre']]
    mazo = [fija] + random.sample(otras, tamano_mazo-1)
    return [c['nombre'] for c in mazo]

# Lógica central
def get_response(msg: str) -> str:
    global last_msg, current_context, user_name
    msg_norm = normalizar_texto(msg)

    # Evitar repetición
    if msg_norm == last_msg:
        return 'Parece que repetiste la misma pregunta, ¿quieres que te ayude con algo específico?'
    last_msg = msg_norm

    # 0) Detectar nombre usuario
    nombre_match = re.search(r"\b(?:mi nombre es|me llamo|soy)\s+([A-Za-zÁÉÍÓÚáéíóúñÑ]+)", msg_norm)
    if nombre_match:
        user_name = nombre_match.group(1).capitalize()
        return f'¡Encantado, {user_name}! ¿En qué puedo ayudarte hoy?'

    # 1) Saludos
    if contiene_saludo(msg_norm):
        saludo = random.choice(['¡Hola!','¡Hey!','¡Buenas!'])
        base = f' {user_name},' if user_name else ''
        return f'{saludo}{base} ¿en qué puedo ayudarte hoy?'

    # 2) Te amo / Te quiero
    if msg_norm in ['te amo','te quiero']:
        return 'Y yo a ti, ciudadano promedio 😎'

    # 3) Risas
    if es_risa(msg_norm):
        return random.choice([
            '¡Me alegra que te hayas divertido! 😄',
            'Jajaja, ¡me encanta tu sentido del humor!'
        ])

    # 4) Texto aleatorio
    if parece_aleatorio(msg_norm):
        return random.choice([
            '¿Qué me estás contando? 🤨',
            'Hmm... eso no suena a Clash Royale.',
            '¿Estás jugando con el teclado o qué? 😂',
            'Eso ni el Rey Esqueleto lo entiende...',
            'Parece un hechizo mal lanzado. ¿Qué quisiste decir? 😅',
            '¿Querías escribir otra cosa, clashero?'
        ])

    # 5) Pedir mazo genérico
    if re.search(r"\b(quiero|dame|necesito) un mazo\b", msg_norm):
        current_context = 'pedido_mazo'
        base = f' {user_name},' if user_name else ''
        return f'Puedo recomendarte varios mazos según tu estilo de juego{base} ¿prefieres atacar o defender?'
    # respuesta un solo palabra "mazo"
    if re.fullmatch(r'(un )?mazo', msg_norm):
        current_context = 'pedido_mazo'
        return (f'{user_name + "," if user_name else ""} ¿Prefieres un mazo de ataque o defensa?')

    # 6) Contexto ataque/defensa
    if current_context == 'pedido_mazo':
        if 'atacar' in msg_norm or 'ataque' in msg_norm:
            current_context = ''
            elegido = random.choice([m for m in mazos if 'ofensivo' in m.get('tipo','').lower()])
            return '⚔️ ' + f'{user_name + "," if user_name else ""} aquí tienes un mazo ofensivo:\n- ' + '\n- '.join(elegido['cartas'])
        if 'defender' in msg_norm or 'defensa' in msg_norm:
            current_context = ''
            elegido = random.choice([m for m in mazos if 'defensivo' in m.get('tipo','').lower()])
            return '🛡️ ' + f'{user_name + "," if user_name else ""} aquí tienes un mazo defensivo:\n- ' + '\n- '.join(elegido['cartas'])
        return 'No entendí si prefieres atacar o defender. ¿Podrías decirlo de nuevo?'

    # 7) Mazo con carta
    m = re.search(r"mazo con (.+)", msg_norm)
    if m:
        carta = m.group(1).strip()
        gen = crear_mazo_con_carta(carta, cards)
        if gen:
            return '🧩 ' + f'{user_name + "," if user_name else ""} aquí tienes un mazo con {carta.capitalize()}:\n- ' + '\n- '.join(gen)
        return f'No encontré la carta «{carta}». ¿Quieres otro mazo?'

    # 8) Favoritos
    fav_c = re.search(r"mi carta favorita es (.+)", msg_norm)
    if fav_c:
        current_context = 'esperando_fav'
        c = fav_c.group(1).strip()
        return random.choice([
            f'¡{c.capitalize()} es una carta interesante! 😎',
            f'Vaya gusto tienes con {c}, no está nada mal 😉',
            '¿Por qué esa?',
            '¡Qué gustos, hermano! Jajaja'
        ])
    fav_j = re.search(r"mi jugador favorito es (.+)", msg_norm)
    if fav_j:
        current_context = 'esperando_fav'
        j = fav_j.group(1).strip()
        return random.choice([
            f'¡{j.capitalize()} es un jugador top! 😎',
            f'Buena elección con {j}, me cae bien 😉',
            '¿Por qué ese?',
            '¡Qué gustos, hermano! Jajaja'
        ])
    if current_context == 'esperando_fav':
        current_context = ''
        return random.choice([
            '¡Eso suena genial! Siempre es bueno tenerlo en mente.',
            'Buena razón, así se gana.',
            'Me gusta tu forma de pensar.',
            '¡Buen análisis!'
        ])

    # 9) Confirmación de sugerencia
    if current_context == 'esperando_confirmacion_mazo':
        if es_confirmacion(msg_norm):
            current_context = ''
            el = random.choice(mazos)
            return f'¡Perfecto! Aquí tienes otro mazo: {", ".join(el["cartas"])}'
        else:
            current_context = ''
            return 'Entiendo, ¿en qué más puedo ayudarte?'

    # 10) Modelo
    proc = preprocess_input(msg_norm, sinonimos)
    bow = bag_of_words(proc)
    res = model.predict([bow])[0]
    idx = np.argmax(res)
    tag = labels[idx]
    if res[idx] < 0.7:
        return 'Disculpa, no entendí bien eso. ¿Podrías reformularlo?'

    # 11) Tags específicos
    if tag == 'cartas_totales':
        return f'Hay {len(cards)} cartas en Clash Royale.'
    if tag == 'trivia':
        p = random.choice(trivia)
        return f'🤔 Trivia: {p["pregunta"]}\n✅ {p["respuesta"]}'
    if tag == 'broma_megacaballero':
        return random.choice(chistes)
    if tag == 'cambio_balance':
        cb = random.choice(balance_changes)
        return f'🔄 Cambio: {cb["carta"]} -> {cb["cambio"]}'
    if tag == 'cofres':
      cr = random.choice(cofres)
      return f"🎁 Cofre {cr['nombre']}: {cr.get('contenido', '')}"
    if tag == 'glosario':
        g = random.choice(glosario)
        return f'📖 {g["termino"]}: {g["definicion"]}'

    # Fallback
    for intent in intents:
        if intent.get('tag') == tag:
            return random.choice(intent.get('responses', []))

    return 'No estoy seguro de cómo responder eso, ¿quieres que hablemos de mazos, cartas o trucos?'


if __name__ == '__main__':
    print('Bot Royale listo. Escribe "salir" para terminar.')
    while True:
        msg = input('Tú: ').strip()
        if msg.lower() == 'salir': break
        print('Bot:', get_response(msg))
