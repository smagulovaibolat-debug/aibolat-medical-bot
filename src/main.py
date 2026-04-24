import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# 1. Environment Variables-тен кілттерді алу
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')
PORT = int(os.environ.get('PORT', 5000))

# 2. Gemini ЖИ баптау (Ең тұрақты модель атымен)
genai.configure(api_key=GEMINI_KEY)
# 'gemini-1.5-flash' орнына 'gemini-1.5-flash-latest' немесе 'gemini-pro' қолданамыз
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 3. Telegram Ботты баптау
bot = telebot.TeleBot(TOKEN)

# 4. Render үшін кішкентай веб-сервер (Timed Out қатесін болдырмау үшін)
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот жұмыс істеп тұр!"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

# 5. Боттың логикасы
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Сәлеметсіз бе! Мен доктор Айболаттың цифрлық көмекшісімін. Сізге медициналық сұрақтар бойынша көмектесуге дайынмын.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Gemini-ден жауап алу
        prompt = f"Сен — Қызылорда онкология орталығының хирург дәрігері Айболат Смагуловтың көмекшісісің. Пациентке қазақша кәсіби әрі жылы жауап бер. Сұрақ: {message.text}"
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Кешіріңіз, ЖИ жауап дайындай алмады. Сұрақты басқаша қойып көріңіз.")
            
    except Exception as e:
        print(f"Қате орын алды: {e}")
        bot.reply_to(message, f"ЖИ қатесі: Модель жүктелуде немесе кілтте ақау бар. Сәлден соң қайталаңыз.")

# 6. Ботты және Веб-серверді қатар іске қосу
if __name__ == "__main__":
    # Flask-ты бөлек ағында іске қосу
    threading.Thread(target=run_flask).start()
    # Ботты негізгі ағында іске қосу
    print("Бот сәтті іске қосылды...")
    bot.infinity_polling()
