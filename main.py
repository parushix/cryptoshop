import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiocryptopay import CryptoApp  # Исправленный импорт

# Токены (убедитесь, что они добавлены в Environment Variables на Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTO_TOKEN = os.getenv("CRYPTO_TOKEN")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
# Используем CryptoApp вместо CryptoPay
crypto = CryptoApp(token=CRYPTO_TOKEN, network='mainnet') 

# --- ЧАСТЬ ДЛЯ TELEGRAM БОТА ---
@dp.message(Command("start"))
async def start(message: types.Message):
    # Укажите здесь вашу ссылку на GitHub Pages
    web_app_url = "https://ВАШ_ЛОГИН.github.io/ВАШ_РЕПОЗИТОРИЙ/"
    kb = [[types.InlineKeyboardButton(text="Открыть магазин 🛍", 
            web_app=types.WebAppInfo(url=web_app_url))]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Добро пожаловать! Нажмите кнопку для входа:", reply_markup=keyboard)

# --- ЧАСТЬ ДЛЯ MINI APP (API) ---
async def handle_create_invoice(request):
    try:
        # Создаем счет на 10 USDT
        invoice = await crypto.create_invoice(asset='USDT', amount=10.0)
        return web.json_response({'pay_url': invoice.pay_url})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

# Настройка веб-сервера
app = web.Application()
app.router.add_post('/create-invoice', handle_create_invoice)

async def main():
    # Запуск бота в фоновом режиме
    asyncio.create_task(dp.start_polling(bot))
    
    # Запуск веб-сервера на порту, который дает Render
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    print(f"Server started on port {port}")
    await site.start()
    
    # Чтобы скрипт не завершался
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
