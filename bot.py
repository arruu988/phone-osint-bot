import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8133993773:AAG_pRTiU2M_X-nKdD31HrAe-dXeAHuMDKo")
OSINT_API = "https://osint-info.great-site.net/num.php?key=Vishal&phone="

def main():
    logger.info("Starting bot...")
    
    try:
        # TELEGRAM BOT 12 VERSION USE KARO
        from telegram import Bot
        from telegram.ext import Updater, CommandHandler, MessageHandler
        
        # Create bot
        bot = Bot(token=BOT_TOKEN)
        updater = Updater(bot=bot)
        dispatcher = updater.dispatcher
        
        def start(bot, update):
            update.message.reply_text("Phone OSINT Bot Started! Send 10-digit number.")
        
        def handle_message(bot, update):
            text = update.message.text
            if text.isdigit() and len(text) == 10:
                update.message.reply_text(f"Searching: {text}")
                try:
                    response = requests.get(OSINT_API + text, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data and data.get('success'):
                            results = data.get('results', [])
                            reply = f"Found {len(results)} records for {text}"
                            for r in results[:3]:  # First 3 results
                                reply += f"\nName: {r.get('name', 'N/A')}"
                            update.message.reply_text(reply)
                        else:
                            update.message.reply_text("No data found")
                    else:
                        update.message.reply_text("API error")
                except:
                    update.message.reply_text("Error fetching data")
            else:
                update.message.reply_text("Send 10-digit number")
        
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler([], handle_message))
        
        updater.start_polling()
        logger.info("Bot running!")
        updater.idle()
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == '__main__':
    main()
