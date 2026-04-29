import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8505135235:AAEaGciF3qKt6hHTbwZrOPkRgQSOIwjjVvk"  # Замени на свой
ADMIN_ID = 8670014042       # Замени на свой ID (числом)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 1. ГЛАВНОЕ МЕНЮ ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    
    # Кнопка для GUI (Web App). Если нет своего сайта, пока оставим Google для теста.
    builder.row(InlineKeyboardButton(
        text="🚀 Отправить коментарий", 
        web_app=WebAppInfo(url="https://tg-ja7w.onrender.com")) 
    )
    
    builder.row(InlineKeyboardButton(
        text="📝 Отправить заказ", 
        callback_data="write_complaint")
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе связаться с разработчиком.",
        reply_markup=builder.as_markup()
    )

# --- 2. ЛОГИКА ЖАЛОБ ---
@dp.callback_query(F.data == "write_complaint")
async def ask_complaint(callback: types.CallbackQuery):
    await callback.message.answer("Пожалуйста, напиши текст заказа. Я сразу передам его администратору.")
    await callback.answer()

@dp.message(lambda message: message.text and not message.text.startswith('/'))
async def forward_complaint(message: types.Message):
    # Отправляем админу
    try:
        await bot.send_message(
            ADMIN_ID, 
            f"📩 **НОВЫЙ ЗАКАЗ**\n\n"
            f"От: @{message.from_user.username or 'без_ника'}\n"
            f"ID: `{message.from_user.id}`\n"
            f"Текст: {message.text}"
        )
        await message.answer("✅ Спасибо! Твое сообщение отправлено разработчику.")
    except Exception as e:
        await message.answer("Ошибка при отправке. [Error] : ADMIN_ID.")
        print(f"Ошибка: {e}")

@dp.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)


# --- ЗАПУСК ---
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")

