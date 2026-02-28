import sys
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. Khắc phục lỗi vòng lặp trên Windows cho máy Dell
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- CẤU HÌNH CHÍNH ---
TOKEN = "8562672356:AAFzMmXa7Q-20tNHFfc_q2XJLZSvijMNDlc"
ADMIN_ID = 6765343155  # ID Telegram của bạn

# 2. KHO HÀNG (Bạn hãy nạp thêm mã thật vào đây)
STOCK = {
    "nutrition1": ["NUTRI-111", "NUTRI-222", "NUTRI-333"],
    "shakeee": ["SHAKE-777", "SHAKE-888", "SHAKE-999"],
    "10usd": ["10USD-AAA", "10USD-BBB"]
}

# 3. GIÁ HIỂN THỊ
PRICES = {
    "nutrition1": "5.000đ",
    "shakeee": "10.000đ",
    "10usd": "250.000đ"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Giao diện Menu cho khách hàng"""
    keyboard = [
        [InlineKeyboardButton(f"🍎 Mua Nutrition1 ({PRICES['nutrition1']})", callback_data='buy_nutrition1')],
        [InlineKeyboardButton(f"🥤 Mua Shakeee ({PRICES['shakeee']})", callback_data='buy_shakeee')],
        [InlineKeyboardButton(f"⭐ Mua 10U.SD ({PRICES['10usd']})", callback_data='buy_10usd')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🏪 SHOP XWORLD TỰ ĐỘNG\n\nVui lòng chọn loại code bạn muốn mua bên dưới:",
        reply_markup=reply_markup
    )

async def handle_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý khi khách bấm nút mua và báo cho Admin"""
    query = update.callback_query
    await query.answer() 
    
    product = query.data.split('_')[1]
    user = query.from_user
    
    payment_text = (
        f"🛒 ĐƠN HÀNG: {product.upper()}\n"
        f"💰 GIÁ: {PRICES[product]}\n\n"
        "💳 THÔNG TIN THANH TOÁN:\n"
        "Ngân hàng: MB BANK\n"
        "STK: [ĐIỀN SỐ TÀI KHOẢN CỦA TÀI VÀO ĐÂY]\n"
        "Chủ TK: NGUYỄN VĂN TÀI\n"
        f"Nội dung CK: `{product} {user.id}`\n\n"
        "⚠️ Chuyển xong hãy đợi Admin xác nhận để nhận code!"
    )

    try:
        await query.edit_message_text(text=payment_text)
    except Exception as e:
        if "Message is not modified" not in str(e):
            print(f"Lỗi cập nhật tin nhắn: {e}")

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🔔 CÓ ĐƠN HÀNG MỚI!\n"
             f"👤 Khách: {user.full_name}\n"
             f"📦 Gói: {product}\n"
             f"🆔 ID Khách: `{user.id}`\n\n"
             f"👉 Lệnh trả code (nhấn vào để copy):\n"
             f"`/pay {user.id} {product}`"
    )

async def pay_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lệnh trả code có khả năng tự sửa lỗi cú pháp"""
    if update.effective_user.id != ADMIN_ID:
        return 

    text = update.message.text.replace('`', '').strip()
    args = text.split() 

    try:
        if len(args) < 3:
            await update.message.reply_text("❌ Cú pháp: /pay [ID] [Gói]")
            return

        user_id = int(args[1])
        product = args[2]
        
        if product in STOCK and len(STOCK[product]) > 0:
            code = STOCK[product].pop(0)
            await context.bot.send_message(
                chat_id=user_id, 
                text=f"✅ GIAO DỊCH THÀNH CÔNG!\n\n🎁 Mã {product.upper()} của bạn: `{code}`"
            )
            await update.message.reply_text(f"✅ ĐÃ TRẢ MÃ: `{code}` cho khách {user_id}.")
        else:
            await update.message.reply_text(f"❌ Kho {product} đang HẾT HÀNG!")
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi: {e}")

# PHẦN KHỞI CHẠY (Phải nằm sát lề trái)
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pay", pay_code))
    app.add_handler(CallbackQueryHandler(handle_buy))
    
    print("🚀 Bot Shop XWorld ĐANG CHẠY... Đừng tắt VSC!")
    app.run_polling(drop_pending_updates=True)