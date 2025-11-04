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
    "409177008", "414720251006", "421747000", "4355460266", "402347060", "435546026",
    "4266841656", "4095950011", "42135501290", "44304400", "4833140018", "4430442",
    "453735151", "4411040534", "4833120144", "4427322533", "485038", "5219918900",
    "51461601", "4124510157", "428581000", "462845004", "468138000003", "4100390552",
    "414720221", "516838004", "47820020", "414720251006", "4147202422", "4147202429",
    "41855060086", "4485590006", "435546026", "4266841656", "401043202959", "45659820202",
    "5425504500", "44468900", "4355460267", "486796691460", "41472025100", "4147202546",
    "461046030802", "4266841656", "4147202499", "420767027", "4867961220", "414720251006",
    "4411040534", "435173365032", "5425504502", "5425503300", "48679669146", "43554615026",
    "414720254672", "402347060", "409595000", "414720251006", "4867961220", "409595000",
    "4147202519", "51461601479", "420767027", "48331400187", "41472025100", "4867961220",
    "4147202511", "5520971800", "48331201", "4427422124", "4411040534824", "4856310015",
    "475055611", "54664511435", "514230003635", "427088009", "428581000", "4347691123",
    "435546026", "4390930036", "4403934254", "44039344010", "4403934442", "4411040534",
    "4427322533", "4427880030", "44304400", "4430442", "443051000", "443844004", "444607005",
    "44468900", "44479624", "4485590006", "453735151", "461046028", "462645004", "462845004",
    "46284500531", "462845084", "468138000003", "478200206", "47820020677", "4833120144",
    "4833140018", "48331400187", "483316024689", "4835610446", "485038", "488893", "51461601479",
    "516648040", "516838004", "5219918900", "530264000", "530487200083", "53566680540", "53573862004",
    "5425504500", "54704660098", "531462005", "44791482", "443044003364", "5404044987", "5223030007",
    "60114994", "52647110317", "4427880030", "60112088", "421121000086", "54160636007", "5455100042",
    "483313005633", "51461601411", "5264711031", "44304500", "4005700101", "4347690020", "45966100011",
    "432265026553", "4571493004", "52750500000", "5262053008", "48939601320", "529099001", "402856800002",
    "406042557", "55382300010", "4239990970", "4430410099", "42015600566", "53136400733", "4745030901",
    "51039200086", "403905509436", "5520040003", "511728050112", "40057001010", "4893960132", "47622317206",
    "478786191107", "4023961988", "53324801207", "5515340004", "4649520213", "5189410151", "542418130165",
    "52708900004", "5216990000", "45845320149", "40431300022", "5100040014", "434769803", "406068704",
    "490070034", "4680056031", "4833160246", "483313004", "4750556113", "4563310034", "46104609399",
    "4427550216", "442732252", "48679669", "48331201", "434769709", "4284180498", "42076702", "5219918900",
    "4095950011", "4446070067", "51461601", "531462006", "406156", "416916048037", "48331201", "4427422124",
    "4411040534824", "4856310015", "475055611", "54664511435", "514230003635"
]

@app.on_message(filters.command("hqdump"))
async def dump_cards(client, message):
    try:
        amount = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("Pʟᴇᴀsᴇ Pʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ ᴠᴀɪʟᴅ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ Dᴜᴍᴘ Cᴄ ᴜsᴇ /hqdump 3000")        
        return

    file_path = f"{amount}x_HQ_CC_Dumped_By_@{BOT_USERNAME}.txt"
    with open(file_path, "w") as file:
        for _ in range(amount):
            bin = random.choice(bins)
            bin_prefix = [int(d) for d in bin if d.isdigit()]
            card_details = generate_card_details(bin_prefix)
            file.write(card_details + "\n")

    await message.reply_document(file_path)
    os.remove(file_path)