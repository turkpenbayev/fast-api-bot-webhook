from fastapi import HTTPException
import aiohttp

from app.config import settings

async def send_telegram_message(user_id: int, message: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": user_id,
        "text": message,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, ssl=False) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Telegram API error")

