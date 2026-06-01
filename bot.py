import logging
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === SOZLAMALAR ===
TELEGRAM_TOKEN = "8829917741:AAE1z3Na4RqwtJtJz7pvMe8Uni8pE6f1U78"
OUTPUT_FILE = "xabarlar.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mavjud ma'lumotlarni yuklash
def load_data():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Ma'lumotlarni saqlash
def save_data(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Xabarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    # Faqat may oyidagi xabarlar
    msg_date = message.date
    if msg_date.month != 5:  # 5 = may
        return

    entry = {
        "sana": msg_date.strftime("%d.%m.%Y"),
        "vaqt": msg_date.strftime("%H:%M"),
        "kimdan": message.from_user.full_name if message.from_user else "Noma'lum",
        "username": message.from_user.username if message.from_user else "",
        "matn": message.caption or message.text or "",
        "rasm_bor": message.photo is not None and len(message.photo) > 0,
        "message_id": message.message_id,
        "chat_id": message.chat_id,
    }

    data = load_data()
    data.append(entry)
    save_data(data)

    logger.info(f"Saqlandi: {entry['sana']} - {entry['matn'][:50]}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    
    print("Bot ishga tushdi! xabarlar.json ga yozilmoqda...")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
