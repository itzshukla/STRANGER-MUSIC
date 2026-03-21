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

from pyrogram.types import InlineKeyboardButton
import config
from SHUKLAMUSIC import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID),
            InlineKeyboardButton(text=_["S_B_10"], callback_data="shiv_Shashank"),
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),

InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
        ],
        [InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper")],
    ]
    return buttons