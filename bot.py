import telebot
from groq import Groq
import time
import sys

# --- CONFIGURATION ---
# 1. Telegram Token wahi rahega
BOT_TOKEN = "8550399459:AAEaCVATWHdKEyBRUWrTKopwU80AJmSXxYY"

# 2. Yahan apni Nayi Groq API Key dalein
GROQ_API_KEY = "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"

# Clients Setup
client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

print("--- Bot 4.0 (Groq Powered) is LIVE! ---")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print(f"User ne pucha: {message.text}")
    
    try:
        # Llama 3.3 Model use kar rahe hain (Super Fast & Free)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": message.text}],
        )
        
        reply = completion.choices[0].message.content
        bot.reply_to(message, reply)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "AI thoda thak gaya hai, 1 minute baad try karein!")

# --- SMART LOOP ---
while True:
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\nStopping...")
        sys.exit(0)
    except Exception as e:
        time.sleep(5)