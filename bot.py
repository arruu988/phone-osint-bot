import os
import sys
import requests
import logging

# Logger setup - PEHLE HI
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)  # Console par print karega
    ]
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8133993773:AAG_pRTiU2M_X-nKdD31HrAe-dXeAHuMDKo")
OSINT_API = "https://osint-info.great-site.net/num.php?key=Vishal&phone="

logger.info("🚀 Script started...")
logger.info(f"Token length: {len(BOT_TOKEN) if BOT_TOKEN else 0}")

def get_phone_info(phone):
    try:
        response = requests.get(OSINT_API + phone, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

def format_info(data, phone):
    if not data or not data.get('success'):
        return "❌ No information found."
    
    results = data.get('results', [])
    text = f"📱 *Phone Lookup Results*\nNumber: `{phone}`\nRecords: {len(results)}\n\n"
    
    for i, record in enumerate(results, 1):
        address = record.get('address', 'N/A').replace('!', ', ')
        text += f"""
*Record #{i}*
Name: {record.get('name', 'N/A')}
Father: {record.get('father_name', 'N/A')}
Mobile: {record.get('mobile', 'N/A')}
Address: {address}
Alternate: {record.get('alternate_mobile', 'N/A')}
Telecom: {record.get('telecom_circle', 'N/A')}
ID: {record.get('id_number', 'N/A')}
━━━━━━━━━━━━━━━━━━
"""
    return text

def main():
    logger.info("🚀 Starting bot main function...")
    
    try:
        # Import andar kar rahe hain taki error clear mile
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
        
        logger.info("✅ Imports successful")
        
        # Create updater
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        # Start command
        def start(update, context):
            user = update.message.from_user
            welcome = f"""🤖 *Phone OSINT Bot*

Hello {user.first_name}! Send 10-digit phone number."""
            update.message.reply_text(welcome, parse_mode='Markdown')
        
        # Message handler
        def handle_message(update, context):
            text = update.message.text.strip()
            if text.isdigit() and len(text) == 10:
                update.message.reply_text(f"🔍 Searching {text}...", parse_mode='Markdown')
                result = get_phone_info(text)
                if result:
                    response = format_info(result, text)
                else:
                    response = "❌ API error."
                update.message.reply_text(response, parse_mode='Markdown')
            else:
                update.message.reply_text("📱 Send 10-digit number.")
        
        # Add handlers
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        
        # Start polling
        logger.info("✅ Starting polling...")
        updater.start_polling()
        logger.info("🤖 Bot is now running!")
        
        # Keep running
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Main error: {e}", exc_info=True)
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
