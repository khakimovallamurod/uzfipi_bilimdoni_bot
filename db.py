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

def register(chat_id, fak, yunlish, kurs,nomer, fullname):
    user.insert(document=Document({
        "fakultitet": fak,
        "yunalish": yunlish,
        "kurs": kurs,
        "nomer": nomer,
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
    
    test_id, user_answer_old = test_data[0].strip(), test_data[1].strip().lower()
    true_test = get_testid(test_id=test_id)
    true_test_answer = true_test[0]['test_answer']

    user_answer = ''
    for alp in user_answer_old:
        if alp.isalpha():
            user_answer+=alp

    true_test_filter = ''
    for alp in true_test_answer:
        if alp.isalpha():
            true_test_filter+=alp
    
    if len(test_data) != 2:
        return 'error_testid'
    elif len(true_test_filter) == len(user_answer) and user_answer.isalpha():
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

def admin_get_result(testID: str):
    table_all = sorted(list(results.tables()))
    result_user_data = []
    for table in table_all:
        table_data = results.table(table).get(doc_id=testID)
        if table_data != None:
            user_data = user_search(table)
            user_data['true_total'] = table_data['true_total']
            user_data['false_total'] = table_data['false_total']
            result_user_data.append(user_data)
    result_user_data = sorted(result_user_data, key=lambda x: x['true_total'], reverse=True)
    return result_user_data
