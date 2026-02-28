import os
import sys
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- PHẦN 1: SERVER WEB ĐỂ GIỮ BOT ONLINE 24/7 ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot XWorld is Running 24/7"

def run_web():
    # Render yêu cầu chạy trên port được cấp phát
    port = int(os.environ.get('PORT', 5000))
    app_web.run(host='0.0.0.0', port=port)

# --- PHẦN 2: LOGIC BOT TELEGRAM CỦA TÀI ---
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN = "8562672356:AAFzMmXa7Q-20tNHFfc_q2XJLZSvijMNDlc"
ADMIN_ID = 6765343155 

STOCK = {
    "1": ["NUTRI-111", "NUTRI-222"],
    "2": ["SHAKE-777", "SHAKE-888"],
    "3": ["10USD-AAA", "10USD-BBB"]
}

PRICES = {"nutrition1": "5.000đ", "shakeee": "10.000đ", "10usd": "250.000đ"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"🍎 Gói 1000 build ({PRICES['1']})", callback_data='buy_nutrition1')],
        [InlineKeyboardButton(f"🥤 Gói 4000 build ({PRICES['2']})", callback_data='buy_shakeee')],
        [InlineKeyboardButton(f"⭐ Gói 8000 build ({PRICES['3']})", callback_data='buy_10usd')]
    ]
    await update.message.reply_text("🏪 SHOP XWORLD\nChọn gói bạn muốn mua:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = query.data.split('_')[1]
    user = query.from_user
    
    await query.edit_message_text(
        text=f"🛒 GÓI: {product.upper()}\n💰 GIÁ: {PRICES[product]}\n\n"
             f"💳 VIETCOMBANK: NGUYỄN VĂN TÀI\nSTK: 1051116962\n"
             f"Nội dung: `{product} {user.id}`"
    )

    admin_kb = [[
        InlineKeyboardButton("✅ Duyệt", callback_data=f"pay_{user.id}_{product}"),
        InlineKeyboardButton("❌ Hủy", callback_data=f"can_{user.id}")
    ]]
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔔 ĐƠN MỚI: {user.full_name}\n📦 Gói: {product}\n🆔 ID: `{user.id}`",
        reply_markup=InlineKeyboardMarkup(admin_kb)
    )

async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split('_')
    
    if data[0] == "pay":
        uid, prod = int(data[1]), data[2]
        if prod in STOCK and STOCK[prod]:
            code = STOCK[prod].pop(0)
            await context.bot.send_message(chat_id=uid, text=f"✅ Giao dịch thành công!\n🎁 Mã {prod.upper()}: `{code}`")
            await query.edit_message_text(text=f"🚀 ĐÃ DUYỆT!\nKhách: {uid}\nMã: `{code}`")
        else:
            await query.edit_message_text(text=f"❌ Hết hàng gói {prod}!")
    elif data[0] == "can":
        await query.edit_message_text(text=f"🗑️ Đã hủy đơn của {data[1]}")

# --- PHẦN 3: KÍCH HOẠT SONG SONG ---
if __name__ == '__main__':
    # Chạy Flask ở một luồng (thread) riêng để không làm kẹt Bot
    Thread(target=run_web).start()
    
    # Chạy Bot Telegram
    print("🚀 Bot XWorld đang khởi động chế độ 24/7...")
    app_tg = ApplicationBuilder().token(TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CallbackQueryHandler(handle_buy, pattern='^buy_'))
    app_tg.add_handler(CallbackQueryHandler(handle_admin, pattern='^(pay|can)_'))
    
    app_tg.run_polling(drop_pending_updates=True)