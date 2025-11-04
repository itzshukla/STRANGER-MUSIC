# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2022 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------
import requests
from SHUKLAMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"

BASE_URL = "https://api.together.xyz/v1/chat/completions"

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message):
    try:
        # Typing action when the bot is processing the message
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            # If no question is asked, send an example message
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt where is tajmahal ?"
            )
        else:
            # Extract the query from the user's message
            query = message.text.split(' ', 1)[1]
            print("Input query:", query)  # Debug input

            # Set up headers with Authorization and Content-Type
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            # Prepare the payload with the correct model and user message
            payload = {
                "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  # Change model if needed
                "messages": [
                    {
                        "role": "user",
                        "content": query  # User's question from the message
                    }
                ]
            }

            # Send the POST request to the API
            response = requests.post(BASE_URL, json=payload, headers=headers)

            # Debugging: print raw response
            print("API Response Text:", response.text)  # Print raw response
            print("Status Code:", response.status_code)  # Check the status code

            # If the response is empty or not successful, handle the error
            if response.status_code != 200:
                await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status code: {response.status_code}")
            elif not response.text.strip():
                await message.reply_text("❍ ᴇʀʀᴏʀ: API se koi valid data nahi mil raha hai. Response was empty.")
            else:
                # Attempt to parse the JSON response
                try:
                    response_data = response.json()
                    print("API Response JSON:", response_data)  # Debug response JSON

                    # Get the assistant's response from the JSON data
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        result = response_data["choices"][0]["message"]["content"]
                        await message.reply_text(
                            f"{result} \n\nＡɴsᴡᴇʀᴇᴅ ʙʏ➛ sᴛʀᴀɴɢᴇʀ-ᴍᴜsɪᴄ ™",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    else:
                        await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
                except ValueError:
                    await message.reply_text("❍ ᴇʀʀᴏʀ: Invalid response format.")
    except Exception as e:
        # Catch any other exceptions and send an error message
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e} ")