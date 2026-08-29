# Telegram Echo Bot

A simple Telegram echo bot built with Python and the aiogram library. This bot listens for incoming messages and replies with the exact same text, serving as a foundational template for building more complex Telegram bots.

## Prerequisites

- Python 3.7 or higher
- A Telegram Bot Token (obtained from BotFather on Telegram)

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory in your terminal.
3. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
4. Install the required dependencies. Note that this project strictly requires aiogram version 2.x:
   pip install aiogram==2.25.1

## Configuration

1. Open the `research/echo_bot.py` file in your text editor.
2. Locate the token variable and replace the placeholder with your actual Telegram bot token:
   API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

## Usage

Start the bot by running the script from your terminal:

python research/echo_bot.py

Once the script is actively running, open the Telegram app, navigate to your bot's chat, and send a message. The bot will immediately read your message and echo it back to you. To stop the bot, press Ctrl+C in your terminal.
