import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from SHUKLAMUSIC.plugins.tools.pretenderdb import impo_off, impo_on, check_pretender, add_userdata, get_userdata, usr_data
from SHUKLAMUSIC import app

MISHI = [
    "https://graph.org/file/f86b71018196c5cfe7344.jpg",
    "https://graph.org/file/a3db9af88f25bb1b99325.jpg",
    "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
    "https://graph.org/file/84de4b440300297a8ecb3.jpg",
    "https://graph.org/file/84e84ff778b045879d24f.jpg",
    "https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
    "https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
    "https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
    "https://graph.org/file/37248e7bdff70c662a702.jpg",
    "https://graph.org/file/0bfe29d15e918917d1305.jpg",
    "https://graph.org/file/16b1a2828cc507f8048bd.jpg",
    "https://graph.org/file/e6b01f23f2871e128dad8.jpg",
    "https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
    "https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
    "https://graph.org/file/39d7277189360d2c85b62.jpg",
    "https://graph.org/file/5846b9214eaf12c3ed100.jpg",
    "https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
    "https://graph.org/file/3514efaabe774e4f181f2.jpg",
]

ROY = [
    [
        InlineKeyboardButton(
            text="ᴀᴅᴅ ᴍᴇ",
            url="https://t.me/SapnaMusicRobot?startgroup=true"
        ),
        InlineKeyboardButton(
            text="ᴜᴘᴅᴀᴛᴇ",
            url="https://t.me/SHIVANSH474"
        )
    ],
]


@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    if not message.from_user or message.sender_chat or not await check_pretender(message.chat.id):
        return

    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )

    username_before, first_name_before, last_name_before = await get_userdata(message.from_user.id)
    msg = ""
    needs_update = False

    if (
        username_before != message.from_user.username
        or first_name_before != message.from_user.first_name
        or last_name_before != message.from_user.last_name
    ):
        msg += f"""**♥︎ ᴜsᴇʀ sʜᴏʀᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ♥︎**

**๏ ɴᴀᴍᴇ** ➛ {message.from_user.mention}
**๏ ᴜsᴇʀ ɪᴅ** ➛ {message.from_user.id}
"""

    if username_before != message.from_user.username:
        bef = f"@{username_before}" if username_before else "NO USERNAME"
        aft = f"@{message.from_user.username}" if message.from_user.username else "NO USERNAME"
        msg += f"""
**♥︎ ᴄʜᴀɴɢᴇᴅ ᴜsᴇʀɴᴀᴍᴇ ♥︎**

**๏ ʙᴇғᴏʀᴇ** ➛ {bef}
**๏ ᴀғᴛᴇʀ** ➛ {aft}
"""
        needs_update = True

    if first_name_before != message.from_user.first_name:
        msg += f"""
**♥︎ ᴄʜᴀɴɢᴇᴅ ғɪʀsᴛ ɴᴀᴍᴇ ♥︎**

**๏ ʙᴇғᴏʀᴇ** ➛ {first_name_before}
**๏ ᴀғᴛᴇʀ** ➛ {message.from_user.first_name}
"""
        needs_update = True

    if last_name_before != message.from_user.last_name:
        bef = last_name_before or "NO LAST NAME"
        aft = message.from_user.last_name or "NO LAST NAME"
        msg += f"""
**♥︎ ᴄʜᴀɴɢᴇᴅ ʟᴀsᴛ ɴᴀᴍᴇ ♥︎**

**๏ ʙᴇғᴏʀᴇ** ➛ {bef}
**๏ ᴀғᴛᴇʀ** ➛ {aft}
"""
        needs_update = True

    if needs_update:
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        await message.reply_photo(
            random.choice(MISHI),
            caption=msg,
            reply_markup=InlineKeyboardMarkup(ROY),
        )


@app.on_message(filters.group & filters.command("imposter") & ~filters.bot & ~filters.via_bot)
async def set_mataa(_, message: Message):
    if len(message.command) == 1:
        return await message.reply("**ᴅᴇᴛᴇᴄᴛ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴇʀs ᴜsᴀɢᴇ : /imposter enable|disable**")

    cmd = message.command[1].lower()
    if cmd == "enable":
        if await impo_on(message.chat.id):
            await message.reply(f"**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
        else:
            await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}")
    elif cmd == "disable":
        if not await impo_off(message.chat.id):
            await message.reply(f"**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
        else:
            await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}")
    else:
        await message.reply("**ᴅᴇᴛᴇᴄᴛ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴇʀs ᴜsᴀɢᴇ : /imposter enable|disable**")
