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
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from pyrogram import Client, filters
from SHUKLAMUSIC import app


def google_dork(dork_query, num_results=10):
    query = urllib.parse.quote_plus(dork_query)
    url = f"https://www.google.com/search?q={query}&num={num_results}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                results.append({
                    'link': link
                })

        return results
    else:
        print(f"Error: Unable to fetch results. Status code: {response.status_code}")
        return None

@app.on_message(filters.command("dork"))
async def dork(client, message):
    query = message.text.split(" ", 1)
    if len(query) == 1:
        await message.reply_text("🚫 𝗣𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝘀𝗲𝗮𝗿𝗰𝗵 𝗾𝘂𝗲𝗿𝘆.\n\n /dork <your_query>")
        return

    dork_query = query[1]
    start_time = time.time()
    results = google_dork(dork_query, num_results=500)  # Fetching up to 50 results
    end_time = time.time()

    if results:
        results_text = "\n".join([f"{idx + 1}. {res['link']}\n" for idx, res in enumerate(results)])
        time_taken = end_time - start_time

        # Create a .txt file with the query name and save the results
        file_name = f"{dork_query}.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(results_text)

        # Send the .txt file
        caption = (
            f"🔍 𝗚𝗼𝗼𝗴𝗹𝗲 𝗗𝗼𝗿𝗸 𝗥𝗲𝘀𝘂𝗹𝘁𝘀\n"
            f"⏱️ 𝗧𝗶𝗺𝗲 𝗧𝗮𝗸𝗲𝗻 : {time_taken:.2f} seconds\n"
            f"👤 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗯𝘆 : {message.from_user.first_name}"
        )

        await message.reply_document(file_name, caption=caption)
    else:
        await message.reply_text("No results found.")