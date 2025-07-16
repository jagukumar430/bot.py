
import telebot
import time
import json
from datetime import datetime, timedelta

# === CONFIGURATION ===
TOKEN = '8107821655:AAGHOB00RdE5F7xmTDHbq7Ayhv-BgwnTlk0'
ADMIN_ID = 5651796937
VIP_USERS = [5651796937]  # Add more VIP user IDs here

DATA_FILE = 'user_data.json'

bot = telebot.TeleBot(TOKEN)

# Load or initialize user data
try:
    with open(DATA_FILE, 'r') as f:
        user_data = json.load(f)
except:
    user_data = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(user_data, f)

def can_use(uid):
    if str(uid) in user_data:
        last_used = datetime.fromtimestamp(user_data[str(uid)]['last_used'])
        if datetime.now() - last_used >= timedelta(days=1):
            return True
        return False
    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    uid = message.from_user.id
    daily = "Unlimited (VIP)" if uid in VIP_USERS else "0/1 used" if not can_use(uid) else "0/1 available"
    text = f'''
👋 Welcome {name}! 🎮🎯

🔥 Ready to boost your likes?
📊 Daily Usage: {daily}
🔄 Resets: Every 24 hours

🎮 How to use:
1️⃣ Join allowed groups
2️⃣ Use: /like <your FF UID> <server>
3️⃣ Get instant likes! ⚡️🌟

🛡 VIP Protection: Never face limits again! Get unlimited access! 🔓

🌟💎 VIP Benefits Preview:
🚀 UNLIMITED daily likes
⚡️ Instant processing
🎯 Priority support
👑 VIP badge

📞 Get VIP Now:
👑 Owner: @NoobVelken
📢 Channel: @PuranaFF
'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['like'])
def like_command(message):
    uid = message.from_user.id
    if uid not in VIP_USERS and not can_use(uid):
        bot.reply_to(message, "❌ Daily limit reached. Try again after 24 hours or upgrade to VIP.")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "⚠️ Please use: /like <FF_UID> <Server>")
        return

    ff_uid = args[1]
    server = args[2]

    # Log usage
    user_data[str(uid)] = {'last_used': time.time()}
    save_data()

    bot.reply_to(message, f'✅ Like request sent!')
bot.reply_to(message, f"UID: 🆔 {ff_uid}")
🌐 Server: {server}
⚡ Processing...")
    bot.send_message(ADMIN_ID, f"📥 Like Request
From: @{message.from_user.username or 'NoUsername'} ({uid})
UID: {ff_uid}
Server: {server}")

bot.polling()
