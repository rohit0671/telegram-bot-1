import os
import time
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLISHER_ID = os.getenv("RICHADS_PUBLISHER_ID")
WIDGET_ID = os.getenv("RICHADS_WIDGET_ID")

RICHADS_URL = "https://xml.adx1.com/telegram-mb"
COOLDOWN_SECONDS = 60

user_last_ad_time = {}

def get_richads_ad(chat_id):
    payload = {
        "publisher_id": PUBLISHER_ID,
        "widget_id": WIDGET_ID,
        "telegram_id": chat_id,
        "language_code": "en",
        "bid_floor": 0.0001,
        "production": True
    }
    try:
        r = requests.post(RICHADS_URL, json=payload, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print("RichAds error:", e)
    return None

def can_show_ad(chat_id):
    now = time.time()
    last = user_last_ad_time.get(chat_id, 0)
    if now - last >= COOLDOWN_SECONDS:
        user_last_ad_time[chat_id] = now
        return True
    return False

def start(update: Update, context):
    chat_id = update.message.chat_id
    update.message.reply_text("Welcome 👋")

    if not can_show_ad(chat_id):
        update.message.reply_text("Please wait before next ad ⏳")
        return

    ad = get_richads_ad(chat_id)
    if not ad:
        update.message.reply_text("No ad available right now.")
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(ad.get("button", "Open"), url=ad["link"])]
    ])

    update.message.bot.send_photo(
        chat_id=chat_id,
        photo=ad["image"],
        caption=f"<b>{ad['title']}</b>\n\n{ad['message']}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    if "notification_url" in ad:
        try:
            requests.get(ad["notification_url"], timeout=5)
        except:
            pass

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
