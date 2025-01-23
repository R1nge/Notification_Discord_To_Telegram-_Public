import asyncio
import discord
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import os
import keyboard
from time import sleep

TELEGRAM_TOKEN = ''  # Create a bot using botfather, use its token
DISCORD_TOKEN = '  # Login using browser, find /api/v9/quests/@me request
TELEGRAM_CHAT_ID = ''  # Replace with your Telegram chat ID
TIMESTAMP_FILE = 'last_launch_timestamp.txt'

def read_last_timestamp():
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_last_timestamp(timestamp):
    with open(TIMESTAMP_FILE, 'w') as f:
        f.write(timestamp)


class TelegramManager:
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_message(self, text):
        await self.bot.send_message(chat_id=self.chat_id, text=text)

telegram_manager = TelegramManager(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text='Bot is running.')

async def run_telegram_bot() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try:
            last_timestamp = read_last_timestamp()
            
            if last_timestamp is None:
                current_timestamp = datetime.now().isoformat()
                save_last_timestamp(current_timestamp)
                last_timestamp = current_timestamp
                   
            print(last_timestamp)
            
            # Example
            await self.sync_all_messages('Title',1111111111111111111, last_timestamp)

            current_timestamp = datetime.now().isoformat()
            save_last_timestamp(current_timestamp)
        except Exception as e:
            print(f'An error occurred: {e}')      

    async def sync_message(self, message: str, title: str, id: int):
        if message.channel.id == id:
            print(f'Message from {message.author}: \n {message.content}')
            await telegram_manager.send_message(f'In {title} from {message.author}: \n{message.content}')
            
            
    async def sync_all_messages(self, title: str, channel_id: int, timestamp: str):
        channel = self.get_channel(channel_id)
        if channel:
            print(f'Syncing messages from {title}')
            print(f'Timestamp: {timestamp}')
            since = datetime.fromisoformat(timestamp)
            print(f'Since: {since}')
            async for message in channel.history(after=since):
                print(f'Message from {message.content}')
                await telegram_manager.send_message(f'In {title} from {message.author}: \n{message.content}')
                sleep(1)
        else:
            print('Channel not found or bot does not have access to the channel.')

    async def on_message(self, message):
        # Example
        await self.sync_message(message, 'Title', 1111111111111111111)

async def main() -> None:
    try:
        discord_client = MyClient()
        await asyncio.gather(
            await discord_client.start(DISCORD_TOKEN),
            await run_telegram_bot()
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        keyboard.read_event()
            

if __name__ == '__main__':
    asyncio.run(main())
