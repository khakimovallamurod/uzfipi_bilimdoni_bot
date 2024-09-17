import config
from tinydb import TinyDB, Query
from typing import Union
from tinydb.database import Document

tests = TinyDB('tests.json', indent = 4)
users = TinyDB('results.json', indent = 4)
test = tests.table('Test')
user = users.table('Users')

q = Query()

def is_admin(chat_id):
    admin_id = config.get_adminid()
    if admin_id == str(chat_id):
        return True
    else:
        return False
    
def is_start(chat_id):
    user_one = user.get(doc_id=str(chat_id))
    return user_one == None

def save_pdf(test_id:str,test_name: str,  file_path: str):
    test.insert(
        {
            'test_id': test_id,
            "test_name": test_name,
            "file_path": file_path
        }
    )
    return True

def register(chat_id, fak, yunlish, kurs, fullname):
    user.insert(document=Document({
        "fakultitet": fak,
        "yunalish": yunlish,
        "kurs": kurs,
        "fullname": fullname,
    }, doc_id = chat_id))

def user_search(chat_id):
    return user.get(doc_id=str(chat_id))

def get_testid(test_id):
    test_one = test.search(q.test_id == str(test_id))
    return test_one
