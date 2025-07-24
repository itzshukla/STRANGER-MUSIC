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

@app.on_message(filters.command(["admins","staff"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**ɢʀᴏᴜᴘ sᴛᴀғғ - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 ᴏᴡɴᴇʀ\n└ {owner.mention}\n\n👮🏻 ᴀᴅᴍɪɴs\n"
      else:
        text2 += f"👑 ᴏᴡɴᴇʀ\n└ @{owner.username}\n\n👮🏻 ᴀᴅᴍɪɴs\n"
    except:
      text2 += f"👑 ᴏᴡɴᴇʀ\n└ <i>Hidden</i>\n\n👮🏻 ᴀᴅᴍɪɴs\n"
    if len(adminList) == 0:
      text2 += "└ <i>ᴀᴅᴍɪɴs ᴀʀᴇ ʜɪᴅᴅᴇɴ</i>"  
      await app.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ᴀᴅᴍɪɴs**: {lenAdminList}"  
      await app.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

# ------------------------------------------------------------------------------- #

@app.on_message(filters.command("bots"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**ʙᴏᴛ ʟɪsᴛ - {message.chat.title}**\n\n🤖 ʙᴏᴛs\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | *ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏғ ʙᴏᴛs**: {lenBotList}"  
      await app.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)

# ------------------------------------------------------------------------------- #