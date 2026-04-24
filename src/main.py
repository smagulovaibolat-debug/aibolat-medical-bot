import os
import telebot
import google.generativeai as genai

# Кілттерді жүктеу
TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('GEMINI_KEY')

# Ботты баптау
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        # Gemini-ге сұраныс
        response = model.generate_content(message.text)
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        # Қатенің нақты атын Telegram-ға жіберу
        error_msg = f"ЖИ қатесі: {str(e)}"
        bot.send_message(message.chat.id, error_msg)

# Тұрақты жұмыс істеу үшін веб-сервер (Render үшін)
from flask import Flask
import threading

app = Flask('')
@app.route('/')
def home(): return "Бот жұмыс істеп тұр!"

def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
threading.Thread(target=run).start()

bot.infinity_polling()
