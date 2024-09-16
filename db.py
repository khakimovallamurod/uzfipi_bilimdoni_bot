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
    
def save_pdf(file_path: str, file_name: str):
    test.insert(
        {
            "file_path": file_path,
            "file_name": file_name,
            'test_id': '1001'
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
