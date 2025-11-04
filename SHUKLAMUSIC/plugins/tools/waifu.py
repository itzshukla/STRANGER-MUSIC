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
from pyrogram import filters
from pyrogram.types import Message
from SHUKLAMUSIC import app


@app.on_message(filters.command("waifu"))
async def waifu_command_handler(_, message: Message):
    try:
        args = message.text.split(maxsplit=1)
        tag = args[1] if len(args) > 1 else "maid"

        waifu_data = get_waifu_data(tag)

        if waifu_data and 'images' in waifu_data and waifu_data['images']:
            image = waifu_data['images'][0]
            await message.reply_photo(
                photo=image["url"],
                caption=f"🌸 ʜᴇʀᴇ'ꜱ ʏᴏᴜʀ ᴡᴀɪꜰᴜ ({tag})"
            )
        else:
            await message.reply_text("❌ ɴᴏ ᴡᴀɪꜰᴜꜱ ꜰᴏᴜɴᴅ ᴡɪᴛʜ ᴛʜᴀᴛ ᴛᴀɢ.")

    except Exception as e:
        await message.reply_text(f"⚠️ ᴇʀʀᴏʀ: `{str(e)}`")


def get_waifu_data(tag):
    try:
        response = requests.get(
            "https://api.waifu.im/search",
            params={
                "included_tags": tag,
                "height": ">=2000"
            }
        )
        if response.status_code == 200:
            return response.json()
    except:
        return None