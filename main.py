import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
# Исправленный импорт:
from aiocryptopay import AioCryptoPay, Networks

# Токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CRYPTO_TOKEN = os.getenv("CRYPTO_TOKEN")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация CryptoBot (используем AioCryptoPay и Networks)
# Если тестируете, замените Networks.MAIN_NET на Networks.TEST_NET
crypto = AioCryptoPay(token=CRYPTO_TOKEN, network=Networks.MAIN_NET)

# --- ЧАСТЬ 1: TELEGRAM БОТ ---
@dp.message(Command("start"))
async def start(message: types.Message):
    # Замените ссылку на свою (GitHub Pages)
    web_app_url = "https://ВАШ_ЛОГИН.github.io/ВАШ_РЕПОЗИТОРИЙ/"
    
    kb = [[types.InlineKeyboardButton(
        text="Открыть магазин 🛍", 
        web_app=types.WebAppInfo(url=web_app_url)
    )]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Добро пожаловать! Жмите кнопку:", reply_markup=keyboard)

# --- ЧАСТЬ 2: API ДЛЯ MINI APP ---
async def handle_create_invoice(request):
    try:
        # Создаем счет на 10 USDT
        invoice = await crypto.create_invoice(asset='USDT', amount=10.0)
        # Возвращаем ссылку фронтенду
        return web.json_response({'pay_url': invoice.bot_invoice_url})
    except Exception as e:
        print(f"Error: {e}")
        return web.json_response({'error': str(e)}, status=500)

async def health_check(request):
    return web.Response(text="OK")

# Настройка сервера
app = web.Application()
app.router.add_post('/create-invoice', handle_create_invoice)
app.router.add_get('/', health_check) # Для проверки, что сервер жив

async def main():
    # Запускаем бота фоном
    asyncio.create_task(dp.start_polling(bot))

    # Запускаем веб-сервер на порту от Render
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    print(f"Server started on port {port}")
    await site.start()

    # Держим процесс запущенным
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
