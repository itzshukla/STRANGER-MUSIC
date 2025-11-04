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
import re
import json
import requests
from pyrogram import Client, filters, enums
from SHUKLAMUSIC import app

def get_json_response(data):
    checkout = data
    if checkout:
        url_match = re.search(r'https?://checkout.stripe.com/c/pay/(.+?)#', checkout)
        if not url_match:
            return "❌ Invalid Link: The provided URL is not valid."

        cs = url_match.group(1)
        url = f"https://checkout.stripe.com/c/pay/{cs}"

        pk_list = re.findall(r'"apiKey":"(.+?)"', decode_xor_string(url, 5))
        if not pk_list:
            return "❌ Invalid Link: Unable to retrieve the API key."

        pk = pk_list[0]
        site = re.findall(r'"referrerOrigin":"(.+?)"', decode_xor_string(url, 5))[0]

        headers = {
            'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; M1901F7S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        payload = {
            'key': pk,
            'eid': 'NA',
            'browser_locale': 'en-US',
            'redirect_type': 'stripe_js'
        }

        response = requests.post(f'https://api.stripe.com/v1/payment_pages/{cs}/init', headers=headers, auth=(pk, ''), data=payload)
        
        if response.status_code != 200:
            return f"❌ HTTP Error: {response.status_code}"
        
        fim = response.text

        # Debugging: Log the raw response text
        print(f"Raw response text: {fim}")

        if 'No such payment_page' in fim:
            return "❌ Expired Link: The payment page associated with the link no longer exists."
        else:
            try:
                name = re.findall(r'"display_name": "(.+?)"', fim)
                email = re.findall(r'"customer_email": "(.+?)"', fim)
                cur = re.findall(r'"currency": "(.+?)"', fim)
                amt = re.findall(r'"amount": (\d+),', fim)
                if not amt:
                    amt = re.findall(r'"total": (\d+),', fim)
                if not amt:
                    amt = ['____']
                name = name[0] if name else '____'
                pk = pk if pk else '____'
                site = site if site else '____'
                cs = cs if cs else '____'
                cur = cur[0] if cur else '____'
                email = email[0] if email else '❗️ Email not found'

                data = {
                    'name': name,
                    'pklive': pk,
                    'cslive': cs,
                    'amount': amt[0],
                    'email': email
                }

                return json.dumps(data)
            except Exception as e:
                # Debugging: Log the exception
                print(f"Parsing error: {str(e)}")
                return f"❌ Parsing Error: {str(e)}"

    return None

def decode_xor_string(text, key):
    key = [key] if isinstance(key, int) else key
    output = ''
    for i, c in enumerate(text):
        output += chr(ord(c) ^ key[i % len(key)])
    return output

@app.on_message(filters.command("grab"))
async def grab(client, message):
    try:
        checkout_link = message.text.split(maxsplit=1)[1]

        json_response = get_json_response(checkout_link)

        if json_response:
            try:
                data = json.loads(json_response)

                response_message = "𝗦𝗶𝘁𝗲: {}\n\n".format(data['name'])
                response_message += "𝗣𝗞: {}\n".format(data['pklive'])
                response_message += "𝗖𝗦: {}\n".format(data['cslive'])
                response_message += "𝗘𝗺𝗮𝗶𝗹: {}\n".format(data['email'])
                response_message += "𝗔𝗺𝗼𝘂𝗻𝘁: {}\n".format(data['amount'])
                response_message += "𝗖𝘂𝗿𝗿𝗲𝗻𝗰𝘆: {}\n\n".format(data.get('currency', 'N/A'))
                response_message += "𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗯𝘆 𝗦𝘁𝗿𝗮𝗻𝗴𝗲𝗿"

                await message.reply(response_message, parse_mode=enums.ParseMode.HTML)
            except json.JSONDecodeError as json_err:
                await message.reply(f"Error decoding JSON: {json_err}", parse_mode=enums.ParseMode.HTML)
            except Exception as e:
                await message.reply(f"Unexpected Error: {e}", parse_mode=enums.ParseMode.HTML)
        else:
            await message.reply("❌ Invalid Link", parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        await message.reply(f"Error: {e}", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
