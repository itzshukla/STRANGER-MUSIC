import asyncio
from logging import getLogger
from typing import Dict, Set
import random
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.raw import functions
from SHUKLAMUSIC import app
from SHUKLAMUSIC.utils.database import get_assistant

LOGGER = getLogger(__name__)


vc_active_users: Dict[int, Set[int]] = {}
active_vc_chats: Set[int] = set()


async def get_group_call_participants(userbot, peer):
    """Fetch current VC participants using userbot"""
    try:
        full_chat = await userbot.invoke(functions.channels.GetFullChannel(channel=peer))
        if not hasattr(full_chat.full_chat, 'call') or not full_chat.full_chat.call:
            return []
        call = full_chat.full_chat.call
        participants = await userbot.invoke(functions.phone.GetGroupParticipants(
            call=call, ids=[], sources=[], offset="", limit=100
        ))
        return participants.participants
    except Exception as e:
        error_msg = str(e).upper()
        if any(x in error_msg for x in ["GROUPCALL_NOT_FOUND", "CALL_NOT_FOUND", "NO_GROUPCALL"]):
            return []
        LOGGER.error(f"Error fetching participants: {e}")
        return []

async def monitor_vc_chat(chat_id):
    """Userbot monitors a single VC active chat for join/leave"""
    userbot = await get_assistant(chat_id)
    if not userbot:
        return

    while chat_id in active_vc_chats:
        try:
            peer = await userbot.resolve_peer(chat_id)
            participants_list = await get_group_call_participants(userbot, peer)
            new_users = set()
            for p in participants_list:
                if hasattr(p, 'peer') and hasattr(p.peer, 'user_id'):
                    new_users.add(p.peer.user_id)

            current_users = vc_active_users.get(chat_id, set())
            joined = new_users - current_users
            left = current_users - new_users

            
            tasks = []
            for user_id in joined:
                tasks.append(handle_user_join(chat_id, user_id, userbot))
            for user_id in left:
                tasks.append(handle_user_leave(chat_id, user_id, userbot))
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

            
            vc_active_users[chat_id] = new_users

        except Exception as e:
            LOGGER.error(f"Error monitoring VC for chat {chat_id}: {e}")

        await asyncio.sleep(2)  

async def check_and_monitor_vc(chat_id):
    """Check if VC is active and start monitoring"""
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
    """Send join message"""
    try:
        user = await userbot.get_users(user_id)
        name = user.first_name or "Unknown User"
        username = f"@{user.username}" if user.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
        mention = f'<a href="tg://user?id={user_id}">{name}</a>'
        
        join_message = f"""🎤 **ᴜsᴇʀ ᴊᴏɪɴᴇᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**

👤 **ɴᴀᴍᴇ :-** {mention}
🔗 **ᴜsᴇʀɴᴀᴍᴇ :-** {username}
🆔 **ɪᴅ :-** `{user_id}`

**❖ ᴛʜᴀɴᴋs ғᴏʀ ᴊᴏɪɴɪɴɢ 😁**"""
        
        sent_msg = await app.send_message(chat_id, join_message)
        asyncio.create_task(delete_after_delay(sent_msg, 10))
    except Exception as e:
        LOGGER.error(f"Error sending join message for {user_id}: {e}")

async def handle_user_leave(chat_id, user_id, userbot):
    """Send leave message"""
    try:
        user = await userbot.get_users(user_id)
        name = user.first_name or "Unknown User"
        username = f"@{user.username}" if user.username else "ɴᴏ ᴜsᴇʀɴᴀᴍᴇ"
        mention = f'<a href="tg://user?id={user_id}">{name}</a>'
        
        leave_message = f"""🚪 **ᴜsᴇʀ ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**

👤 **ɴᴀᴍᴇ :-** {mention}
🔗 **ᴜsᴇʀɴᴀᴍᴇ :-** {username}
🆔 **ɪᴅ :-** `{user_id}`

**❖ ʙʏᴇ ʙʏᴇ ᴠɪsɪᴛ ᴀɢᴀɪɴ 👋**"""
        
        sent_msg = await app.send_message(chat_id, leave_message)
        asyncio.create_task(delete_after_delay(sent_msg, 10))
    except Exception as e:
        LOGGER.error(f"Error sending leave message for {user_id}: {e}")

async def delete_after_delay(message, delay):
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except:
        pass


@app.on_message(filters.group)
async def auto_vc_logger_trigger(_, message: Message):
    chat_id = message.chat.id
    # Always check VC and start monitoring
    asyncio.create_task(check_and_monitor_vc(chat_id))
