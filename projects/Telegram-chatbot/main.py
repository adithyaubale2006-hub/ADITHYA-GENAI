import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from google import genai
from aiogram import Bot, Dispatcher, types, executor

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MODEL_NAME = "gemini-3.6-flash"

client = genai.Client(api_key=GEMINI_API_KEY)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

last_response = ""


@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hello! I am your JARVIS AI bot. How can I assist you today?")


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    global last_response
    last_response = ""
    await message.reply("Cleared the previous context. You can start a new conversation now.")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    await message.reply("/start - begin\n/help - this message\n/clear - reset context\nJust text me anything else!")


@dispatcher.message_handler()
async def gemini_chat(message: types.Message):
    global last_response

    contents = []
    if last_response:
        contents.append({"role": "model", "parts": [{"text": last_response}]})#role of the model's last response
    contents.append({"role": "user", "parts": [{"text": message.text}]})#our query

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=contents)
        reply_text = response.text or "No response from Gemini."
    except Exception as e:
        reply_text = f"Error talking to Gemini: {e}"

    last_response = reply_text
    print(f">>> Gemini:\n\t{reply_text}")
    await message.reply(reply_text)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=False)
    #the skip_updates parameter is set to False to ensure that the bot processes all messages, 
    # including those sent while it was offline.