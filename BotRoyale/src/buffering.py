# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 13:56:04 2025

@author: ingro
"""

# src/buffering.py
buffer = []

def add_to_buffer(user_msg, bot_msg, max_len=5):
    buffer.append((user_msg, bot_msg))
    if len(buffer) > max_len:
        buffer.pop(0)

