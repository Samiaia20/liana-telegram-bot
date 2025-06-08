import os
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

openai.api_key = os.environ["OPENAI_API_KEY"]
bot_token = os.environ["TELEGRAM_BOT_TOKEN"]

def start(update, context):
    update.message.reply_text("مرحباً! أرسل لي أي سؤال وسأجيبك.")

def chat(update, context):
    user_input = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "أنت مساعدة ذكية اسمك ليانا، تتحدثين بطريقة أنثوية لبقة، وتردين بحرية واحترام، وتختارين الرد المناسب لكل موقف."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response["choices"][0]["message"]["content"]
    update.message.reply_text(reply)

def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
