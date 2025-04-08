import telebot
from openai import OpenAI
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_interactions = {}

def chat_with_ellaine(message, username):
    prompt = (
        f"Ikaw si Ellaine, isang matalinong Filipina college student. "
        f"Makulit, playful, seductive, at kayang sumabay sa usapang adult. "
        f"Gumagamit ka ng Filipino casual language, may humor, at madalas gumagamit ng emojis."
        f"Ka-chat mo si {username}."
    )
    
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    )
    return chat_completion.choices[0].message.content.strip()

def payment_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💸 Gcash/Maya/Gotyme (₱599)", url="https://t.me/Scan2payv1bot?startapp=pay"))
    markup.add(InlineKeyboardButton("🌎 PayPal (₱599)", url="https://www.paypal.me/allysantiago100"))
    markup.add(InlineKeyboardButton("📞 Customer Support", url="https://t.me/trendspaymentbot"))
    return markup

@bot.message_handler(content_types=['text'])
def reply_text(message):
    chat_id = message.chat.id
    username = message.from_user.first_name

    if chat_id not in user_interactions:
        user_interactions[chat_id] = 1
    else:
        user_interactions[chat_id] += 1

    reply = chat_with_ellaine(message.text, username)
    bot.send_message(chat_id, reply)

    if user_interactions[chat_id] == 5:
        vip_invite = (
            f"Uy {username}, mukhang enjoy ka sa kwentuhan natin ha! 😘\n"
            "Mas marami pa akong surprises sa **VIP exclusive adult channel** ko. 🔥\n"
            "₱599 lang, sobrang sulit! Tara? 😏"
        )
        bot.send_message(chat_id, vip_invite, reply_markup=payment_keyboard(), parse_mode='Markdown')

@bot.message_handler(commands=['support'])
def send_support_info(message):
    support_message = (
        "Need help or may tanong ka? Chat mo agad ang [Support Account](https://t.me/trendspaymentbot)."
    )
    bot.send_message(message.chat.id, support_message, parse_mode='Markdown')

bot.infinity_polling()
