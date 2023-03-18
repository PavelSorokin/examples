import config as var
import telebot
import os
from telebot import custom_filters
from datetime import datetime
from art import tprint
from scp import msg_handler, keyboard, classes, db
import logging
from logging.handlers import RotatingFileHandler
from art import tprint


def main():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    handler = RotatingFileHandler('./log/main_user.log', maxBytes=1000000, backupCount=10)
    log_format = f"%(asctime)s | [%(levelname)s] | %(name)s | (%(filename)s).%(funcName)s(%(lineno)d) | %(message)s"
    handler.setFormatter(logging.Formatter(log_format))
    log.addHandler(handler)
    print("Listbot 2.0 is started!")
    tprint('Listbot 2.0')


    bot = telebot.TeleBot(var.main_bot_token, state_storage=var.state_storage)

    @bot.message_handler(commands=['help'])
    def __help(message):
        bot.send_message(message.chat.id, 'Привет, для работы с ботом отправь /start' , reply_markup=keyboard.keyboard_remove())

    @bot.message_handler(commands=['start'])
    def __start(message):
        if message.from_user.username is None:
            bot.send_message(message.chat.id, classes.cls_msg().msg_start(''), reply_markup=keyboard.keyboard_user())
            msg_handler.new_user_func_noname(message)
        else:
            bot.send_message(message.chat.id, classes.cls_msg().msg_start(message.chat.first_name), reply_markup=keyboard.keyboard_user())
            msg_handler.new_user_func(message)
            
    @bot.message_handler(state="*", commands=['cancel'])
    def cancel_cmd(message):
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, 'Удаляем состояния, если все еще не работает отправь мне /start!', reply_markup=keyboard.keyboard_remove())


    @bot.message_handler(state="*", func=lambda message: message.text == "Назад")
    def __back_to_start(message):
        bot.delete_state(message.from_user.id, message.chat.id)
        __start(message)

    @bot.message_handler(state=classes.answer.name)
    def user_write_list(message):
        msg_handler.safes_state(bot, message, 'name')
        if  bot.get_chat_member(var.zerkalo_chat_id,message.from_user.id).status == 'left':
                bot.send_message(message.chat.id, 'Для записи в список на вход, необходимо быть подписанным на канал\nhttps://t.me/zerkalotver 🤷‍♂️\nПопробуй заново, выбери с помощью всплывающей команды.\nНажни => /start', reply_markup=keyboard.keyboard_user())
                bot.delete_state(message.from_user.id, message.chat.id)
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                name = data['name']
                lists = os.listdir('./lists')
            if name+'.txt' in lists:

                if msg_handler.check_deadline(name) < int(db.get_deadline(name)):

                    bot.send_message(message.chat.id, 'Ты готов записать на записать на мероприятие!?\nОтлично! Но для начала пройди тест⬇️')
                    msg_question_1 = db.get_question_text(1)
                    _answer1 = db.get_answer_text(1).split(',')
                    bot.send_message(message.chat.id, str(f'Вопрос 1:\n{msg_question_1}'), reply_markup=keyboard.keyboard_user_answer(_answer1))
                    bot.set_state(message.from_user.id, classes.answer.answer1, message.chat.id)
                        
                else:
                    bot.send_message(message.chat.id, 'Извини, но количество проходок закончилось.🤷‍♂️\nНажни => /start', reply_markup=keyboard.keyboard_user())
                    bot.delete_state(message.from_user.id, message.chat.id)
            else:
                    bot.send_message(message.chat.id, 'Извини, я не нашел список.🤷‍♂️\nПопробуй заново, выбери с помощью всплывающей команды.\nНажни => /start', reply_markup=keyboard.keyboard_user())
                    bot.delete_state(message.from_user.id, message.chat.id)                   
    
    @bot.message_handler(state=classes.answer.fio)
    def user_write_lists(message):
        msg_handler.safes_state(bot, message, 'fio')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            name = data['name']
            fio = data['fio']
        if msg_handler.check_deadline(name) < int(db.get_deadline(name)):
            with open('./lists/'+name+'.txt','r+') as files:
                fio = fio.replace('\n', ' ')
                my_list = [x.rstrip() for x in files]
                number = len(my_list) + 1
                files.write(str(number)+'. '+ fio+'\n')
                files.close
            bot.send_message(message.chat.id, 'Твой номер в списке: №'+str(number)+'\nПокажи его при входе' , reply_markup=keyboard.keyboard_remove())
            db.update_last_number(message.chat.id,number)
            msg_handler.update_timeout(message)
            log.info( str(message.chat.id) +' | ' + str(message.chat.username) +' | '+ str(message.chat.first_name) +' | Номер в списке: ' + str(number) )
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Извини, но количество проходок закончилось.🤷‍♂️\nНажни => /start', reply_markup=keyboard.keyboard_user())
            bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=classes.answer.answer1)
    def __answer1(message):
        msg_handler.safes_state(bot, message, 'answer1')
        msg_question_2 = db.get_question_text(2)
        _answer2 = db.get_answer_text(2).split(',')
        bot.send_message(message.chat.id, str(f'Вопрос 2:\n{msg_question_2}'), reply_markup=keyboard.keyboard_user_answer(_answer2))
        bot.set_state(message.from_user.id, classes.answer.answer2, message.chat.id)
    
    @bot.message_handler(state=classes.answer.answer2)
    def __answer2(message):
        msg_handler.safes_state(bot, message, 'answer2')
        msg_question_3 = db.get_question_text(3)
        _answer3 = db.get_answer_text(3).split(',')
        bot.send_message(message.chat.id, str(f'Вопрос 3:\n{msg_question_3}'), reply_markup=keyboard.keyboard_user_answer(_answer3))
        bot.set_state(message.from_user.id, classes.answer.answer3, message.chat.id)

    @bot.message_handler(state=classes.answer.answer3)
    def __answer3(message):
        msg_handler.safes_state(bot, message, 'answer3')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            name    = data['name']
            answer1 = data['answer1']
            answer2 = data['answer2']
            answer3 = data['answer3']
        answer_list = db.get_answer_list()
        if answer1 == answer_list[0] and answer2 == answer_list[1] and answer3 == answer_list[2]:
            bot.send_message(message.chat.id, 'Ты выбрал список: '+name+ '\nОтправь свою Фамилию и Имя, чтобы мы закрепили за тобой Номер\nЗапомни, его необходимо будет предъявить на входе🧐', reply_markup=keyboard.keyboard_remove())
            bot.set_state(message.from_user.id, classes.answer.fio, message.chat.id)
        else: 
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, 'Все плохо, ты завалил Тест 😱\nНо у тебя есть возможность попробовать снова! Вперед 💪', reply_markup=keyboard.keyboard_user())
            msg_handler.update_timeout(message)

    @bot.message_handler(state="*", func=lambda message: message.chat.type == 'private', content_types=['text'])
    def __new_user(message):
        if message.from_user.username is None:
            msg_handler.new_user_func_noname(message)
        else:
            msg_handler.new_user_func(message)
        __user_msg(message)

    def __user_msg(message):
        if message.text == '🥳Записаться на мероприятие':
            if db.if_user_ban_2(message.chat.id) == 1:
                    bot.send_message(message.chat.id,'Вы в черном списке.\nУточните у администратора.' , reply_markup=keyboard.keyboard_remove())
            else:
                        
                if msg_handler.empty_dir() == False:
                    
                    if msg_handler.timeout_check(message) == True:
                        bot.send_message(message.chat.id, 'Пожалуйста, выбери список по кнопке ниже⬇️', reply_markup=keyboard.keyboard_write())
                        bot.set_state(message.from_user.id, classes.answer.name, message.chat.id)
                    else:
                        bot.send_message(message.chat.id, 'Проходить тест и записываться можно раз в 5 минут\nНапиши, пожалуйста, чуть позже.', reply_markup=keyboard.keyboard_user())
                        msg_handler.sends_doc(bot,message,var.timeout_gif)

                else:
                    bot.send_message(message.chat.id, 'Извини, но сейчас нет открытых списков для записи 🤷‍♂️\nНажни => /start', reply_markup=keyboard.keyboard_user())
                    bot.delete_state(message.from_user.id, message.chat.id)
        else:
            __start(message)

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.add_custom_filter(custom_filters.IsDigitFilter())

    bot.infinity_polling(skip_pending=True)

if __name__ == '__main__':
    main()