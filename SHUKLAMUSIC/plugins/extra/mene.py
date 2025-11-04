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
from pyrogram import Client, filters
import requests
from SHUKLAMUSIC import app 

# Define a command handler for the /meme command
@app.on_message(filters.command("meme"))
def meme_command(client, message):
    # API endpoint for random memes
    api_url = "https://meme-api.com/gimme"

    try:
        # Make a request to the API
        response = requests.get(api_url)
        data = response.json()

        # Extract the meme image URL
        meme_url = data.get("url")
        title = data.get("title")

        # Mention the bot username in the caption
        caption = f"{title}\n\nRequest by {message.from_user.mention}\nBot username: @{app.get_me().username}"

        # Send the meme image to the user with the modified caption
        message.reply_photo(
            photo=meme_url,
            caption=caption
        )

    except Exception as e:
        print(f"Error fetching meme: {e}")
        message.reply_text("Sorry, I couldn't fetch a meme at the moment.")
