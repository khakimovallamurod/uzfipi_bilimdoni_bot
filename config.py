from dotenv import load_dotenv
import os

load_dotenv()
def get_token():
    TOKEN = os.getenv("TOKEN")
    Admin = os.getenv("admin_id")
    if TOKEN is None:
        raise ValueError("TOKEN not found.")
    return TOKEN

def get_adminid():
    admin_id = os.getenv("admin_id")
    if admin_id is None:
        raise ValueError("admin_id not found.")
    return admin_id