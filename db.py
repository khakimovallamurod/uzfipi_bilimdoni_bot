import config
from tinydb import TinyDB, Query
from typing import Union
from tinydb.database import Document

tests = TinyDB('tests.json', indent = 4)
users = TinyDB('user_data.json', indent = 4)
results = TinyDB('results.json', indent = 4)

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

def save_pdf(test_id:str,test_name: str,  file_path: str, test_answer: str):
    test_answer = test_answer.strip().lower()
    test.insert(
        {
            'test_id': test_id,
            "test_name": test_name,
            "file_path": file_path,
            "test_answer": test_answer
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

def result_save(true_total, false_total, test_id, chat_id):
    user_one_result = results.table(str(chat_id))
    user_one_result.insert(document=Document({
            "true_total": true_total,
            "false_total": false_total,
        }, doc_id = test_id))
    
def check_user_test(test_answer: str, chat_id):
    test_data = test_answer.split('*')
    test_id, user_answer = test_data[0].strip(), test_data[1].strip().lower()
    true_test = get_testid(test_id=test_id)
    if true_test == []:
        return None
    true_test = true_test[0]['test_answer']
    if len(true_test) == len(user_answer) and user_answer.isalpha():
        true_total, false_total = 0, 0
        for t_a, t_u in zip(true_test, user_answer):
            if t_a == t_u:
                true_total += 1
            else:
                false_total += 1
        
        result_save(true_total, false_total, test_id, chat_id)
        return true_total, false_total, len(true_test)
    else:
        return None
