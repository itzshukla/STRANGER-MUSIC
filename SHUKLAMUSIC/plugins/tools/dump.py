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
import random
from datetime import datetime, timedelta
import os
from pyrogram import Client, filters
from SHUKLAMUSIC import app
from config import BOT_USERNAME

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def generate_card_number(prefix, length):
    number = prefix
    while len(number) < (length - 1):
        number.append(random.randint(0, 9))
    checksum = luhn_checksum(int(''.join(map(str, number))) * 10)
    number.append((10 - checksum) % 10)
    return ''.join(map(str, number))

def generate_card_details(prefix):
    length = 16  # Assuming a standard length for credit card numbers
    card_number = generate_card_number(prefix, length)
    cvv = generate_cvv()
    expiration_date = generate_expiration_date()
    return f"{card_number}|{expiration_date}|{cvv}"

def generate_cvv():
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

def generate_expiration_date():
    start_date = datetime.now()
    month = random.randint(1, 12)
    year = random.randint(start_date.year + 1, start_date.year + 8)
    return f"{month:02d}|{year}"

# List of BINs
bins = [
    "480365", "460531", "420640", "462228", "426750", "514812",
    "412610", "424631", "533224", "420767", "517805", "441103",
    "514812", "412610", "414720", "420767", "468005", "486796",
    "426684", "405206", "407791", "407166", "406068", "405731",
    "412425", "414720", "414740", "414934", "420767", "422708",
    "423125", "515462", "423223", "522974", "549184", "516949",
    "523905", "523920", "523974", "524234", "524207", "524198",
    "524176", "524175", "524164", "524151", "524028", "523995",
    "462068", "406003", "527519", "522835", "531106", "515593",
    "528535", "407843", "414709", "511558", "486355", "533248",
    "541175", "537664", "529867", "520737", "515549", "522096",
    "426807", "538976", "517148", "554350", "407732", "524708",
    "545608", "511541", "518873", "464018", "511939", "526192",
    "514377", "511516", "537970", "448563", "417401", "539277",
    "403995", "414720", "515478", "511014", "438857", "519004",
    "510008", "522078", "555426", "400893", "438854", "412138",
    "532839", "452522", "546325", "515676", "512230", "536670",
    "555740", "557039", "533920", "523434", "549630", "424631",
    "405037", "525855", "531083", "400022", "413098", "431503",
    "420760", "510785", "421807", "532205", "531260", "486236",
    "452163", "440393", "434769", "406068", "420767", "406032",
    "431231", "442756", "475056", "483313", "478200", "461046",
    "414720", "486796", "402451", "556314", "540463", "406042",
    "447914", "480213", "514616", "546160", "552942", "418505",
    "543570", "522150", "547446", "521616", "552478", "521583"
]


@app.on_message(filters.command("dump"))
async def dump_cards(client, message):
    try:
        amount = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ ᴠᴀɪʟᴅ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ Dᴜᴍᴘ Cᴄ ᴜsᴇ /dump 3000")        
        return

    file_path = f"{amount}x_NON VBVHQ_CC_Dumped_By_@{BOT_USERNAME}.txt"
    with open(file_path, "w") as file:
        for _ in range(amount):
            bin = random.choice(bins)
            bin_prefix = [int(d) for d in bin if d.isdigit()]
            card_details = generate_card_details(bin_prefix)
            file.write(card_details + "\n")

    await message.reply_document(file_path)
    os.remove(file_path)
    