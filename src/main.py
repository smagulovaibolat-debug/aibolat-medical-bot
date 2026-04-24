import os
import telebot
import google.generativeai as genai

# Айнымалыларды алу
TOKEN = os.environ.get('TELEGRAM_TOKEN')
KEY = os.environ.get('GEMINI_KEY')

# Ботты іске қосу
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Сәлеметсіз бе! Доктор Айболаттың көмекшісі жұмыс істеп тұр.")

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        bot.send_message(message.chat.id, f"ЖИ қатесі: {e}")

# Ботты үзіліссіз жұмыс істету
if __name__ == "__main__":
    bot.infinity_polling()
