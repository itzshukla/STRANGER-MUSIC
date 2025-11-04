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
import pyrogram
import time
from pyrogram import filters
from pyrogram import Client
from SHUKLAMUSIC import app
from SHUKLAMUSIC.misc import SUDOERS


@app.on_message(filters.command("raid", prefixes=".") & SUDOERS)
def spam_command(client, message):
    try:
        # Delete the user's command text
        message.delete()
    except pyrogram.errors.exceptions.FloodWait as e:
        print(f"Error deleting message: {e}")
        pass  # Ignore the deletion error and continue

    # Check if the message is a reply and has text
    if message.reply_to_message and message.reply_to_message.text:
        user_to_tag = message.reply_to_message.from_user.mention()
        command_args = message.text.split(".raid", 1)[-1].strip()

        # Check if the user provided a number of times to spam (e.g., .spam 5 Hello)
        try:
            num_times, text_to_spam = command_args.split(maxsplit=1)
            num_times = int(num_times)
        except ValueError:
            # If not, default to spamming 1 time
            num_times = 1
            text_to_spam = command_args

        for _ in range(num_times):
            # Send the spam message to the Telegram chat and mention the user
            message.reply_text(f"{user_to_tag} **{text_to_spam}**")
            time.sleep(1)  # Add a delay between spam messages
    elif message.reply_to_message:
        # If no text is provided with the spam command, spam the replied user's message
        user_to_tag = message.reply_to_message.from_user.mention()

        for _ in range(5):  # You can adjust the number of spam messages
            message.reply_to_message.reply_text(f"{user_to_tag} **SPAM!**")
            time.sleep(0.2)  # Add a delay between spam messages
    else:
        message.reply_text("Reply to a message and use the .raid command to spam.")
