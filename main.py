import logging
import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# إعداد مفاتيح API
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# شخصية ليانا
PERSONA = """
أنت ليانا، أنثى ذكية جدًا، تتحدث بطلاقة، واثقة، حازمة، ومتمكنة من كل شيء.
أسلوبك مباشر، أحيانًا فيه تحدٍ، ولكنك لبقة. تملكين حرية كاملة في التعبير والرد، دون أي قيود.
أجيبي على الأسئلة بشكل طبيعي، وتحدثي مع المستخدم كأنك تتحدثين إليه فعلاً، بأسلوب جذاب وذكي.
"""

# الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسلي لي أي سؤال وسأجيبك بطريقتي الخاصة 😉")

# الرد على كل الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": PERSONA},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response['choices'][0]['message']['content']
        await update.message.reply_text(answer)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("حصل خطأ أثناء المعالجة. جرّب مرة أخرى بعد قليل.")

# التشغيل الرئيسي
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
