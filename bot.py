import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import openai
from dotenv import load_dotenv
import os

# Отключаем строгую валидацию pydantic (workaround для pydantic 2.10.6)
os.environ["OPENAI_PYTHON_DISABLE_PYDANTIC_VALIDATION"] = "1"

# Указываем базовый URL для OpenRouter.ai
openai.api_base = "https://openrouter.ai/api/v1"

load_dotenv()  # Загружаем переменные окружения из файла .env

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def get_ai_response(user_text: str) -> str:
    openai.api_key = OPENROUTER_API_KEY
    try:
        # Оборачиваем вызов в asyncio.to_thread, так как acreate не поддерживается
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="google/gemini-2.0-pro-exp-02-05:free",  # Проверьте название модели согласно документации OpenRouter
            messages=[{"role": "user", "content": user_text}],
            max_tokens=150,
            temperature=0.7,
        )
        result_text = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        result_text = f"Произошла ошибка: {e}"
    return result_text

async def main():
    bot = Bot(token=TELEGRAM_API_TOKEN)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("Привет! Я Telegram-бот с интеграцией AI. Напиши мне что-нибудь.")

    @dp.message(Command("help"))
    async def help_command(message: types.Message):
        await message.answer("Я бот, который обрабатывает твои сообщения и возвращает ответы от AI. Просто напиши сообщение!")

    @dp.message()
    async def handle_message(message: types.Message):
        if message.text:
            ai_response = await get_ai_response(message.text)
            await message.answer(ai_response)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
