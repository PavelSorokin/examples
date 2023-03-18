import os
from telebot import types
from telebot.types import KeyboardButton
from scp import msg_handler, db
def keyboard_back():

    rest = ['Назад']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    return markup

def keyboard_remove():

    markup = types.ReplyKeyboardRemove()
    return markup

def keyboard_admin():
    rest = ['Показать','Создать','Закрыть','Открыть','Удалить','Просмотреть','Кол-во проходок','Изменить вопросы']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    return markup

def keyboard_user():

    rest = ['🥳Записаться на мероприятие']
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    return markup

def keyboard_delete():

    rest = os.listdir('./lists')
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    markup.add('Назад')
    return markup

def keyboard_write():
    rest = []

    lists = os.listdir('./lists')
    for i in lists:
        if (i.startswith('close')) == False:
            l = len(i)
            i = i[:l-4]
            rest.append(i)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    markup.add('Назад')
    return markup

def keyboard_question():
    rest = db.get_question()
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(str('Вопрос '+str(i+1)+ ': ' + rest[i])) for i in range(len(rest))]
    markup.add(*row)
    markup.add('Назад')
    return markup

def keyboard_new_answer_var(new_answer_var):
    rest = new_answer_var
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    markup.add('Назад')
    return markup

def keyboard_user_answer(answer):
    rest = answer
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    row = [KeyboardButton(x) for x in rest]
    markup.add(*row)
    markup.add('Назад')
    return markup