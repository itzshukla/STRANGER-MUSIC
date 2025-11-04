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
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import *
from SHUKLAMUSIC import app
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.utils import bot_sys_stats
from SHUKLAMUSIC.utils.decorators.language import language
from SHUKLAMUSIC.utils.inline import supp_markup
from config import BANNED_USERS
import random

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


@app.on_message(filters.command("ping", prefixes=["/"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        random.choice(SHASHANK_IMG),
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await SHUKLA.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
