# -*- coding: utf-8 -*-
# Descripción: Bot de Telegram para uso personal
# Autor: Rafael de Vega

import telebot
import os
import definitions
from telebot import types
import sqlite3

okHand = u'\U0001F44D'

bot = telebot.TeleBot(definitions.token)
users = list()
for line in open('users','r'):
    id = int(line)
    users.append(id)

@bot.message_handler(commands=['start'])
def command_hola(m):
    chat_id = m.chat.id
    name = m.from_user.first_name
    if chat_id not in users:
        bot.send_message(chat_id, definitions.welcome + name)
        users.append(chat_id)
        with open('users','a') as f:
            f.write(str(chat_id)+'\n')
    else:
        bot.send_message(chat_id, definitions.userKnow + name)

@bot.message_handler(commands=['hola'])
def command_hola(m):
    chat_id = m.chat.id
    name = m.from_user.first_name
    bot.send_message(chat_id, definitions.hello + name)

@bot.message_handler(commands=['startvnc'])
def command_startvnc(m):
    chat_id = m.chat.id
    if  chat_id == definitions.userTop or  chat_id == definitions.groupTop:
        name = m.from_user.first_name
        os.system(definitions.pathVNC)
        bot.send_message(chat_id, 'Escritorio VNC iniciado ')
    else:
        bot.send_message(chat_id, definitions.permission_denied)

@bot.message_handler(commands=['plex'])
def command_plex(m):
    chat_id = m.chat.id
    if  chat_id == definitions.userTop or  chat_id == definitions.groupTop:
        name = m.from_user.first_name
        text = m.text.split()
        option = ''
        if len(text) > 1:
            option = text[1]
        if option == 'start':
            os.system(definitions.pathPlex)
            bot.send_message(chat_id, 'He iniciado el servidor Plex')
        elif option == 'stop':
            os.system(definitions.pathPlex)
            bot.send_message(chat_id, 'He detenido el servidor Plex')
        elif option == 'restart':
            os.system(definitions.pathPlex)
            bot.send_message(chat_id, 'He reiniciado el servidor Plex')
        else:
            bot.send_message(chat_id, 'Debes enviar un comando para Plex (start, stop, restart)')
    else:
        bot.send_message(chat_id, definitions.permission_denied)

@bot.message_handler(commands=['samba'])
def command_samba(m):
    chat_id = m.chat.id
    if  chat_id == definitions.userTop or  chat_id == definitions.groupTop:
        name = m.from_user.first_name
        text = m.text.split()
        option = ''
        if len(text) > 1:
            option = text[1]
        if option == 'start':
            os.system(definitions.pathPlex)
            bot.send_message(chat_id, 'He iniciado el servidor Samba')
        elif option == 'stop':
            os.system(definitions.pathPlex)
            bot.send_message(chat_id, 'He detenido el servidor Samba')
        elif option == 'restart':
            os.system(definitions.pathPlex)
            bot.send_message(chat_id, 'He reiniciado el servidor Samba')
        else:
            bot.send_message(chat_id, 'Debes enviar un comando para Samba (start, stop, restart)')
    else:
        bot.send_message(chat_id, definitions.permission_denied)

@bot.message_handler(commands=['receipt'])
def command_receipt(m):
    chat_id = m.chat.id
    if  chat_id == definitions.userTop or  chat_id == definitions.groupTop:
        name = m.from_user.first_name
        text = m.text.split()
        option = ''
        if len(text) > 1:
            option = text[1]
    else:
        bot.send_message(chat_id, definitions.permission_denied)

# to create database:
#con = sqlite3.connect('receipts.db')
#cursor = con.cursor()
#cursor.execute("CREATE TABLE facturas (concepto TEXT, fecha TEXT , cantidad NUMERIC)")
@bot.message_handler(commands=['store'])
def command_store(m):
    chat_id = m.chat.id
    if  chat_id == definitions.userTop or  chat_id == definitions.groupTop:
        text = m.text.split()
        if len(text) != 4:
                bot.send_message(chat_id, 'Formato no válido')
        else:
            try:
                concepto = text[1]
                fecha = text[2]
                cantidad = float(text[3])
                con = sqlite3.connect('receipts.db')
                cursor = con.cursor()
                cursor.execute("INSERT INTO  facturas (concepto ,fecha ,cantidad) VALUES (?,?,?)",(concepto, fecha, cantidad))
                con.commit()
                cursor.close()
                con.close()
                bot.send_message(chat_id, 'Almacenado! '+ okHand)
            except ValueError:
                bot.send_message(chat_id, 'Revisa el formato de la cantidad. Recuerda tiene que ser un número, y si tiene decimales sepáralo con un punto')
    else:
        bot.send_message(chat_id, definitions.permission_denied)


bot.polling(none_stop = True)
