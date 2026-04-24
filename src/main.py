import os
import telebot
import google.generativeai as genai

# Кілттер
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

# Gemini баптау
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Ботты іске қосу
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Сәлеметсіз бе! Доктор Айболаттың көмекшісі жұмыс істеп тұр.")

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        bot.send_message(message.chat.id, f"ЖИ қатесі: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()
