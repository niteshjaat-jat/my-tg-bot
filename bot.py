import telebot
from groq import Groq
import time
import sys
import os
from threading import Thread
from flask import Flask

# --- RENDER KE LIYE SERVER SETUP (Isse 'Port' wala error nahi aayega) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    # Render automatically PORT environment variable deta hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    # Server ko alag thread mein chalate hain taaki bot bhi chalta rahe
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION ---
# Yaad rahe: In keys ko naya generate karke yahan replace karna safety ke liye zaroori hai
BOT_TOKEN = "8550399459:AAEaCVATWHdKEyBRUWrTKopwU80AJmSXxYY"
GROQ_API_KEY = "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"

# Clients initialization
try:
    client = Groq(api_key=GROQ_API_KEY)
    bot = telebot.TeleBot(BOT_TOKEN)
except Exception as e:
    print(f"Initialization Error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(f"Message received: {message.text}")
    try:
        # Llama 3.3 model use kar rahe hain
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message.text}],
        )
        reply = completion.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        print(f"AI Error: {e}")
        bot.reply_to(message, "AI thoda busy hai, kripya 1 minute baad try karein.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Pehle Web Server chalu karo taaki Render status "Live" dikhaye
    keep_alive()
    print("--- Web Server started successfully ---")
    
    # 2. Bot ki polling shuru karo
    print("--- Telegram Bot is starting... ---")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            # Agar koi network error aaye toh 5 sec ruk kar fir chalu karega
            print(f"Polling Error: {e}")
            time.sleep(5)
