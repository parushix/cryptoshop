import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiocryptopay import CryptoPay
import asyncio

# Берем токены из переменных окружения (для безопасности)
token = os.getenv("BOT_TOKEN")
crypto_token = os.getenv("CRYPTO_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()
crypto = CryptoPay(token=crypto_token, network='mainnet') # Смените на testnet для тестов

@dp.message(Command("start"))
async def start(message: types.Message):
    # Кнопка для открытия Mini App (замените URL на ваш после Шага 2)
    kb = [[types.InlineKeyboardButton(text="Открыть магазин 🛍", 
            web_app=types.WebAppInfo(url="https://ВАШ_АККАУНТ.github.io/my-shop/"))]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Привет! Нажми кнопку ниже, чтобы войти в магазин:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())