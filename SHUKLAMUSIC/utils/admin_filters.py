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
from pyrogram.types import Message, CallbackQuery
from SHUKLAMUSIC.utils.admin_check import is_admin, is_group_owner
from SHUKLAMUSIC.misc import SUDOERS
from config import OWNER_ID


def sudo_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    return bool(
        (
            (msg.from_user and msg.from_user.id in SUDOERS)
            or (msg.sender_chat and msg.sender_chat.id in SUDOERS)
        )
        and not getattr(msg, "edit_date", False)
    )

sudo_filter = filters.create(func=sudo_filter_func, name="SudoUsersFilter")

async def admin_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    if getattr(msg, "edit_date", False):
        return False
    return await is_admin(msg)

admin_filter = filters.create(func=admin_filter_func, name="AdminFilter")

async def group_owner_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    if getattr(msg, "edit_date", False):
        return False
    return await is_group_owner(msg)

owner_filter = filters.create(func=group_owner_filter_func, name="GroupOwnerFilter")

def bot_owner_filter_func(_, __, obj: Message | CallbackQuery) -> bool:
    msg = obj.message if isinstance(obj, CallbackQuery) else obj
    return (
        msg.from_user
        and msg.from_user.id == OWNER_ID
        and not getattr(msg, "edit_date", False)
    )

dev_filter = filters.create(func=bot_owner_filter_func, name="BotOwnerFilter")