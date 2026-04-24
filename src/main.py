import os
import telebot
import google.generativeai as genai

# Environment variables-тен кілттерді алу
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

# Gemini-ді баптау
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Telegram ботты бастау
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Боттың мінез-құлқын анықтау
SYSTEM_PROMPT = """Сен — хирург Айболат Смагуловтың цифрлық көмекшісісің. 
Тілің: Қазақ тілі. Пациенттерге жылы жауап беріп, медициналық кеңестер ұсын. 
Сұрақтарға кәсіби әрі түсінікті жауап бер."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Сәлеметсіз бе! Мен доктор Айболаттың цифрлық көмекшісімін. Сізге қалай көмектесе аламын?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Gemini-ден жауап алу
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nПациент: {message.text}")
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        bot.send_message(message.chat.id, "Кешіріңіз, қате орын алды. Сәлден кейін қайталап көріңіз.")

# Ботты іске қосу
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Bot is running!"

    import threading
    threading.Thread(target=bot.infinity_polling).start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
