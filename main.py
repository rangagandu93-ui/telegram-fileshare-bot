import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8291586190:AAHVyRpc7qr-CF2jpSULD1tH1uHj0tgwBq8"
ADMIN_ID = 8057485206

TEMP_FILES = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = update.message.text.split()
    if len(args) > 1 and args[1] == "files":
        if not TEMP_FILES:
            await update.message.reply_text("⚠ No active files right now.")
            return
        
        await update.message.reply_text("📥 Sending available videos...")

        for file_id in TEMP_FILES:
            await update.message.reply_document(document=file_id)

        return

    await update.message.reply_text("👋 Welcome to the bot!")

async def handle_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    
    file = update.message.document or update.message.video
    if not file:
        return

    file_id = file.file_id
    TEMP_FILES.append(file_id)

    await update.message.reply_text(f"✔ Saved! Total files: {len(TEMP_FILES)}")

    async def auto_delete(fid):
        await asyncio.sleep(900)
        if fid in TEMP_FILES:
            TEMP_FILES.remove(fid)

    asyncio.create_task(auto_delete(file_id))

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        TEMP_FILES.clear()
        await update.message.reply_text("♻ Cleared all temporary files!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.ALL, handle_upload))

    app.run_polling()

if __name__ == "__main__":
    main()
  
