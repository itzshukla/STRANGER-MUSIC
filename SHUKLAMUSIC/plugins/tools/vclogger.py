import asyncio
from logging import getLogger
from typing import Dict, Set
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from pyrogram.raw import functions
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils.database import get_assistant

LOGGER = getLogger(__name__)


VC_LOGGER_STATE = {}  # Stores On/Off per chat

def is_enabled(chat_id: int) -> bool:
    return VC_LOGGER_STATE.get(chat_id, False)

def enable_logger(chat_id: int):
    VC_LOGGER_STATE[chat_id] = True

def disable_logger(chat_id: int):
    VC_LOGGER_STATE[chat_id] = False



vc_active_users: Dict[int, Set[int]] = {}
active_vc_chats: Set[int] = set()



async def get_group_call_participants(userbot, peer):
    try:
        full_chat = await userbot.invoke(
            functions.channels.GetFullChannel(channel=peer)
        )
        if not hasattr(full_chat.full_chat, "call") or not full_chat.full_chat.call:
            return []

        call = full_chat.full_chat.call
        participants = await userbot.invoke(
            functions.phone.GetGroupParticipants(
                call=call, ids=[], sources=[], offset="", limit=100
            )
        )
        return participants.participants

    except Exception as e:
        if any(
            x in str(e).upper()
            for x in ["GROUPCALL_NOT_FOUND", "CALL_NOT_FOUND", "NO_GROUPCALL"]
        ):
            return []
        LOGGER.error(f"Error fetching VC participants: {e}")
        return []



async def monitor_vc_chat(chat_id):
    if not is_enabled(chat_id):
        return

    userbot = await get_assistant(chat_id)
    if not userbot:
        return

    while chat_id in active_vc_chats:
        if not is_enabled(chat_id):
            break

        try:
            peer = await userbot.resolve_peer(chat_id)
            participants_list = await get_group_call_participants(userbot, peer)

            new_users = set()
            for p in participants_list:
                if hasattr(p, "peer") and hasattr(p.peer, "user_id"):
                    new_users.add(p.peer.user_id)

            current_users = vc_active_users.get(chat_id, set())

            joined = new_users - current_users
            left = current_users - new_users

            tasks = []
            for user_id in joined:
                tasks.append(
                    handle_user_join(chat_id, user_id, userbot)
                )
            for user_id in left:
                tasks.append(
                    handle_user_leave(chat_id, user_id, userbot)
                )

            if tasks:
                await asyncio.gather(*tasks)

            vc_active_users[chat_id] = new_users

        except Exception as e:
            LOGGER.error(f"VC Monitor Error [{chat_id}]: {e}")

        await asyncio.sleep(2)



async def check_and_monitor_vc(chat_id):
    if not is_enabled(chat_id):
        return

    userbot = await get_assistant(chat_id)
    if not userbot:
        return

    try:
        peer = await userbot.resolve_peer(chat_id)
        participants = await get_group_call_participants(userbot, peer)

        if participants and chat_id not in active_vc_chats:
            active_vc_chats.add(chat_id)
            asyncio.create_task(monitor_vc_chat(chat_id))

    except:
        pass



async def handle_user_join(chat_id, user_id, userbot):
    try:
        user = await userbot.get_users(user_id)
        mention = (
            f'<a href="tg://user?id={user_id}">{user.first_name}</a>'
        )
        username = f"@{user.username}" if user.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"

        text = f"""
🎤 <b>ᴜꜱᴇʀ ᴊᴏɪɴᴇᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ</b>

👤 <b>ɴᴀᴍᴇ:</b> {mention}
🔗 <b>ᴜꜱᴇʀɴᴀᴍᴇ:</b> {username}
🆔 <b>ɪᴅ:</b> <code>{user_id}</code>
"""

        msg = await app.send_message(chat_id, text)
        asyncio.create_task(delete_after_delay(msg, 10))

    except Exception as e:
        LOGGER.error(f"JOIN MSG ERROR: {e}")


async def handle_user_leave(chat_id, user_id, userbot):
    try:
        user = await userbot.get_users(user_id)
        mention = (
            f'<a href="tg://user?id={user_id}">{user.first_name}</a>'
        )
        username = f"@{user.username}" if user.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"

        text = f"""
🚪 <b>ᴜꜱᴇʀ ʟᴇꜰᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ</b>

👤 <b>ɴᴀᴍᴇ:</b> {mention}
🔗 <b>ᴜꜱᴇʀɴᴀᴍᴇ:</b> {username}
🆔 <b>ɪᴅ:</b> <code>{user_id}</code>
"""

        msg = await app.send_message(chat_id, text)
        asyncio.create_task(delete_after_delay(msg, 10))

    except Exception as e:
        LOGGER.error(f"LEAVE MSG ERROR: {e}")


async def delete_after_delay(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass



@app.on_message(filters.command("vclog") & filters.group)
async def vc_log_toggle(_, message: Message):
    chat_id = message.chat.id

    button_text = "🔴 Turn OFF" if is_enabled(chat_id) else "🟢 Turn ON"

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    button_text, callback_data=f"toggle_vclog_{chat_id}"
                )
            ]
        ]
    )

    await message.reply(
        f"""
🎧 <b>Voice Chat Logger Status</b>

➡️ <b>Current:</b> {'🟢 Enabled' if is_enabled(chat_id) else '🔴 Disabled'}

Tap button below to toggle VC logging.
""",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("toggle_vclog_"))
async def vc_log_button(_, cq: CallbackQuery):
    chat_id = int(cq.data.split("_")[2])

    if is_enabled(chat_id):
        disable_logger(chat_id)
        active_vc_chats.discard(chat_id)
        status = "🔴 <b>Disabled</b>"
    else:
        enable_logger(chat_id)
        status = "🟢 <b>Enabled</b>"
        asyncio.create_task(check_and_monitor_vc(chat_id))

    new_button = "🔴 Turn OFF" if is_enabled(chat_id) else "🟢 Turn ON"

    await cq.edit_message_text(
        f"🎧 <b>Voice Chat Logger Updated!</b>\n\nCurrent Status → {status}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        new_button, callback_data=f"toggle_vclog_{chat_id}"
                    )
                ]
            ]
        ),
    )



@app.on_message(filters.group)
async def auto_trigger(_, message: Message):
    chat_id = message.chat.id
    if is_enabled(chat_id):
        asyncio.create_task(check_and_monitor_vc(chat_id))