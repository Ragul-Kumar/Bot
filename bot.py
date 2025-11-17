import os
import asyncio
import logging
from telegram import Update
from telegram.error import TimedOut
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Put your token here (or load from env)
BOT_TOKEN = "Your API Token Here"

# Local video files (same folder)
VIDEO_FILES = ["video1.mp4", "video2.mp4", "video3.mp4"]

# Max file size for bot uploads (Telegram bots max ~50 MB)
MAX_UPLOAD_BYTES = 50 * 1024 * 1024


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send 'hi' to get the video(s).")


async def reply_with_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip().lower()
    if text != "hi":
        return

    await update.message.reply_text("Preparing to send videos...")

    for path in VIDEO_FILES:
        if not os.path.isfile(path):
            await update.message.reply_text(f"❌ File not found: {path}")
            continue

        size = os.path.getsize(path)
        logger.info("File %s size = %.2f MB", path, size / (1024 * 1024))

        if size > MAX_UPLOAD_BYTES:
            await update.message.reply_text(
                f"⚠️ '{os.path.basename(path)}' is {size//(1024*1024)} MB — larger than the 50 MB bot upload limit.\n"
                "Either compress it (ffmpeg) or host it at a URL and I'll send the link."
            )
            continue

        # Try sending with 3 attempts and backoff
        for attempt in range(1, 4):
            try:
                logger.info("Sending %s (attempt %d)", path, attempt)
                with open(path, "rb") as f:
                    # no 'timeout' kwarg here
                    await update.message.reply_video(f, supports_streaming=True)
                logger.info("Sent %s", path)
                break
            except TimedOut:
                logger.warning("TimedOut sending %s (attempt %d)", path, attempt)
                if attempt == 3:
                    await update.message.reply_text("⏳ Upload timed out after 3 attempts.")
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.exception("Failed sending %s: %s", path, e)
                await update.message.reply_text(f"Failed to send {os.path.basename(path)}: {e}")
                break


def main():
    if BOT_TOKEN.startswith("REPLACE") or BOT_TOKEN.strip() == "":
        raise RuntimeError("Set BOT_TOKEN in this file before running (or change code to read env).")

    # Force HTTP/1.1 can improve reliability for some uploads:
    app = ApplicationBuilder().token(BOT_TOKEN).http_version("1.1").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply_with_videos))

    logger.info("Bot is starting (polling)...")
    # run_polling timeout controls the long-polling read timeout; set high for slow networks
    app.run_polling(timeout=300)


if __name__ == "__main__":
    main()
