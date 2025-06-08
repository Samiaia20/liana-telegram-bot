import os, openai
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# خادم Replit صغير لإبقاء البوت نشط
app = Flask('')
@app.route('/')
def home():
    return "🤖 Bot is alive!"
Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))), daemon=True).start()

# مفاتيح السر
openai.api_key = os.environ['OPENAI_API_KEY']
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل لي أي سؤال وسأجيبك.")

# الرد على النص
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content
    await update.message.reply_text(reply)

bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
bot.add_handler(CommandHandler("start", start))
bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
bot.run_polling()