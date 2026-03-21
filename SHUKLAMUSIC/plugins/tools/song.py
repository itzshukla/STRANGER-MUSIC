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

import os
import re
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
)

from SHUKLAMUSIC import app, YouTube
from SHUKLAMUSIC.platforms.Youtube import download_song, download_video
from config import (
    BANNED_USERS,
    SONG_DOWNLOAD_DURATION,
    SONG_DOWNLOAD_DURATION_LIMIT,
)
from SHUKLAMUSIC.utils.decorators.language import language, languageCB
from SHUKLAMUSIC.utils.errors import capture_err, capture_callback_err
from SHUKLAMUSIC.utils.formatters import time_to_seconds
from SHUKLAMUSIC.utils.inline.song import song_markup

SONG_COMMAND = ["song"]


@app.on_message(filters.command(SONG_COMMAND) & filters.group & ~BANNED_USERS)
@capture_err
@language
async def song_command_group(client, message: Message, lang):
    await message.reply_text(
        lang["song_1"],
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(lang["SG_B_1"],
                                   url=f"https://t.me/{app.username}?start=song")]]
        ),
    )


@app.on_message(filters.command(SONG_COMMAND) & filters.private & ~BANNED_USERS)
@capture_err
@language
async def song_command_private(client, message: Message, lang):
    await message.delete()
    mystic = await message.reply_text(lang["play_1"])

    url = await YouTube.url(message)
    query = url or (message.text.split(None, 1)[1] if len(message.command) > 1 else None)
    if not query:
        return await mystic.edit_text(lang["song_2"])

    if url and not await YouTube.exists(url):
        return await mystic.edit_text(lang["song_5"])

    try:
        title, dur_min, dur_sec, thumb, vidid = await YouTube.details(query)
    except Exception:
        return await mystic.edit_text(lang["play_3"])

    if not dur_min:
        return await mystic.edit_text(lang["song_3"])
    if int(dur_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(lang["play_4"].format(SONG_DOWNLOAD_DURATION, dur_min))

    await mystic.delete()
    await message.reply_photo(
        thumb,
        caption=lang["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(song_markup(lang, vidid)),
    )


@app.on_callback_query(filters.regex(r"song_back") & ~BANNED_USERS)
@capture_callback_err
@languageCB
async def songs_back_helper(client, cq, lang):
    _ignored, req = cq.data.split(None, 1)
    stype, vidid = req.split("|")
    await cq.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(song_markup(lang, vidid))
    )


@app.on_callback_query(filters.regex(r"song_helper") & ~BANNED_USERS)
@capture_callback_err
@languageCB
async def song_helper_cb(client, cq, lang):
    _ignored, req = cq.data.split(None, 1)
    stype, vidid = req.split("|")

    try:
        await cq.answer(lang["song_6"], show_alert=True)
    except Exception:
        pass

    buttons = [
        [InlineKeyboardButton(
            text="⬇️ Download",
            callback_data=f"song_download {stype}|direct|{vidid}",
        )],
        [
            InlineKeyboardButton(lang["BACK_BUTTON"], callback_data=f"song_back {stype}|{vidid}"),
            InlineKeyboardButton(lang["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    await cq.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"song_download") & ~BANNED_USERS)
@capture_callback_err
@languageCB
async def song_download_cb(client, cq, lang):
    try:
        await cq.answer("Downloading…")
    except Exception:
        pass

    _ignored, req = cq.data.split(None, 1)
    stype, fmt_id, vidid = req.split("|")
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    mystic = await cq.edit_message_text(lang["song_8"])

    file_path = None
    try:
        info, _v = await YouTube.track(yturl)
        title = re.sub(r"\W+", " ", info["title"])
        thumb = await cq.message.download()
        duration_sec = time_to_seconds(info.get("duration_min")) if info.get("duration_min") else None

        if stype == "audio":
            file_path = await download_song(yturl)
            if not file_path:
                return await mystic.edit_text(lang["song_10"])
            await mystic.edit_text(lang["song_11"])
            await app.send_chat_action(cq.message.chat.id, ChatAction.UPLOAD_AUDIO)
            await cq.edit_message_media(
                InputMediaAudio(
                    media=file_path,
                    caption=title,
                    thumb=thumb,
                    title=title,
                    performer=info.get("uploader"),
                )
            )
        else:
            file_path = await download_video(yturl)
            if not file_path:
                return await mystic.edit_text(lang["song_10"])
            w, h = cq.message.photo.width, cq.message.photo.height
            await mystic.edit_text(lang["song_11"])
            await app.send_chat_action(cq.message.chat.id, ChatAction.UPLOAD_VIDEO)
            await cq.edit_message_media(
                InputMediaVideo(
                    media=file_path,
                    duration=duration_sec,
                    width=w,
                    height=h,
                    thumb=thumb,
                    caption=title,
                    supports_streaming=True,
                )
            )

    except Exception as err:
        print(f"[SONG] error: {err}")
        await mystic.edit_text(lang["song_10"])
    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"[SONG] cleanup failed: {e}")
