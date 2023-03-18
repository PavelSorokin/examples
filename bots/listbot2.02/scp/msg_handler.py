from datetime import datetime
import glob, os
from scp import db
from config import timeout_seconds

def sends_doc(bot, message, doc):
    docs = open(doc, 'rb')
    bot.send_document(message.chat.id, docs)

def safes_state(bot, message, state):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data[state] = message.text
        
def empty_dir():
    ls = []       
    lists = os.listdir('./lists')
    if len(lists) != 0:
        for i in lists:
            if (i.startswith('close')) == False:
                ls.append(i)
    if len(lists) == 0 and ls == []:
        return True
    elif len(lists) !=0 and ls == []:
        return True
    else:
        return False

def empty_dir_admin():       
    lists = os.listdir('./lists')
    if len(lists) == 0:
        return True
    else:
        return False

def new_user_func(message):
    if not db.if_user_exists(message.chat.id):
        db.new_user(message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)

def new_user_func_noname(message):
    if not db.if_user_exists(message.chat.id):
        db.new_user(message.chat.id, message.chat.id, message.from_user.first_name, message.from_user.last_name)

def new_list(list_name):
    if db.if_list_exists(list_name) == False:
        db.insert_list(list_name)
        return True
    else:
        return False
        
def create_list_file(name):
    with open('./lists/'+ name +'.txt', 'w') as files:
        files.close

def check_deadline(name):
        if os.path.isfile('./lists/'+name+'.txt') == True:
            with open('./lists/'+name+'.txt','r+') as files:
                my_list = [x.rstrip() for x in files]
                number = len(my_list)
            return number
        else:
            return 100000

def update_timeout(message):
    timeouts = datetime.now()
    db.update_timeout_on(timeouts, message.chat.id)

def timeout_check(message):
    now = datetime.now()
    if db.get_timeout(message.chat.id) == 0:        
        return True
    else:
        if (now-datetime.strptime(db.get_timeout(message.chat.id),"%Y-%m-%d %H:%M:%S.%f")).seconds < timeout_seconds:
            return False
        else:
            return True