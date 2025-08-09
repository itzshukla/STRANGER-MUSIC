import asyncio
import os
import re
import json
from typing import Union
from urllib.parse import urlparse, parse_qs

import httpx
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
from SHUKLAMUSIC.utils.database import is_on_off
from SHUKLAMUSIC.utils.formatters import time_to_seconds
from config import YOUR_API_URL, YOUR_API_KEY


async def get_file_from_api(video_id, audio=True):
    endpoint = "/download/audio" if audio else "/download/video"
    url = f"{YOUR_API_URL}{endpoint}"
    params = {"video_id": video_id}
    headers = {"x-api-key": YOUR_API_KEY}
    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.get(url, params=params, headers=headers)
        if response.status_code == 200:
            ext = "mp3" if audio else "mp4"
            os.makedirs("downloads", exist_ok=True)
            file_path = f"downloads/{video_id}.{ext}"
            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_path
        else:
            print("API Error:", response.status_code, response.text)
            return None

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset is None:
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            duration = result["duration"]
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        # Extract YouTube video ID
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        url_data = urlparse(link)
        if url_data.hostname and "youtube" in url_data.hostname:
            query = parse_qs(url_data.query)
            video_id = query.get("v", [None])[0]
        elif url_data.hostname == "youtu.be":
            video_id = url_data.path[1:]
        else:
            video_id = link  # fallback

        file_path = await get_file_from_api(video_id, audio=False)
        if file_path:
            return 1, file_path
        else:
            return 0, "API download failed"

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        # This still uses shell/yt-dlp for playlist ID extraction. 
        # If your API supports playlist extraction, replace this block with an API call.
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-i", "--get-id", "--flat-playlist",
            "--playlist-end", str(limit),
            "--skip-download", link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f'Error:\n{stderr.decode()}')
            return []
        result = stdout.decode().split("\n")
        return [r for r in result if r.strip()]

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        # This is still local yt-dlp. If your API supports formats, update here.
        import yt_dlp
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True}
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except:
                    continue
                if not "dash" in str(format["format"]).lower():
                    try:
                        format["format"]
                        format["filesize"]
                        format["format_id"]
                        format["ext"]
                        format["format_note"]
                    except:
                        continue
                    formats_available.append(
                        {
                            "format": format["format"],
                            "filesize": format["filesize"],
                            "format_id": format["format_id"],
                            "ext": format["ext"],
                            "format_note": format["format_note"],
                            "yturl": link,
                        }
                    )
        return formats_available, link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        # Extract YouTube video ID
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        url_data = urlparse(link)
        if url_data.hostname and "youtube" in url_data.hostname:
            query = parse_qs(url_data.query)
            video_id = query.get("v", [None])[0]
        elif url_data.hostname == "youtu.be":
            video_id = url_data.path[1:]
        else:
            video_id = link  # fallback

        if songvideo:
            file_path = await get_file_from_api(video_id, audio=False)
            return file_path, True
        elif songaudio or not video:  # Default to audio if not video
            file_path = await get_file_from_api(video_id, audio=True)
            return file_path, True
        elif video:
            file_path = await get_file_from_api(video_id, audio=False)
            return file_path, True
        else:
            file_path = await get_file_from_api(video_id, audio=True)
            return file_path, True