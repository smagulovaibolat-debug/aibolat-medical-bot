import os
import subprocess
import sys

# СЕРВЕРГЕ КІТАПХАНАЛАРДЫ КҮШТЕП ОРНАТУ (БҰЛ МІНДЕТТІ ТҮРДЕ ІСТЕЙДІ)
def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", "google-generativeai", "flask"])
        print("Кітапханалар сәтті орнатылды!")
    except Exception as e:
        print(f"Орнату қатесі: {e}")

# Код басталмас бұрын орнатуды іске қосамыз
install_requirements()

import telebot
import google.generativeai as genai

# Негізгі баптаулар
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        bot.send_message(message.chat.id, f"ЖИ қатесі: {e}")

if __name__ == "__main__":
    print("Бот іске қосылуда...")
    bot.infinity_polling()
