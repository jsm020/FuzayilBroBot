import asyncio
import os
import aiosqlite
import xlsxwriter
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, FSInputFile
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(i) for i in os.getenv('ADMIN_IDS', '').split(',') if i.strip().isdigit()]
WEB_APP_URL = os.getenv('WEB_APP_URL', 'https://karavanshop.uz')

# DB yaratish
async def create_db():
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            full_name TEXT,
            phone TEXT
        )''')
        await db.commit()

# Foydalanuvchini qo'shish
async def user_exists(user_id):
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchone() is not None
    async with aiosqlite.connect('users.db') as db:
        await db.execute(
            'INSERT OR IGNORE INTO users (user_id, full_name, phone) VALUES (?, ?, ?)',
            (user_id, full_name, phone)
        )
        await db.commit()

# Foydalanuvchilar ID ro'yxatini olish
async def get_all_users():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT user_id FROM users') as cursor:
            return [row[0] for row in await cursor.fetchall()]

# Foydalanuvchilar to'liq ma'lumotini olish
async def get_all_users_full():
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT user_id, full_name, phone FROM users') as cursor:
            return await cursor.fetchall()

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# /start komandasi
@dp.message(CommandStart())
async def start(message: types.Message):
    if await user_exists(message.from_user.id):
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🌐 Web App ochish", web_app=WebAppInfo(url=WEB_APP_URL))]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Siz allaqachon ro'yxatdan o'tgansiz! Web App ochish uchun tugmani bosing:", reply_markup=kb)
    else:
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Assalomu alaykum! Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:", reply_markup=kb)

# Kontakt yuborilganda
@dp.message(lambda m: m.contact is not None)
async def contact_handler(message: types.Message):
    contact = message.contact
    await add_user(message.from_user.id, message.from_user.full_name, contact.phone_number)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🌐 Web App ochish", web_app=WebAppInfo(url=WEB_APP_URL))]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("✅ Ro'yxatdan o'tdingiz! Web App ochish uchun tugmani bosing:", reply_markup=kb)

# Admin uchun: xabar yuborish
@dp.message(lambda m: m.text and m.from_user.id in ADMIN_IDS and m.text.startswith('/sendall'))
async def sendall_handler(message: types.Message):
    text = message.text[8:].strip()
    if not text:
        await message.answer("⚠️ Xabar matni kerak: /sendall Salom hammaga!")
        return

    users = await get_all_users()
    count = 0
    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            count += 1
        except:
            pass

    await message.answer(f"✅ Xabar {count} ta foydalanuvchiga yuborildi.")

# Admin uchun: foydalanuvchilar ro'yxatini Excelga eksport qilish
@dp.message(lambda m: m.text and m.from_user.id in ADMIN_IDS and m.text.startswith('/exportusers'))
async def export_users_handler(message: types.Message):
    users = await get_all_users_full()
    if not users:
        await message.answer("❗ Bazada foydalanuvchilar topilmadi.")
        return

    file_path = 'users_export.xlsx'
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, ["user_id", "full_name", "phone"])

    for idx, row in enumerate(users, start=1):
        worksheet.write_row(idx, 0, row)

    workbook.close()

    document = FSInputFile(file_path)
    await bot.send_document(message.from_user.id, document, caption="📄 Foydalanuvchilar ro'yxati (Excel)")
    os.remove(file_path)

# Botni ishga tushirish
async def main():
    await create_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


