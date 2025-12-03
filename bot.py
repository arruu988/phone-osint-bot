import os
import requests
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8133993773:AAG_pRTiU2M_X-nKdD31HrAe-dXeAHuMDKo")
OSINT_API = "https://osint-info.great-site.net/num.php?key=Vishal&phone="

def get_phone_info(phone):
    """Fetch phone information from API"""
    try:
        response = requests.get(OSINT_API + phone, timeout=10)
        logger.info(f"API Response Status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

def format_info(data, phone):
    """Format API response into readable text"""
    if not data or not data.get('success'):
        return "❌ No information found for this number."
    
    results = data.get('results', [])
    if not results:
        return "❌ No records found."
    
    text = f"📱 *Phone Lookup Results*\nNumber: `{phone}`\nRecords Found: {len(results)}\n\n"
    
    for i, record in enumerate(results, 1):
        address = record.get('address', 'N/A').replace('!', ', ')
        text += f"""*Record #{i}*
👤 Name: {record.get('name', 'N/A')}
👨 Father: {record.get('father_name', 'N/A')}
📞 Mobile: {record.get('mobile', 'N/A')}
🏠 Address: {address}
📱 Alternate: {record.get('alternate_mobile', 'N/A')}
📡 Telecom: {record.get('telecom_circle', 'N/A')}
🆔 ID: {record.get('id_number', 'N/A')}
━━━━━━━━━━━━━━━━━━━━━━
"""
    return text

def start(update, context):
    """Handle /start command"""
    user = update.message.from_user
    welcome = f"""
🤖 *Phone OSINT Bot*

Hello *{user.first_name}*! I can lookup phone information.

📍 *How to use:*
Simply send me any 10-digit Indian phone number.

📌 *Example:* `8799610678`

⚡ *Features:*
• Name, Father's Name
• Address Details  
• Telecom Operator
• Alternate Numbers
• ID Information

✅ *Status:* Online
🏠 *Host:* Render.com
"""
    update.message.reply_text(welcome, parse_mode='Markdown')

def handle_message(update, context):
    """Handle incoming messages"""
    text = update.message.text.strip()
    
    # Check if it's a 10-digit number
    if text.isdigit() and len(text) == 10:
        # Send searching message
        searching_msg = update.message.reply_text(
            f"🔍 *Searching for:* `{text}`\nPlease wait...",
            parse_mode='Markdown'
        )
        
        # Get phone info
        result = get_phone_info(text)
        
        # Send result
        if result:
            response = format_info(result, text)
        else:
            response = "❌ Sorry, API is currently unavailable. Please try again later."
        
        update.message.reply_text(response, parse_mode='Markdown')
        
        # Delete searching message
        try:
            context.bot.delete_message(
                chat_id=update.message.chat_id,
                message_id=searching_msg.message_id
            )
        except:
            pass
    else:
        update.message.reply_text(
            "📱 *Invalid Input!*\nPlease send a valid 10-digit phone number.\n\nExample: `9876543210`",
            parse_mode='Markdown'
        )

def error(update, context):
    """Log errors"""
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    """Start the bot"""
    logger.info("🚀 Starting Phone OSINT Bot...")
    
    try:
        # Version 13.15 mein ParseMode import nahi karna padta
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
        
        logger.info("✅ Libraries imported successfully")
        
        # Create the Updater
        updater = Updater(BOT_TOKEN, use_context=True)
        
        # Get the dispatcher to register handlers
        dp = updater.dispatcher
        
        # Add command handlers
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", start))
        
        # Add message handler
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        
        # Log all errors
        dp.add_error_handler(error)
        
        # Start the Bot
        logger.info("✅ Bot initialized, starting polling...")
        updater.start_polling()
        
        logger.info("🤖 Bot is now running! Press Ctrl+C to stop.")
        
        # Run the bot until you press Ctrl-C
        updater.idle()
        
    except ImportError as e:
        logger.error(f"❌ Import Error: {e}")
        logger.error("Please install: pip install python-telegram-bot==13.15 requests==2.31.0")
    except Exception as e:
        logger.error(f"❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
