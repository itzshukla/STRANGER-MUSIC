import asyncio
from pyrogram import filters, enums
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.errors import FloodWait
from SHUKLAMUSIC import app

chatQueue = []
stopProcess = False

# ------------------- ZOMBIE CLEANER -------------------

@app.on_message(filters.command(["zombies", "clean"]))
async def remove_deleted_accounts(client, message: Message):
    global stopProcess

    try:
        sender = await app.get_chat_member(message.chat.id, message.from_user.id)
        if not sender.privileges:
            return await message.reply("👮🏻 | Only group **admins** can execute this command.")
    except:
        return await message.reply("👮🏻 | Only group **admins** can execute this command.")

    bot = await app.get_chat_member(message.chat.id, "self")
    if bot.status == ChatMemberStatus.MEMBER:
        return await message.reply("➠ | I need **admin permissions** to remove deleted accounts.")

    if len(chatQueue) >= 30:
        return await message.reply("➠ | I'm already working in **30 chats**. Please try again shortly.")

    if message.chat.id in chatQueue:
        return await message.reply("➠ | A cleanup is already in progress. Use /stop to cancel.")

    chatQueue.append(message.chat.id)
    deletedList = []

    async for member in app.get_chat_members(message.chat.id):
        if member.user.is_deleted:
            deletedList.append(member.user)

    if not deletedList:
        chatQueue.remove(message.chat.id)
        return await message.reply("⟳ | No deleted accounts found in this chat.")

    estimate = len(deletedList) * 1
    temp_msg = await message.reply(f"🧭 | Detected **{len(deletedList)}** deleted accounts.\n🥀 | Estimated time: `{estimate}s`.")

    removed = 0
    stopProcess = False

    while deletedList and not stopProcess:
        user = deletedList.pop(0)
        try:
            await app.ban_chat_member(message.chat.id, user.id)
            removed += 1
        except:
            pass
        await asyncio.sleep(10)

    chatQueue.remove(message.chat.id)
    await temp_msg.delete()

    await message.reply(
        f"✅ | Successfully removed `{removed}` deleted account(s) from this chat."
    )


# ------------------- ADMINS LIST -------------------

@app.on_message(filters.command(["admins", "staff"]))
async def list_admins(client, message: Message):
    try:
        admins = []
        owners = []

        async for member in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            if not member.privileges.is_anonymous and not member.user.is_bot:
                if member.status == ChatMemberStatus.OWNER:
                    owners.append(member.user)
                else:
                    admins.append(member.user)

        text = f"**👥 Group Staff - {message.chat.title}**\n\n"

        if owners:
            owner = owners[0]
            text += f"👑 Owner\n└ {owner.mention if not owner.username else '@' + owner.username}\n\n"
        else:
            text += "👑 Owner\n└ <i>Hidden</i>\n\n"

        text += "👮🏻 Admins\n"
        if not admins:
            text += "└ <i>Admins are hidden</i>"
        else:
            for i, admin in enumerate(admins):
                if admin.username:
                    text += f"{'└' if i == len(admins) - 1 else '├'} @{admin.username}\n"
                else:
                    text += f"{'└' if i == len(admins) - 1 else '├'} {admin.mention}\n"

        text += f"\n✅ | Total Admins: {len(admins) + len(owners)}"
        await app.send_message(message.chat.id, text)

    except FloodWait as e:
        await asyncio.sleep(e.value)


# ------------------- BOTS LIST -------------------

@app.on_message(filters.command("bots"))
async def list_bots(client, message: Message):
    try:
        bots = [member.user async for member in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.BOTS)]

        if not bots:
            return await message.reply("🤖 | No bots found in this group.")

        text = f"**🤖 Bots List - {message.chat.title}**\n\n"
        for i, bot in enumerate(bots):
            text += f"{'└' if i == len(bots) - 1 else '├'} @{bot.username}\n"

        text += f"\n✅ | Total Bots: {len(bots)}"
        await app.send_message(message.chat.id, text)

    except FloodWait as e:
        await asyncio.sleep(e.value)
