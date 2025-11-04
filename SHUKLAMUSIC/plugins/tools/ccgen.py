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
from pyrogram import filters, enums
from SHUKLAMUSIC import app
import io
import random
import re
import aiohttp
from pyrogram import Client, filters

# Function to check Luhn algorithm for card validation
def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')

        if isSecond:
            d = d * 2

        nSum += d // 10
        nSum += d % 10

        isSecond = not isSecond

    return nSum % 10 == 0

# Function to generate card details
def cc_gen(cc, amount, mes='x', ano='x', cvv='x'):
    am = amount
    genrated = 0
    ccs = []

    while genrated < am:
        s = "0123456789"
        l = list(s)
        random.shuffle(l)
        result = ''.join(l)
        result = cc + result

        if cc[0] == "3":
            ccgen = result[:15]
        else:
            ccgen = result[:16]

        if checkLuhn(ccgen):
            genrated += 1
        else:
            continue

        if mes == 'x':
            mesgen = random.randint(1, 12)
            if len(str(mesgen)) == 1:
                mesgen = "0" + str(mesgen)
        else:
            mesgen = mes

        if ano == 'x':
            anogen = random.randint(2024, 2032)
        else:
            anogen = ano

        if cvv == 'x':
            if cc[0] == "3":
                cvvgen = random.randint(1000, 9999)
            else:
                cvvgen = random.randint(100, 999)
        else:
            cvvgen = cvv

        lista = f"{ccgen}|{mesgen}|{anogen}|{cvvgen}"
        ccs.append(lista)

    return ccs

# Function to fetch BIN information
async def bin_lookup(bin_number):
    astroboyapi = f"https://astroboyapi.com/api/bin.php?bin={bin_number}"

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(astroboyapi) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")
                    
                    bin_info_text = f"""
𝗕𝗶𝗻 𝗟𝗼𝗼𝗸𝘂𝗽 𝗥𝗲𝘀𝘂𝗹𝘁 🔍

[ϟ] 𝗕𝗶𝗻: <code>{bin_number}</code>
[ϟ] 𝗜𝗻𝗳𝗼: {brand} - {card_type} - {level}
[ϟ] 𝗕𝗮𝗻𝗸: {bank}
[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} {country_flag}
"""
                    return bin_info_text
                except Exception as e:
                    return f"Error: Unable to retrieve BIN information ({str(e)})"
            else:
                return f"Error: Unable to retrieve BIN information (Status code: {response.status})"

# Function to handle the generate_cc command
async def generate_cc(client, message):
    if len(message.text.split()) == 2:
        text = message.text.split()[1]
        amount = int(10)
    elif len(message.text.split()) == 3:
        text = message.text.split()[1]
        amount = int(message.text.split()[2])
    else:
        await message.reply("𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗙𝗢𝗥𝗠𝗔𝗧 ⚠️", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
        return

    if amount > 30000:
        await message.reply("𝗟𝗜𝗠𝗜𝗧 𝗧𝗢 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘 30000 ⚠️", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
        return

    params = re.sub('x+', 'x', text).split('|')
    if len(params[0]) < 6:
        await message.reply("Invalid bin.", disable_web_page_preview=True)
        return

    loading_message = await message.reply("𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗻𝗴 𝗰𝗰", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    cc = params[0].replace('x', '')
    expiration_month = int(params[1]) if len(params) > 1 and params[1] != 'x' else 'x'
    expiration_year = int(params[2]) if len(params) > 2 and params[2] != 'x' else 'x'
    cvv = params[3] if len(params) > 3 and params[3] != 'x' else 'x'

    ccs = cc_gen(cc, amount, expiration_month, expiration_year, cvv)
    astro = '\n'.join([f"<code>{cc}</code>" for cc in ccs])

    bin_info = await bin_lookup(cc[:6])

    if amount <= 10:
        mess = f"""
Here is your generated results:

{astro}

⊗ 𝗔𝗹𝗴𝗼: 𝗟𝘂𝗵𝗻
⊗ 𝗘𝘅𝘁𝗿𝗮𝗽: <code>{text}</code>
⊗ 𝗔𝗺𝗼𝘂𝗻𝘁: <code>{amount}</code>

⊗ Generated By: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
{bin_info}
"""
        await loading_message.delete()
        await message.reply(mess, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    else:
        mess = f"""
𝗖𝗖 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘𝗗 ✅

[ϟ] 𝗔𝗹𝗴𝗼: 𝗟𝘂𝗵𝗻
[ϟ] 𝗔𝗺𝗼𝘂𝗻𝘁: <code>{amount}</code>
[ϟ] 𝗘𝘅𝘁𝗿𝗮𝗽: <code>{text}</code>

[ϟ] 𝗚𝗲𝗻 𝗕𝘆: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
{bin_info}
"""
        try:
            with io.BytesIO(bytes('\n'.join(ccs), 'utf-8')) as out_file:
                out_file.name = 'cc.txt'
                await loading_message.delete()
                await client.send_document(message.chat.id, out_file, caption=mess, parse_mode=enums.ParseMode.HTML)
        except Exception as e:
            await loading_message.delete()
            await message.reply(f"Error: {e}", parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)

# Command to generate card details
@app.on_message(filters.command("gen", prefixes="."))
async def generate_cc_command(client, message):
    await generate_cc(client, message)
  