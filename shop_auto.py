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

# Đã sửa lại Key cho khớp với callback_data
STOCK = {
    "nutrition1": ["NUTRI-111", "NUTRI-222"],
    "shakeee": ["SHAKE-777", "SHAKE-888"],
    "10usd": ["10USD-AAA", "10USD-BBB"]
}

# Danh sách giá tiền chuẩn
PRICES = {
    "nutrition1": "5.000đ", 
    "shakeee": "10.000đ", 
    "10usd": "250.000đ"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Đã sửa lỗi KeyError: '1' bằng cách gọi đúng tên gói trong PRICES
    keyboard = [
        [InlineKeyboardButton(f"🍎 Gói 1000 build ({PRICES['nutrition1']})", callback_data='buy_nutrition1')],
        [InlineKeyboardButton(f"🥤 Gói 4000 build ({PRICES['shakeee']})", callback_data='buy_shakeee')],
        [InlineKeyboardButton(f"⭐ Gói 8000 build ({PRICES['10usd']})", callback_data='buy_10usd')]
    ]
    await update.message.reply_text("🏪 SHOP XWORLD\nChọn gói bạn muốn mua:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    product = query.data.split('_')[1]
    user = query.from_user
    
    # Lấy giá tiền (xóa chữ 'đ' và dấu '.' để lấy số nguyên)
    price_raw = PRICES[product].replace('đ', '').replace('.', '')
    # Tạo nội dung chuyển khoản tự động
    content = f"{product}{user.id}"
    
    # Link tạo QR động từ VietQR
    qr_url = f"https://img.vietqr.io/image/vcb-1051116962-compact2.jpg?amount={price_raw}&addInfo={content}&accountName=NGUYEN%20VAN%20TAI"

    # Gửi ảnh QR cho khách kèm hướng dẫn
    await context.bot.send_photo(
        chat_id=user.id,
        photo=qr_url,
        caption=f"🛒 GÓI: {product.upper()}\n💰 GIÁ: {PRICES[product]}\n\n"
                f"📌 Bạn chỉ cần quét mã QR trên để thanh toán.\n"
                f"⚠️ Nội dung chuyển khoản đã được tạo sẵn, vui lòng không thay đổi!"
    )

    # Thông báo cho bạn (Admin) như cũ
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
        # Kiểm tra kho hàng theo tên gói
        if prod in STOCK and len(STOCK[prod]) > 0:
            code = STOCK[prod].pop(0)
            await context.bot.send_message(chat_id=uid, text=f"✅ Giao dịch thành công!\n🎁 Mã {prod.upper()}: `{code}`")
            await query.edit_message_text(text=f"🚀 ĐÃ DUYỆT!\nKhách: {uid}\nMã: `{code}`")
        else:
            await query.edit_message_text(text=f"❌ Hết hàng gói {prod}!")
    elif data[0] == "can":
        await query.edit_message_text(text=f"🗑️ Đã hủy đơn của {data[1]}")

# --- PHẦN 3: KÍCH HOẠT SONG SONG ---
if __name__ == '__main__':
    # Chạy Flask ở một luồng (thread) riêng để Render không báo lỗi Port
    Thread(target=run_web).start()
    
    # Chạy Bot Telegram
    print("🚀 Bot XWorld đang khởi động chế độ 24/7...")
    app_tg = ApplicationBuilder().token(TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CallbackQueryHandler(handle_buy, pattern='^buy_'))
    app_tg.add_handler(CallbackQueryHandler(handle_admin, pattern='^(pay|can)_'))
    
    app_tg.run_polling(drop_pending_updates=True)