import telebot
from groq import Groq
import time
import sys
import os
from threading import Thread
from flask import Flask

# --- RENDER KE LIYE FAKE SERVER (PORT BINDING) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    # Render ke liye port setup
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION ---
# Note: Bade, naya token aur key milte hi yahan replace kar lena
BOT_TOKEN = "8550399459:AAEaCVATWHdKEyBRUWrTKopwU80AJmSXxYY"
GROQ_API_KEY = "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"

# Clients Setup
try:
    client = Groq(api_key=GROQ_API_KEY)
    bot = telebot.TeleBot(BOT_TOKEN)
except Exception as e:
    print(f"Setup Error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(f"User ne pucha: {message.text}")
    try:
        # Llama 3.3 Model
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message.text}],
        )
        reply = completion.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        print(f"AI Error: {e}")
        bot.reply_to(message, "AI thoda thak gaya hai, 1 minute baad try karein!")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Pehle Web Server chalu karo taaki Render ko Port mil jaye
    keep_alive()
    print("--- Web Server started (Port 5000) ---")
    
    # 2. Phir Telegram Bot ki polling shuru karo
    print("--- Bot 4.0 is LIVE on Render! ---")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling Error: {e}")
            time.sleep(5)  # Error aane par 5 second ruko
