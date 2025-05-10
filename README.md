# FuzayilBroBot

## Qisqacha qo‘llanma

1. **Talablar:**
   - Python 3.8+
   - `requirements.txt` dagi kutubxonalar: 
     ```bash
     pip install -r requirements.txt
     ```

2. **Sozlash:**
   - `.env` faylini oching va quyidagilarni to‘ldiring:
     ```ini
     BOT_TOKEN=your_telegram_bot_token_here
     ADMIN_IDS=admin_id1,admin_id2
     WEB_APP_URL=https://karavanshop.uz
     ```

3. **Botni ishga tushirish:**
   ```bash
   python3 bot.py
   ```

4. **Foydalanish:**
   - Foydalanuvchi /start bosganda, agar bazada bo‘lsa, to‘g‘ridan-to‘g‘ri Web App tugmasi chiqadi.
   - Yangi foydalanuvchi telefon raqamini yuborib ro‘yxatdan o‘tadi.
   - Admin quyidagi komandalarni ishlata oladi:
     - `/sendall xabar matni` — barcha foydalanuvchilarga xabar yuborish
     - `/exportusers` — barcha foydalanuvchilar ro‘yxatini Excel fayl ko‘rinishida olish

5. **E'tibor bering:**
   - `users.db` va `.env` fayllari gitga kirmaydi (ular `.gitignore`da ko‘rsatilgan).