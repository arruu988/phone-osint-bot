import os
import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8133993773:AAG_pRTiU2M_X-nKdD31HrAe-dXeAHuMDKo")
OSINT_API = "https://osint-info.great-site.net/num.php?key=Vishal&phone="

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_phone_info(phone):
    try:
        response = requests.get(OSINT_API + phone, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Error: {e}")
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

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome = f"""
🤖 *Phone OSINT Bot*

Hello {user.first_name}! I can lookup phone information.

Send any 10-digit phone number to start.

Example: `8799610678`

✅ API: Working
⚡ Host: Render
"""
    update.message.reply_text(welcome, parse_mode='Markdown')

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    
    if text.isdigit() and len(text) == 10:
        msg = update.message.reply_text("🔍 Searching...", parse_mode='Markdown')
        result = get_phone_info(text)
        
        if result:
            response = format_info(result, text)
        else:
            response = "❌ API error. Try again later."
        
        update.message.reply_text(response, parse_mode='Markdown')
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
    else:
        update.message.reply_text("📱 Send a 10-digit phone number.", parse_mode='Markdown')

def main():
    logger.info("🚀 Starting bot...")
    
    try:
        # Create updater
        updater = Updater(BOT_TOKEN, use_context=True)
        
        # Get dispatcher
        dp = updater.dispatcher
        
        # Add handlers
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        
        # Start bot
        updater.start_polling()
        logger.info("✅ Bot started successfully!")
        
        # Run until Ctrl+C
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")

if __name__ == '__main__':
    main()
