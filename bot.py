

# --- SOZLAMALAR ---
BOT_TOKEN = "8881776997:AAGUDveO5IamtiaJjjiP66WKFmo4NU7-q_Q"
WEBAPP_URL = "https://javohirkenjaev.github.io/fikrhub-webapp/"
GEMINI_API_KEY = "AQ.Ab8RN6JKFk5VO3EDzkf_5rzW8OnL_x2kj3eosBiRR55OHwCdXA"

import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Assalomu alaykum, <b>{user_name}</b>! 🌟\n\n"
        f"<b>FikrHub</b> - Xorazmdagi eng yirik do'konlar va xizmatlar platformasiga xush kelibsiz.\n\n"
        f"🤖 <i>Menga istalgan savolni yozing, men sizga AI yordamida javob beraman!</i>"
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 FikrHub Platformasini Ochish", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer(welcome_text, reply_markup=markup, parse_mode="HTML")

@dp.message(F.text)
async def ai_chat_handler(message: types.Message):
    wait_msg = await message.answer("⏳ AI javob tayyorlamoqda...")
    
    try:
        # Google talab qilgan eng so'nggi gemini-3.8-flash modeli
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"Sen FikrHub Pro platformasining aqlli maslahatchisisan (asoschi Javohir Kenjayev). Foydalanuvchi savoli: {message.text}"
        )
        
        reply_text = response.text if response and response.text else "Javob topilmadi."
        
        full_text = f"🤖 <b>FikrHub AI:</b>\n\n{reply_text}\n\n👇 <i>Do'konlarni ko'rish uchun tugmani bosing:</i>"
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Platformadan Qidirish", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
        
        await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
        await message.answer(full_text, reply_markup=markup, parse_mode="HTML")
        
    except Exception as e:
        print(f"AI Xatolik tafsiloti: {e}")
        await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    print("🚀 FikrHub AI Boti muvaffaqiyatli ishga tushdi!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())