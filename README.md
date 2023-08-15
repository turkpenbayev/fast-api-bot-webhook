# FastApi TelegramBot WEBHOOK

1. install requirments python>=3.10 version:

    ```sh
    $ pip install -r requirements.txt
    ```


2. run app

    ```sh
    $ uvicorn app.main:app
    ```

3. run ngrok

    ```sh
    $ ngrok http 8000
    ```

4. set webhook for bot modify set_webhook.py file:

    ```sh
    NGROK_URL = '' Replace with your webhook URL
    ```

    run script
    ```sh
    $ python set_webhook.py 
    ```


1. Bot [https://t.me/fab_tel_bot](https://t.me/fab_tel_bot)

