import os
import sys
import requests
import logging

# Force Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8133993773:AAG_pRTiU2M_X-nKdD31HrAe-dXeAHuMDKo")
OSINT_API = "https://osint-info.great-site.net/num.php?key=Vishal&phone="

def get_phone_info(phone):
    try:
        response = requests.get(OSINT_API + phone, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

def main():
    logger.info("🚀 Initializing bot...")
    
    try:
        # Try different imports
        try:
            from telegram.ext import Application, CommandHandler, MessageHandler, filters
            logger.info("✅ Using v20+ syntax")
            VERSION = "v20"
        except ImportError:
            try:
                from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
                logger.info("✅ Using v13-20 syntax")
                VERSION = "v13"
            except ImportError:
                from telegram.ext import Updater, CommandHandler, MessageHandler
                logger.info("✅ Using v12 syntax")
                VERSION = "v12"
        
        # V20+ version
        if VERSION == "v20":
            async def start(update, context):
                await update.message.reply_text("🤖 Phone OSINT Bot - Send 10-digit number")
            
            async def handle_message(update, context):
                text = update.message.text.strip()
                if text.isdigit() and len(text) == 10:
                    await update.message.reply_text(f"Searching {text}...")
                    result = get_phone_info(text)
                    if result and result.get('success'):
                        await update.message.reply_text(f"Found {len(result.get('results', []))} records")
                    else:
                        await update.message.reply_text("No data found")
                else:
                    await update.message.reply_text("Send 10-digit number")
            
            app = Application.builder().token(BOT_TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            app.run_polling()
        
        # V13-20 version
        elif VERSION == "v13":
            def start(update, context):
                update.message.reply_text("🤖 Phone OSINT Bot - Send 10-digit number")
            
            def handle_message(update, context):
                text = update.message.text.strip()
                if text.isdigit() and len(text) == 10:
                    update.message.reply_text(f"Searching {text}...")
                    result = get_phone_info(text)
                    if result and result.get('success'):
                        update.message.reply_text(f"Found {len(result.get('results', []))} records")
                    else:
                        update.message.reply_text("No data found")
                else:
                    update.message.reply_text("Send 10-digit number")
            
            updater = Updater(BOT_TOKEN, use_context=True)
            dp = updater.dispatcher
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
            updater.start_polling()
            updater.idle()
        
        # V12 version
        else:
            def start(bot, update):
                bot.send_message(chat_id=update.message.chat_id, text="🤖 Phone OSINT Bot")
            
            def handle_message(bot, update):
                text = update.message.text.strip()
                if text.isdigit() and len(text) == 10:
                    bot.send_message(chat_id=update.message.chat_id, text=f"Searching {text}...")
                    result = get_phone_info(text)
                    if result and result.get('success'):
                        bot.send_message(chat_id=update.message.chat_id, text=f"Found {len(result.get('results', []))} records")
                    else:
                        bot.send_message(chat_id=update.message.chat_id, text="No data found")
                else:
                    bot.send_message(chat_id=update.message.chat_id, text="Send 10-digit number")
            
            from telegram.ext import Updater, CommandHandler, MessageHandler
            updater = Updater(BOT_TOKEN)
            dp = updater.dispatcher
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(MessageHandler(None, handle_message))
            updater.start_polling()
            updater.idle()
            
    except Exception as e:
        logger.error(f"❌ Final error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
