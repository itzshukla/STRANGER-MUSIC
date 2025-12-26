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
import asyncio
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from SHUKLAMUSIC import app

INFO_TEXT = """
<u><b>ᴜsᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b></u>
<b>● ᴜsᴇʀ ɪᴅ ➠</b> <code>{}</code>
<b>● ᴜsᴇʀɴᴀᴍᴇ ➠</b> <code>@{}</code>
<b>● ᴍᴇɴᴛɪᴏɴ ➠</b> {}
<b>● ᴜsᴇʀ sᴛᴀᴛᴜs ➠</b> {}
<b>● ᴜsᴇʀ ᴅᴄ ɪᴅ ➠</b> {}
"""

async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        x = user.status
        if x == enums.UserStatus.RECENTLY:
            return "recently."
        elif x == enums.UserStatus.LAST_WEEK:
            return "last week."
        elif x == enums.UserStatus.LONG_AGO:
            return "seen long ago."
        elif x == enums.UserStatus.OFFLINE:
            return "User is offline."
        elif x == enums.UserStatus.ONLINE:
            return "User is online."
    except:
        return "**✦ sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !**"

@app.on_message(filters.command(["info", "information", "userinfo", "whois"], prefixes=["/", "!"]))
async def userinfo(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    try:
        # /info <user_id or username>
        if not message.reply_to_message and len(message.command) == 2:
            user_id = message.text.split(None, 1)[1]

        # if reply
        elif message.reply_to_message:
            user_id = message.reply_to_message.from_user.id

        # get user info
        user_info = await app.get_chat(user_id)
        user = await app.get_users(user_id)
        status = await userstatus(user.id)

        id = user_info.id
        dc_id = user.dc_id
        username = user_info.username or "N/A"
        mention = user.mention

        # Choose profile link based on availability of username
        if user.username:
            profile_url = f"https://t.me/{user.username}"
        else:
            profile_url = f"tg://user?id={user.id}"

        await app.send_message(
            chat_id,
            text=INFO_TEXT.format(id, username, mention, status, dc_id),
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👤 ᴜsᴇʀ ᴘʀᴏғɪʟᴇ", url=profile_url)
                    ],
                    [
                        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")
                    ]
                ]
            ),
        )
    except Exception as e:
        await message.reply_text(str(e))
