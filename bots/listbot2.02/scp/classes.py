from telebot.handler_backends import State, StatesGroup

class create_list(StatesGroup):
    name = State()

class delete_list(StatesGroup):
    name = State()

class close_list(StatesGroup):
    name = State()

class open_list(StatesGroup):
    name = State()

class read_list(StatesGroup):
    name = State()

class intdeadline(StatesGroup):
    name = State()
    deadline = State()

class answer(StatesGroup):
    name = State()
    fio = State()
    answer1 = State()
    answer2 = State()
    answer3 = State()

class quest(StatesGroup):
    _question = State()
    _new_question = State()
    _new_answer_var = State()
    _new_answer = State()

class cls_msg():

    def msg_help(self):
        self.msg_help_txt = 'Привет, для работы с ботом отправь /start'
        return self.msg_help_txt

    def msg_start(self, first_name):
        self.first_name = first_name  
        self.msg_start_txt = 'Привет, {first_name}!\nТы хочешь записаться на мероприятие?\nСледуй командам ниже 😉⬇️'.format(first_name=self.first_name)
        return self.msg_start_txt

    def msg_newlist(self):
        self.msg_start_txt = 'Как назвать список?'
        return self.msg_start_txt
        
    def msg_start_admin(self):
        self.msg_help_txt = 'Привет! Выбери, что мне сделать со списками на мероприятие:\nПоказать - Выводит сообщение о всех списках\nСоздать - Создает на сервере список, в который можно начинать вписывать людей\nЗакрыть - Отправляет готовый список,и переименовывает его с префиксом "close_"(чтобы ни кто его не видел, кроме тебя)\nУдалить - удалет навсегда список с сервера'
        return self.msg_help_txt
        