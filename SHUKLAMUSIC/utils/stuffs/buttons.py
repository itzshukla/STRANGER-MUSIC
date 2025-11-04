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
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    MBUTTON = [[InlineKeyboardButton("ᴄʜᴀᴛ-ɢᴘᴛ", callback_data="mplus HELP_ChatGPT"),InlineKeyboardButton("ɢʀᴏᴜᴘs", callback_data="mplus HELP_Group"),InlineKeyboardButton("sᴛɪᴄᴋᴇʀs", callback_data="mplus HELP_Sticker")],
    [InlineKeyboardButton("ᴛᴀɢ-ᴀʟʟ", callback_data="mplus HELP_TagAll"),
    InlineKeyboardButton("ɪɴꜰᴏ", callback_data="mplus HELP_Info"),InlineKeyboardButton("ᴇxᴛʀᴀ", callback_data="mplus HELP_Extra")],
    [InlineKeyboardButton("ɪᴍᴀɢᴇ", callback_data="mplus HELP_Image"),
    InlineKeyboardButton("ᴀᴄᴛɪᴏɴ", callback_data="mplus HELP_Action"),InlineKeyboardButton("sᴇᴀʀᴄʜ", callback_data="mplus HELP_Search")],    
    [InlineKeyboardButton("ғᴏɴᴛ", callback_data="mplus HELP_Font"),
    InlineKeyboardButton("ɢᴀᴍᴇs", callback_data="mplus HELP_Game"),InlineKeyboardButton("ᴛ-ɢʀᴀᴘʜ", callback_data="mplus HELP_TG")],
    [InlineKeyboardButton("ɪᴍᴘᴏsᴛᴇʀ", callback_data="mplus HELP_Imposter"),
    InlineKeyboardButton("ᴛʀᴜᴛʜ-ᴅᴀʀᴇ", callback_data="mplus HELP_TD"),InlineKeyboardButton("ʜᴀsᴛᴀɢ", callback_data="mplus HELP_HT")], 
    [InlineKeyboardButton("ᴛᴛs", callback_data="mplus HELP_TTS"),
    InlineKeyboardButton("ғᴜɴ", callback_data="mplus HELP_Fun"),InlineKeyboardButton("ǫᴜᴏᴛʟʏ", callback_data="mplus HELP_Q")],          
    [InlineKeyboardButton("◁", callback_data=f"settings_back_helper"), 
    InlineKeyboardButton("▷", callback_data=f"managebot123 settings_back_helper"),
    ]]