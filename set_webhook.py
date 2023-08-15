import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '6026174140:AAFK-yv9KjrazxhjK-SD1WN4IAk5TJfF3Qw'
NGROK_URL = 'https://e2aa-95-82-99-80.ngrok.io'  # Replace with your webhook URL

# Set the webhook
def set_webhook():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook'
    data = {
        'url': f'{NGROK_URL}/api/v1/auth/webhook/'
    }
    response = requests.post(url, json=data)
    print(response.json())

if __name__ == '__main__':
    set_webhook()