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
import aiohttp
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
from SHUKLAMUSIC.platforms.Youtube import API_URL, download_song, download_video
from config import (
    BANNED_USERS,
    SONG_DOWNLOAD_DURATION,
    SONG_DOWNLOAD_DURATION_LIMIT,
)
from SHUKLAMUSIC.utils.decorators.language import language, languageCB
from SHUKLAMUSIC.utils.errors import capture_err, capture_callback_err
from SHUKLAMUSIC.utils.formatters import convert_bytes, time_to_seconds
from SHUKLAMUSIC.utils.inline.song import song_markup

SONG_COMMAND = ["song"]


async def get_formats_from_api(vidid: str) -> list:
    formats_available = []
    async with aiohttp.ClientSession() as session:
        for media_type in ("audio", "video"):
            try:
                async with session.get(
                    f"{API_URL}/formats",
                    params={"url": vidid, "type": media_type},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status != 200:
                        continue
                    data = await resp.json()
                    for fmt in data.get("formats", []):
                        formats_available.append({
                            "format": fmt.get("format", f"{media_type} - {fmt.get('quality', '')}"),
                            "filesize": fmt.get("filesize"),
                            "format_id": fmt.get("format_id", media_type),
                            "ext": fmt.get("ext", "mp3" if media_type == "audio" else "mp4"),
                            "format_note": fmt.get("quality") or fmt.get("format_note", media_type.title()),
                            "type": media_type,
                        })
            except Exception:
                continue
    return formats_available


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

    try:
        formats = await get_formats_from_api(vidid)
    except Exception:
        return await cq.edit_message_text(lang["song_7"])

    if not formats:
        return await cq.edit_message_text(lang["song_7"])

    buttons = []
    seen = set()

    if stype == "audio":
        for f in formats:
            if f.get("type") != "audio":
                continue
            label = f["format_note"].title()
            if label in seen:
                continue
            seen.add(label)
            size_text = convert_bytes(f["filesize"]) if f.get("filesize") else ""
            btn_text = f"{label} • {size_text}" if size_text else label
            buttons.append([InlineKeyboardButton(
                text=btn_text,
                callback_data=f"song_download {stype}|{f['format_id']}|{vidid}",
            )])
    else:
        for f in formats:
            if f.get("type") != "video":
                continue
            label = f["format_note"].title()
            if label in seen:
                continue
            seen.add(label)
            size_text = convert_bytes(f["filesize"]) if f.get("filesize") else ""
            btn_text = f"{label} • {size_text}" if size_text else label
            buttons.append([InlineKeyboardButton(
                text=btn_text,
                callback_data=f"song_download {stype}|{f['format_id']}|{vidid}",
            )])

    buttons.append([
        InlineKeyboardButton(lang["BACK_BUTTON"], callback_data=f"song_back {stype}|{vidid}"),
        InlineKeyboardButton(lang["CLOSE_BUTTON"], callback_data="close"),
    ])

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
        print(f"[SONG] download/upload error: {err}")
        await mystic.edit_text(lang["song_10"])
    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"[SONG] cleanup failed: {e}")
