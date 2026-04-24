import os
import telebot
import google.generativeai as genai
import sys

# Кілттерді тексеру
token = os.environ.get('TELEGRAM_TOKEN')
api_key = os.environ.get('GEMINI_KEY')

if not token or not api_key:
    print("Қате: Кілттер табылған жоқ! Environment Variables бөлімін тексеріңіз.")
    sys.exit(1)

# Баптау
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(token)

print("Бот іске қосылды...")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Сәлеметсіз бе! Мен доктор Айболаттың көмекшісімін. Сізге қалай көмектесе аламын?")

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        response = model.generate_content(f"Сен — хирург Айболат Смагуловтың көмекшісісің. Қазақша жауап бер. Сұрақ: {message.text}")
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        print(f"Gemini қатесі: {e}")
        bot.send_message(message.chat.id, "Кешіріңіз, ЖИ жауап бере алмай тұр. Кілтті тексеру керек.")

bot.infinity_polling()
