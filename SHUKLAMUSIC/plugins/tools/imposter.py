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
from pyrogram import filters
import random
from pyrogram.types import Message
from SHUKLAMUSIC import app
from SHUKLAMUSIC.plugins.tools.pretenderdb import (
    impo_off, impo_on, check_pretender,
    add_userdata, get_userdata, usr_data
)
from SHUKLAMUSIC.utils.admin_filters import admin_filter

SHASHANK_IMG = [
"https://graph.org/file/f76fd86d1936d45a63c64.jpg",
"https://graph.org/file/69ba894371860cd22d92e.jpg",
"https://graph.org/file/67fde88d8c3aa8327d363.jpg",
"https://graph.org/file/3a400f1f32fc381913061.jpg",
"https://graph.org/file/a0893f3a1e6777f6de821.jpg",
"https://graph.org/file/5a285fc0124657c7b7a0b.jpg",
"https://graph.org/file/25e215c4602b241b66829.jpg",
"https://graph.org/file/a13e9733afdad69720d67.jpg",
"https://graph.org/file/692e89f8fe20554e7a139.jpg",
"https://graph.org/file/db277a7810a3f65d92f22.jpg",
"https://graph.org/file/a00f89c5aa75735896e0f.jpg",
"https://graph.org/file/f86b71018196c5cfe7344.jpg",
"https://graph.org/file/a3db9af88f25bb1b99325.jpg",
"https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
"https://graph.org/file/84de4b440300297a8ecb3.jpg",
"https://graph.org/file/84e84ff778b045879d24f.jpg",
"https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
"https://graph.org/file/df11d8257613418142063.jpg",
"https://graph.org/file/9e23720fedc47259b6195.jpg",
"https://graph.org/file/826485f2d7db6f09db8ed.jpg",
"https://graph.org/file/ff3ad786da825b5205691.jpg",
"https://graph.org/file/52713c9fe9253ae668f13.jpg",
"https://graph.org/file/8f8516c86677a8c91bfb1.jpg",
"https://graph.org/file/6603c3740378d3f7187da.jpg"
]

@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    if message.sender_chat or not await check_pretender(message.chat.id):
        return
    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    usernamebefore, first_name, lastname_before = await get_userdata(message.from_user.id)
    msg = ""
    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""
**🔓 ᴘʀᴇᴛᴇɴᴅᴇʀ ᴅᴇᴛᴇᴄᴛᴇᴅ 🔓**
━━━━━━━━━━━━━━━  
**🍊 ɴᴀᴍᴇ** : {message.from_user.mention}
**🍅 ᴜsᴇʀ ɪᴅ** : {message.from_user.id}
━━━━━━━━━━━━━━━  \n
"""
    if usernamebefore != message.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else "NO USERNAME"
        usernameafter = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "NO USERNAME"
        )
        msg += """
**🐻‍❄️ ᴄʜᴀɴɢᴇᴅ ᴜsᴇʀɴᴀᴍᴇ 🐻‍❄️**
━━━━━━━━━━━━━━━  
**🎭 ғʀᴏᴍ** : {bef}
**🍜 ᴛᴏ** : {aft}
━━━━━━━━━━━━━━━  \n
""".format(bef=usernamebefore, aft=usernameafter)
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if first_name != message.from_user.first_name:
        msg += """
**🪧 ᴄʜᴀɴɢᴇs ғɪʀsᴛ ɴᴀᴍᴇ 🪧**
━━━━━━━━━━━━━━━  
**🔐 ғʀᴏᴍ** : {bef}
**🍓 ᴛᴏ** : {aft}
━━━━━━━━━━━━━━━  \n
""".format(
            bef=first_name, aft=message.from_user.first_name
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if lastname_before != message.from_user.last_name:
        lastname_before = lastname_before or "NO LAST NAME"
        lastname_after = message.from_user.last_name or "NO LAST NAME"
        msg += """
**🪧 ᴄʜᴀɴɢᴇs ʟᴀsᴛ ɴᴀᴍᴇ 🪧**
━━━━━━━━━━━━━━━  
**🚏ғʀᴏᴍ** : {bef}
**🍕 ᴛᴏ** : {aft}
━━━━━━━━━━━━━━━  \n
""".format(
            bef=lastname_before, aft=lastname_after
        )
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if msg != "":
        await message.reply_photo(random. choice(SHASHANK_IMG), caption=msg)


@app.on_message(filters.group & filters.command("imposter") & ~filters.bot & ~filters.via_bot & admin_filter)
async def set_mataa(_, message: Message):
    if len(message.command) == 1:
        return await message.reply("ᴅᴇᴛᴇᴄᴛ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴇʀs **ᴜsᴀɢᴇ:** `/imposter enable|disable`")
    if message.command[1] == "enable":
        cekset = await impo_on(message.chat.id)
        if cekset:
            await message.reply("**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
        else:
            await impo_on(message.chat.id)
            await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}")
    elif message.command[1] == "disable":
        cekset = await impo_off(message.chat.id)
        if not cekset:
            await message.reply("**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
        else:
            await impo_off(message.chat.id)
            await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}")
    else:
        await message.reply("**ᴅᴇᴛᴇᴄᴛ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴇʀs ᴜsᴀɢᴇ : ᴘʀᴇᴛᴇɴᴅᴇʀ ᴏɴ|ᴏғғ**")