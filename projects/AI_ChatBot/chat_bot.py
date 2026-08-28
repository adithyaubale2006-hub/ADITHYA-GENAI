import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)


def create_chat():
    """Create and return a new chat session."""
    return client.chats.create(
        model="gemini-3.6-flash"
    )


def chat_with_gemini(chat, message):
    """Send a message to an existing chat session and return the reply text."""
    interaction = chat.send_message(
        message=message
    )
    return interaction.text


def generate_title(first_message):
    """
    Generate a short, ChatGPT-style conversation title from the first user
    message. Uses a standalone one-off call (not the ongoing chat session)
    so it doesn't pollute the conversation history.
    """
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=(
                "Summarize the following message as a short chat title. "
                "Max 5 words. No quotes, no punctuation at the end, "
                "no preamble -- output only the title.\n\n"
                f"Message: {first_message}"
            )
        )
        title = (response.text or "").strip().strip('"\'')
        return title[:50] if title else "New chat"
    except Exception:
        # Fall back to a truncated version of the message if the
        # title-generation call fails for any reason
        fallback = first_message.strip().replace("\n", " ")
        return (fallback[:40] + "...") if len(fallback) > 40 else (fallback or "New chat")