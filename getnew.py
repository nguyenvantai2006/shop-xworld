import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import asyncio
import sys

# Khắc phục lỗi Windows cho máy Dell
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

sent_titles = []

def get_latest_news():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    url = 'https://baomoi.com/tin-moi.epi' 
    
    try:
        r = requests.get(url, headers=headers, timeout=20) # Tăng timeout để tránh lỗi mạng
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Lấy tin theo đúng cấu trúc bạn đã soi
            items = soup.find_all('h3', class_='font-semibold block')
            
            news_list = []
            for item in items[:10]: 
                if item.a:
                    title = item.a.get('title') or item.get_text(strip=True)
                    href = item.a.get('href')
                    link = 'https://baomoi.com' + href if href.startswith('/') else href
                    if title and len(title) > 10:
                        news_list.append((title, link))
            return news_list
    except Exception as e:
        print(f"Đang thử kết nối lại... ({e})")
    return []

async def auto_check_news(context: ContextTypes.DEFAULT_TYPE):
    global sent_titles
    MY_CHANNEL = "@codexworld123456" 
    news_list = get_latest_news()
    
    for title, link in news_list:
        if title not in sent_titles:
            sent_titles.append(title)
            if len(sent_titles) > 50: sent_titles.pop(0)
            
            message = f"🆕 TIN MỚI NHẤT:\n\n{title}\n\n🔗 Xem tại: {link}"
            try:
                await context.bot.send_message(chat_id=MY_CHANNEL, text=message)
                print(f"==> Đã gửi: {title}")
            except Exception as e:
                print(f"Lỗi gửi tin: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Xóa lịch trình cũ để tránh lỗi Updater
    for job in context.job_queue.get_jobs_by_name("news_job"):
        job.schedule_removal()
        
    context.job_queue.run_repeating(auto_check_news, interval=30, first=1, name="news_job")
    await update.message.reply_text("🚀 Bot đã khởi động lại và đang quét tin cho @codexworld123456!")

# Sửa lại phần khởi tạo App ở cuối file
if __name__ == '__main__':
    TOKEN = "8614538054:AAEg6MiwHoagYfLPn0gnbISx7RG6fEgGuKE"
    
    # Thêm cấu hình connect_timeout và read_timeout
    app = ApplicationBuilder().token(TOKEN).connect_timeout(30).read_timeout(30).build()
    
    app.add_handler(CommandHandler("start", start))
    print("Bot đang khởi động lại với cấu hình chống Time out...")
    app.run_polling(drop_pending_updates=True)