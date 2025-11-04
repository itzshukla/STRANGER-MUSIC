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
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from SHUKLAMUSIC import app
from datetime import datetime
import os
from config import OWNER_ID
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
import asyncio
from datetime import datetime
from time import time
from pyrogram.errors import MessageDeleteForbidden, RPCError
from asyncio import sleep
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.types import Message, User, ChatPrivileges

@app.on_message(filters.command("addme") & filters.user(OWNER_ID))
async def rpromote(client, message: Message):
    try:
        user_id, group_id = message.text.split(maxsplit=2)[1:]
    except ValueError:
        return await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ Group id.")
    
    if user_id.startswith('@'):
        user = await client.get_users(user_id)
        user_id = user.id
        mention = user.mention
    else:
        user = await client.get_users(int(user_id))
        first_name = user.first_name
        user_id = user.id
        mention = f"<a href=tg://user?id={user_id}>{first_name}</a>"
    
    AMBOT = await message.reply_text(f"#ʀᴇᴍᴏᴛᴇ_ᴘʀᴏᴍᴏᴛᴇ\nᴘʀᴏᴍᴏᴛᴇ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")
    
    try:
        await app.promote_chat_member(
            group_id,
            user_id,
            privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
            )
        )
        await app.set_administrator_title(group_id, user_id, "AMBOT OP")
    except RPCError as e:
        await AMBOT.edit(f"An error occurred: {str(e)}")
        return
    
    await AMBOT.edit(f"#ʀᴇᴍᴏᴛᴇ_ᴘʀᴏᴍᴏᴛᴇᴅ\nᴘʀᴏᴍᴏᴛᴇᴅ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")

@app.on_message(filters.command("demoteme") & filters.user(OWNER_ID))
async def rpromote(client, message: Message):
    try:
        user_id, group_id = message.text.split(maxsplit=2)[1:]
    except ValueError:
        return await message.reply_text("ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ Group id.")
    
    if user_id.startswith('@'):
        user = await client.get_users(user_id)
        user_id = user.id
        mention = user.mention
    else:
        user = await client.get_users(int(user_id))
        first_name = user.first_name
        user_id = user.id
        mention = f"<a href=tg://user?id={user_id}>{first_name}</a>"
    
    AMBOT = await message.reply_text(f"#ʀᴇᴍᴏᴛᴇ_ᴘʀᴏᴍᴏᴛᴇ\nᴘʀᴏᴍᴏᴛᴇ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")
    
    try:
        await app.promote_chat_member(
            group_id,
            user_id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            )
        )
    except RPCError as e:
        await AMBOT.edit(f"An error occurred: {str(e)}")
        return
    
    await AMBOT.edit(f"#ʀᴇᴍᴏᴛᴇ_ᴘʀᴏᴍᴏᴛᴇᴅ\nᴘʀᴏᴍᴏᴛᴇᴅ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")


@app.on_message(filters.command("runban") & filters.user(OWNER_ID))
async def runban(client, message: Message, _):
    try:
        user_id, group_id = message.text.split(maxsplit=2)[1:]
    except ValueError:
        return await message.reply_text("Please provide Group id.")
    if user_id.startswith('@'):
        user = await client.get_users(user_id)
        user_id = user.id
        mention = user.mention
    else:
        user = await client.get_users(int(user_id))
        first_name = user.first_name
        user_id = user.id
        mention = f"<a href=tg://user?id={user_id}>{first_name}</a>"
    try:
        AMBOT = await message.reply_text(f"#ʀᴇᴍᴏᴛᴇ_ᴜɴʙᴀɴ\nᴜɴʙᴀɴɪɴɢ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")
        await app.unban_chat_member(group_id, user_id)
    except FloodWait as fw:
        await asyncio.sleep(int(fw.x))
        await AMBOT.edit(f"#ʀᴇᴍᴏᴛᴇ_ᴜɴʙᴀɴ\nᴜɴʙᴀɴɴᴅᴇᴅ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ ᴜɴʙᴀɴɴᴅᴇᴅ\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")
    except Exception as e:
        await AMBOT.edit(f"An error occurred: {str(e)}")

@app.on_message(filters.command("rban") & filters.user(OWNER_ID))
async def rban(client, message: Message, _):
    try:
        user_id, group_id = message.text.split(maxsplit=2)[1:]
    except ValueError:
        return await message.reply_text("Please provide Group id.")
    if user_id.startswith('@'):
        user = await client.get_users(user_id)
        user_id = user.id
        mention = user.mention
    else:
        user = await client.get_users(int(user_id))
        first_name = user.first_name
        user_id = user.id
        mention = f"<a href=tg://user?id={user_id}>{first_name}</a>"
    try:
        AMBOT = await message.reply_text(f"#ʀᴇᴍᴏᴛᴇ_ʙᴀɴ\nʙᴀɴɪɴɢ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")
        await app.ban_chat_member(group_id, user_id)
    except FloodWait as fw:
        await asyncio.sleep(int(fw.x))
        await AMBOT.edit(f"#ʀᴇᴍᴏᴛᴇ_ʙᴀɴ\nʙᴀɴɴᴅᴇᴅ ᴜꜱᴇʀ : {mention}\nᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ɪᴅ : <code>{group_id}</code>\n\nꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ ʙᴀɴɴᴅᴇᴅ\n\nᴘᴏᴡᴇʀ ʙʏ : @SapnaMusicRobot")
    except Exception as e:
        await AMBOT.edit(f"An error occurred: {str(e)}")