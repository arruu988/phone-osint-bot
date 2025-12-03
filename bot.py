import os
import sys
import requests
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8133993773:AAG_pRTiU2M_X-nKdD31HrAe-dXeAHuMDKo")
OSINT_API = "https://osint-info.great-site.net/num.php?key=Vishal&phone="

logger.info("🚀 Starting bot...")

def main():
    try:
        # Version 20+ ke liye
        from telegram.ext import Application, CommandHandler, MessageHandler, filters
        
        # Bot functions
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
        
        async def start(update, context):
            user = update.message.from_user
            welcome = f"""🤖 *Phone OSINT Bot*

Hello {user.first_name}! Send 10-digit phone number.

Example: `8799610678`"""
            await update.message.reply_text(welcome, parse_mode='Markdown')
        
        async def handle_message(update, context):
            text = update.message.text.strip()
            if text.isdigit() and len(text) == 10:
                msg = await update.message.reply_text(f"🔍 Searching {text}...", parse_mode='Markdown')
                result = get_phone_info(text)
                if result:
                    response = format_info(result, text)
                else:
                    response = "❌ API error. Try again later."
                await update.message.reply_text(response, parse_mode='Markdown')
                await msg.delete()
            else:
                await update.message.reply_text("📱 Send a 10-digit phone number.", parse_mode='Markdown')
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Run bot
        logger.info("✅ Bot starting...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
