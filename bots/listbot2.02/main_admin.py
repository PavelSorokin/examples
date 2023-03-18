import config as var
import telebot
import os
from telebot import custom_filters
from datetime import datetime
from art import tprint
from scp import msg_handler, keyboard, classes, db
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
from tabulate import tabulate
import datetime
def main():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    handler = RotatingFileHandler('./log/main_admin.log', maxBytes=1000000, backupCount=10)
    log_format = f"%(asctime)s | [%(levelname)s] | %(name)s | (%(filename)s).%(funcName)s(%(lineno)d) | %(message)s"
    handler.setFormatter(logging.Formatter(log_format))
    log.addHandler(handler)
    print("Listbot 2.0 ADMIN is started!")
    tprint('Listbot ADMIN')

    bot = telebot.TeleBot(var.main_admin_token, state_storage=var.state_storage)

    @bot.message_handler(commands=['help'])
    def __help(message):
        bot.send_message(message.chat.id, classes.cls_msg().msg_help() , reply_markup=keyboard.keyboard_remove())

    @bot.message_handler(commands=['start'])
    def __start(message): 
        bot.send_message(message.chat.id, classes.cls_msg().msg_start_admin(), reply_markup=keyboard.keyboard_admin())
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state="*", func=lambda message: message.text == "Назад")
    def __back_to_start(message):
        __start(message)
    
    @bot.message_handler(state=classes.create_list.name)
    def __admin_create_list(message):
        msg_handler.safes_state(bot, message, 'name')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            name = data['name']
        if msg_handler.new_list(name) == True:
            msg_handler.create_list_file(name)
            bot.send_message(message.chat.id, 'Спиcок создан: '+ name, reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Список '+ name +' существует! Удали старый из списков', reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)
    
    @bot.message_handler(state=classes.close_list.name)
    def __admin_close_list(message):
        msg_handler.safes_state(bot, message, 'name')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            doc = data['name']
            docs = open('./lists/'+doc, 'rb')
        if os.path.getsize('./lists/'+doc) == 0:
            bot.send_message(message.chat.id, 'Извини, файл пустой. Его можно только удалить.🤷‍♂️\nПопробуй заново, выбери с помощью всплывающей команды.\nНажни => /start', reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_document(message.chat.id, docs)
            bot.send_message(message.chat.id, 'Отправляю список: '+doc, reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)
            if doc.startswith('close') == False:    
                os.rename('./lists/'+doc, './lists/close_'+doc)
                db.close_list(doc[:-4])

    @bot.message_handler(state=classes.open_list.name)
    def __admin_open_list(message):
        msg_handler.safes_state(bot, message, 'name')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            doc = data['name']
        if os.path.getsize('./lists/'+doc) == 0:
            bot.send_message(message.chat.id, 'Извини, файл пустой. Его можно только удалить.🤷‍♂️\nПопробуй заново, выбери с помощью всплывающей команды.\nНажни => /start', reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Открываю список: '+doc, reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)
            if doc.startswith('close') == True:    
                os.rename('./lists/'+doc, './lists/'+doc[6:])
                db.open_list(doc[6:-4])
            

    @bot.message_handler(state=classes.read_list.name)
    def __admin_read_list(message):
        msg_handler.safes_state(bot, message, 'name')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            doc = data['name']
            docs = open('./lists/'+doc, 'rb')
        if os.path.getsize('./lists/'+doc) == 0:
            bot.send_message(message.chat.id, 'Извини, файл пустой. Его можно только удалить.🤷‍♂️\nПопробуй заново, выбери с помощью всплывающей команды.\nНажни => /start', reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_document(message.chat.id, docs)
            bot.send_message(message.chat.id, 'Отправляю список: '+doc, reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=classes.delete_list.name)
    def __admin_delete_list(message):
        msg_handler.safes_state(bot, message, 'name')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            doc = data['name']
            __list = doc[:-4]
            if doc.startswith('close') == True:
                __list =  __list[6:]
            os.remove('./lists/'+ doc)
            db.delete_list(__list)
        bot.send_message(message.chat.id, 'Список '+ doc + ' удален' , reply_markup=keyboard.keyboard_admin())
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=classes.intdeadline.name)
    def __deadline(message):
        msg_handler.safes_state(bot, message, 'name')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            name = data['name']

        if name.startswith('close') == False:
            bot.send_message(message.chat.id,'Отправь мне новое ЧИСЛО, чтобы изменить количество проходок на этом списке', reply_markup=keyboard.keyboard_back())
            bot.set_state(message.from_user.id, classes.intdeadline.deadline, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Работает только на открытых списках!', reply_markup=keyboard.keyboard_admin())
            bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=classes.intdeadline.deadline, is_digit=False)
    def __noint(message):
        bot.send_message(message.chat.id,'Введи только число, без пробелов и символов', parse_mode='Markdown', reply_markup=keyboard.keyboard_back())
        bot.set_state(message.from_user.id, classes.intdeadline.deadline, message.chat.id) 

    @bot.message_handler(state=classes.intdeadline.deadline, is_digit=True)
    def __yesint(message):  
        msg_handler.safes_state(bot, message, 'deadline')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                __name     = data['name']
                __deadline = data['deadline']   
                db.update_deadline(__name[:-4],__deadline)
                msg_nd = 'Установлено новое количество проходок\n' +__name[:-4] + ': '+ str(__deadline)
        bot.send_message(message.chat.id, msg_nd, reply_markup=keyboard.keyboard_admin())
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=classes.quest._question)
    def __quest1(message):
        msg_handler.safes_state(bot, message, '_question')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            question = data['_question']
            question = question[9:]

        bot.send_message(message.chat.id,'Отправь новый вопрос', reply_markup=keyboard.keyboard_back())
        bot.set_state(message.from_user.id, classes.quest._new_question, message.chat.id)

    @bot.message_handler(state=classes.quest._new_question)
    def __quest2(message):
        msg_handler.safes_state(bot, message, '_new_question')
        bot.send_message(message.chat.id,'А теперь отправь мне новые ответы на вопросы\nПримеры:\n1,2,3,4\nили\nЗалупа,пупа+1,какой ответ?,234', reply_markup=keyboard.keyboard_back())
        bot.set_state(message.from_user.id, classes.quest._new_answer_var, message.chat.id)
    
    @bot.message_handler(state=classes.quest._new_answer_var)
    def __quest3(message):
        msg_handler.safes_state(bot, message, '_new_answer_var')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            new_answer_var = data['_new_answer_var']
        new_answer_var = new_answer_var.split(',')
        bot.send_message(message.chat.id,'Выбери правильный ответ', reply_markup=keyboard.keyboard_new_answer_var(new_answer_var))
        bot.set_state(message.from_user.id, classes.quest._new_answer, message.chat.id)

    @bot.message_handler(state=classes.quest._new_answer)
    def __quest4(message):
        msg_handler.safes_state(bot, message, '_new_answer')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            question = data['_question']
            question = question[10:]
            id = db.get_question_id(question)
            new_question =  data['_new_question']
            new_answer_var = data['_new_answer_var']
            new_answer =  data['_new_answer']
            db.update_question(new_question,new_answer_var,new_answer,id)
        bot.send_message(message.chat.id,str('Обновил вопрос:\n'+new_question+'\nОтвет:\n'+new_answer), reply_markup=keyboard.keyboard_admin())
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state="*", func=lambda message: message.chat.id in var.admins, content_types=['text'])
    def __admin(message):
        if message.text == 'Создать':

                bot.send_message(message.chat.id, classes.cls_msg().msg_newlist(), reply_markup=keyboard.keyboard_back())
                bot.set_state(message.from_user.id, classes.create_list.name, message.chat.id)
        
        elif message.text == 'Показать':
                
                if db.get_lists() != False:
                    get_lists, headers = db.get_lists()
                    df = pd.DataFrame(get_lists)
                    df.columns = headers
                    table = tabulate(df, headers=headers, tablefmt='simple_outline', showindex=False)
                    bot.send_message(message.chat.id, f'```{table}```',parse_mode='MarkdownV2',reply_markup=keyboard.keyboard_admin())
                else:
                    bot.send_message(message.chat.id, 'Списков нет :)', reply_markup=keyboard.keyboard_admin())
        
        elif message.text == 'Кол-во проходок':

                bot.send_message(message.chat.id, 'Выбери список', reply_markup=keyboard.keyboard_delete())
                bot.set_state(message.from_user.id, classes.intdeadline.name, message.chat.id)

        elif message.text == 'Изменить вопросы':

                bot.send_message(message.chat.id, 'Выбери вопрос', reply_markup=keyboard.keyboard_question())
                bot.set_state(message.from_user.id, classes.quest._question, message.chat.id)

        elif msg_handler.empty_dir_admin() == False:

            if  message.text == 'Закрыть':

                bot.send_message(message.chat.id, 'Какой список закрыть?', reply_markup=keyboard.keyboard_delete())
                bot.set_state(message.from_user.id, classes.close_list.name, message.chat.id)
                
            elif  message.text == 'Открыть':

                bot.send_message(message.chat.id, 'Какой список открыть?', reply_markup=keyboard.keyboard_delete())
                bot.set_state(message.from_user.id, classes.open_list.name, message.chat.id)

            elif message.text == 'Просмотреть':

                bot.send_message(message.chat.id, 'Какой список ты хочешь посмотреть?', reply_markup=keyboard.keyboard_delete())
                bot.set_state(message.from_user.id, classes.read_list.name, message.chat.id)

            elif message.text == 'Удалить':
               
                bot.send_message(message.chat.id, 'Какой список удалить?', reply_markup=keyboard.keyboard_delete())
                bot.set_state(message.from_user.id, classes.delete_list.name, message.chat.id)

            else:

                bot.send_message(message.chat.id, 'Извини, я ничего не нашел. Попробуй сначала создать🤷‍♂️\nНажни => /start', reply_markup=keyboard.keyboard_admin())
                bot.delete_state(message.from_user.id, message.chat.id)
    
        else:
            __start(message)

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())

    bot.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    main()
