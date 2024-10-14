import requests
from config import get_token
TOKEN = get_token()
URL = 'https://allamurodxakimov.pythonanywhere.com/'  # Flask ilovangizning webhook URL'si

# Webhook URL'ni sozlash
webhook_url = f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}'
response = requests.get(webhook_url)

if response.ok:
    print('Webhook set successfully')
else:
    print('Failed to set webhook')
