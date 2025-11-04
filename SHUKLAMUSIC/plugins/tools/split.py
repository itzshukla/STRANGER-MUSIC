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
from pyrogram.types import Message
import os

from SHUKLAMUSIC import app

@app.on_message(filters.command("split") & filters.reply)
async def split_file(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.document:
        file_id = message.reply_to_message.document.file_id
        file_name = message.reply_to_message.document.file_name
        
        try:
            num_lines = int(message.text.split(" ")[1])
        except (IndexError, ValueError):
            num_lines = 2

        file_path = await client.download_media(file_id)

        if not os.path.exists(file_path):
            await message.reply("Failed to download the file.")
            return

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            await message.reply(f"Failed to read the file: {str(e)}")
            return

        for i in range(0, len(lines), num_lines):
            split_lines = lines[i:i + num_lines]
            split_file_path = f"split_{i//num_lines + 1}.txt"
            try:
                with open(split_file_path, 'w') as split_file:
                    split_file.writelines(split_lines)
            except Exception as e:
                await message.reply(f"Failed to write the split file: {str(e)}")
                continue
            
            try:
                await client.send_document(chat_id=message.chat.id, document=split_file_path)
            except Exception as e:
                await message.reply(f"Failed to send the split file: {str(e)}")
                continue
            
            os.remove(split_file_path)

        os.remove(file_path)

    else:
        await message.reply("Please reply to a document file to split it /split number of cc")