import certifi
import os

# Fix for the Google Generative AI SSL Certificate issue
os.environ["SSL_CERT_FILE"] = certifi.where()

import chainlit as cl
from src.llm import llm_model
from src.prompt import system_prompt
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


@cl.on_chat_start
async def start_chat():
    """This runs once when the user opens the chat."""

    # 1. Initialize the "messages" list with your Zomato System Prompt
    messages = [
        SystemMessage(content=system_prompt())
    ]

    # 2. Store the messages list in the user's session so the bot remembers the conversation
    cl.user_session.set("messages", messages)

    # 3. Send an initial greeting to the UI
    await cl.Message(content="Welcome to Zomato! 🍕 What can I get started for you today?").send()


@cl.on_message
async def main(message: cl.Message):
    """This runs every time the user types a new message."""

    # 1. Retrieve the chat history (the messages list)
    messages = cl.user_session.get("messages")

    # 2. Add the user's new message to the list
    messages.append(HumanMessage(content=message.content))

    # 3. Load the Gemini LLM
    llm = llm_model()

    # 4. Create an empty message up front, then fill it in as chunks arrive.
    #    This is Chainlit's built-in streaming pattern: stream_token()
    #    appends to the bubble already shown in the UI in real time, so the
    #    answer visibly types itself out - no custom frontend code needed,
    #    Chainlit's own UI handles the rendering.
    response_msg = cl.Message(content="")
    await response_msg.send()

    full_response = ""
    try:
        # astream() (async streaming) instead of ainvoke() - same idea as
        # ainvoke() but yields the response as a series of chunks instead
        # of waiting for the whole thing to be ready.
        async for chunk in llm.astream(messages):
            content = chunk.content

            if not content:
                continue

            # chunk.content is usually a plain string, but with the
            # google-genai SDK's automatic function calling (AFC) path -
            # enabled by default, even when no tools are bound - it can
            # come back as a list of content parts instead (e.g.
            # [{"type": "text", "text": "..."}]). Normalize both shapes
            # to a plain string before appending, otherwise "str + list"
            # raises a TypeError.
            if isinstance(content, list):
                token = "".join(
                    part.get("text", "") if isinstance(part, dict) else str(part)
                    for part in content
                )
            else:
                token = content

            if token:
                full_response += token
                await response_msg.stream_token(token)
    except Exception as e:
        # Log the real error server-side for debugging...
        print(f"Error while streaming response: {e}")
        # ...but only show a generic, friendly message in the UI.
        error_text = "Sorry, something went wrong while getting your response. Please try again."
        if full_response:
            # Partial answer already streamed - append a short note rather
            # than discarding what the user already saw.
            await response_msg.stream_token(f"\n\n_{error_text}_")
        else:
            response_msg.content = error_text
            await response_msg.update()
        return

    # 5. Tell Chainlit the message is complete (finalizes the streamed bubble)
    await response_msg.update()

    # 6. Add the AI's full response to the history so it remembers it for the next turn
    messages.append(AIMessage(content=full_response))

    # 7. Save the updated list back to the session
    cl.user_session.set("messages", messages)