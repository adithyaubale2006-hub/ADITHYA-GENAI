# Telegram Echo Bot

A simple Telegram Echo Bot built with Python and the aiogram library. The bot listens for incoming messages and replies with the exact same text.

This project serves as a foundational template for understanding Telegram bot development and can be extended to build more advanced applications such as AI-powered chatbots.

## Features

* Receives messages from Telegram users
* Replies with the exact same message
* Built using Python and aiogram
* Simple and beginner-friendly implementation
* Provides a foundation for building advanced Telegram bots

## Technologies Used

* Python
* Telegram Bot API
* aiogram 2.25.1

## Prerequisites

Before setting up the project, ensure that you have the following installed:

* Git
* Git Bash
* Anaconda or Miniconda
* Python 3.7 or higher
* A Telegram Bot Token obtained from BotFather

## Project Setup Using Git Bash and Conda

### 1. Clone the Repository

Open Git Bash and clone the repository:

```bash
git clone <your-repository-url>
```

### 2. Navigate to the Project Directory

```bash
cd Telegram-Echo-Bot
```

Replace `Telegram-Echo-Bot` with the actual name of your repository if it is different.

### 3. Create a Conda Environment

Create a dedicated Conda environment for the project:

```bash
conda create --name telegram-bot python=3.10
```

Activate the environment:

```bash
conda activate telegram-bot
```

### 4. Install Dependencies

Install the required version of aiogram:

```bash
pip install aiogram==2.25.1
```

Alternatively, if a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

## Configuration

Open the following file:

```text
research/echo_bot.py
```

Locate the Telegram bot token variable:

```python
API_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

Replace the placeholder with your Telegram Bot Token obtained from BotFather.

Example:

```python
API_TOKEN = "YOUR_ACTUAL_BOT_TOKEN"
```

Important: Do not share your Telegram bot token publicly or upload it directly to GitHub. If the token is exposed, regenerate it immediately through BotFather.

## Running the Bot

Make sure the Conda environment is activated:

```bash
conda activate telegram-bot
```

Run the bot:

```bash
python research/echo_bot.py
```

Once the script is running:

1. Open Telegram.
2. Navigate to your bot.
3. Send any text message.
4. The bot will reply with the exact same text.

To stop the bot, press:

```text
Ctrl + C
```

## Example

**User**

```text
Hello Bot
```

**Bot**

```text
Hello how may i assist you Today?
```

## Project Structure

```text
Telegram-chatbot/
│
├── main.py
├── echo_bot.py
├── test.py
├── requirements.txt
└── README.md
```

## How It Works

```text
User sends a message
        |
        v
Telegram Bot receives the message
        |
        v
Python application processes the message
using aiogram
        |
        v
The bot sends the same message back
        |
        v
User receives the echoed message
```

## Future Improvements

This project can be extended with:

* Command handling
* Environment variable configuration
* Google Gemini API integration
* AI-generated responses
* Conversation memory
* User authentication

## Learning Objective

The purpose of this project is to understand the fundamentals of Telegram bot development, including:

* Creating a Telegram bot
* Using the Telegram Bot API
* Receiving user messages
* Processing incoming updates
* Sending responses using aiogram

These concepts provide a foundation for developing more advanced applications, including AI-powered Telegram chatbots and agent-based systems.

## Author

Adithya Ubale

B.Tech Student | Generative AI


