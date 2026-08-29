import logging
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
#print(TELEGRAM_BOT_TOKEN)

#Configure logging
logging.basicConfig(level=logging.INFO)

#Initializer Botdispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help']) #{YOU CAN INSERT ANY COMMAND name,....}
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm JARVISBot!\nPowered by aiogram.")


if __name__ == '__main__':
    #Start polling
    executor.start_polling(dp, skip_updates=True)