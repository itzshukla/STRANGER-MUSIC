from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SHUKLAMUSIC import app
from config import BOT_USERNAME

# Caption Text
start_txt = """<b>✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ <u>sᴛʀᴀɴɢᴇʀ ʀᴇᴘᴏs</u> ✨</b>

🚀 <b>ᴇᴀsʏ ᴅᴇᴘʟᴏʏ</b> – 1-ᴄʟɪᴄᴋ ʜᴇʀᴏᴋᴜ ᴅᴇᴘʟᴏʏᴍᴇɴᴛ  
🛡️ <b>ɴᴏ ʜᴇʀᴏᴋᴜ ᴏʀ ɪᴅ ʙᴀɴ ɪssᴜᴇs</b>  
🔋 <b>ᴜɴʟɪᴍɪᴛᴇᴅ ᴅʏɴᴏs</b> – ʀᴜɴ 24/7 ʟᴀɢɢ-ғʀᴇᴇ  
⚙️ <b>ғᴜʟʟʏ ғᴜɴᴄᴛɪᴏɴᴀʟ & ᴇʀʀᴏʀ-ғʀᴇᴇ</b>  

<i>ɴᴇᴇᴅ ʜᴇʟᴘ? sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴛᴏ ᴛʜᴇ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ!</i>"""

# Repo Command Handler
@app.on_message(filters.command("repo"))
async def repo_handler(_, msg):
    buttons = [
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/MASTIWITHFRIENDSXD"),
            InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url="https://t.me/SHASHANKDEVS"),
        ],
        [InlineKeyboardButton("🧾 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/SHIVANSH474")],
        [
            InlineKeyboardButton("💥 ʙᴀɴᴀʟʟ", url="https://github.com/itzshukla/STRANGER-BANALL/fork"),
            InlineKeyboardButton("🎧 ᴍᴜsɪᴄ V2", url="https://github.com/itzshukla/STRANGER-MUSIC/fork"),
        ],
        [
            InlineKeyboardButton("🎶 ᴍᴜsɪᴄ V1", url="https://github.com/itzshukla/STRANGER-MUSIC2.0/fork"),
            InlineKeyboardButton("💬 ᴄʜᴀᴛʙᴏᴛ", url="https://github.com/itzshukla/STRANGER-CHATBOT/fork"),
        ],
        [
            InlineKeyboardButton("🎯 sᴛʀɪɴɢ ɢᴇɴ", url="https://github.com/itzshukla/STRANGER-STRING-GEN/fork"),
            InlineKeyboardButton("🛠️ ɢᴄ ᴍᴀɴᴀɢᴇʀ", url="https://github.com/itzshukla/STRANGER-ROBOT/fork"),
        ],
        [
            InlineKeyboardButton("⚔️ sᴘᴀᴍ ʙᴏᴛs", url="https://github.com/itzshukla/STRANGER-SPAM-X/fork"),
            InlineKeyboardButton("👾 ʙᴀɴᴀʟʟ 10", url="https://github.com/itzshukla/STRANGER-BANALL-BOTS/fork"),
        ],
        [
            InlineKeyboardButton("🧪 sᴛʀɪɴɢ ʜᴀᴄᴋ", url="https://github.com/itzshukla/STRANGER-SESSION-HACK/fork"),
            InlineKeyboardButton("🤖 ɪᴅ ᴜsᴇʀʙᴏᴛ", url="https://t.me/StrangerHosterbot"),
        ],
        [InlineKeyboardButton("👑 sᴜᴘᴇʀ ᴜsᴇʀʙᴏᴛ", url="https://github.com/itzshukla/STRANGER-OPUSERBOT2.0/fork")]
    ]

    await msg.reply_photo(
        photo="https://telegra.ph/file/d9bddd89a8070632de73e.jpg",
        caption=start_txt,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

   
# --------------


@app.on_message(filters.command("repo", prefixes="#"))
@capture_err
async def repo(_, message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/repos/itzshukla/STRANGER-MUSIC/contributors")
    
    if response.status_code == 200:
        users = response.json()
        list_of_users = ""
        count = 1
        for user in users:
            list_of_users += f"{count}. [{user['login']}]({user['html_url']})\n"
            count += 1

        text = f"""[𝖱𝖤𝖯𝖮 𝖫𝖨𝖭𝖪](https://github.com/itzshukla/STRANGER-MUSIC) | [UPDATES](https://t.me/SHIVANSH474)
| 𝖢𝖮𝖭𝖳𝖱𝖨𝖡𝖴𝖳𝖮𝖱𝖲 |
----------------
{list_of_users}"""
        await app.send_message(message.chat.id, text=text, disable_web_page_preview=True)
    else:
        await app.send_message(message.chat.id, text="Failed to fetch contributors.")


