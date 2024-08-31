from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from slowmode import SlowmodeDB
from dotenv import load_dotenv

import os

load_dotenv()
slowdb = SlowmodeDB()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    await update.message.reply_html(
        f"👋 Hello, {user.mention_html()}!\n\n📨 Just send me your message, and i'll post it.\n\n⚠️ I currently support only text messages, no images, videos or etc, but maybe i'll support more soon!",
    )

async def post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_message.chat_id) == os.getenv('CHAT_ID'):
        return
    available = slowdb.check_slowmode(update.effective_user.id)
    if not available[0]:
        time_until = datetime.fromtimestamp(available[1]) + timedelta(hours=1)
        rd = relativedelta(datetime.now(), time_until)
        
        hours = abs(rd.hours)
        minutes = abs(rd.minutes)
        seconds = abs(rd.seconds)
        
        to_wait = "Wait {} hours, {} minutes and {} seconds before posting your message.".format(
            hours, minutes, seconds
        )
        await update.message.reply_html(
            f"❌ You cannot post message yet! " + to_wait
        )
    else:
        try:
            await update.get_bot().send_message(int(os.getenv('CHAT_ID')), update.message.text + '\n\n- whiteboard',
                parse_mode='markdown')
            await update.message.reply_html(
                f"✅ Successfully posted your message!"
            )
            slowdb.set_slowmode(update.effective_user.id, datetime.now().timestamp())
        except Exception as e:
            await update.message.reply_markdown_v2(
                "❌ Couldn't send your message\!\n```\n" + str(e) + '\n```'
            )