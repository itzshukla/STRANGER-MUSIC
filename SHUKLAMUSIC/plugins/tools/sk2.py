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
import time
import stripe
from pyrogram import Client, filters, enums
from SHUKLAMUSIC import app

async def retrieve_account_details(sk):
    stripe.api_key = sk
    try:
        account = stripe.Account.retrieve()
        account_details = {
            "name": account.get("business_profile", {}).get("name") or account.get("settings", {}).get("dashboard", {}).get("display_name"),
            "email": account.get("email") or account.get("business_profile", {}).get("support_email"),
            "support_phone": account.get("business_profile", {}).get("support_phone"),
            "url": account.get("business_profile", {}).get("url"),
            "country": account.get("country"),
            "country_currency": account.get("default_currency"),
            "account_type": account.get("type"),
            "timezone": account.get("settings", {}).get("dashboard", {}).get("timezone"),
            "details_submitted": account.get("details_submitted"),
            "live_mode": account.get("charges_enabled"),
            "mcc": account.get("business_profile", {}).get("mcc"),
            "capabilities": account.get("capabilities", {}),
            "account_id": account.get("id")
        }
    except stripe.error.InvalidRequestError as e:
        account_details = {
            "error": f"Invalid API Key provided: {str(e)}"
        }
    except stripe.error.AuthenticationError as e:
        account_details = {
            "error": f"Authentication Error: {str(e)}"
        }
    except stripe.error.APIConnectionError as e:
        account_details = {
            "error": f"Network communication error: {str(e)}"
        }
    except stripe.error.StripeError as e:
        account_details = {
            "error": f"Stripe error: {str(e)}"
        }
    except Exception as e:
        account_details = {
            "error": f"An unexpected error occurred: {str(e)}"
        }
    return account_details

def title_case(text):
    if isinstance(text, bool):
        return "Yes" if text else "No"
    if isinstance(text, str):
        return text.title()
    return text

async def check_status(message, sk, user_id):
    tic = time.perf_counter()
    account_details = await retrieve_account_details(sk)
    toc = time.perf_counter()

    if "error" in account_details:
        response_text = f"""
[ϟ] 𝗦𝗞 ➜
<code>{sk}</code>
[ϟ] 𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲 : {account_details['error']} ❌
[ϟ] 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➜ <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>
        """
    else:
        display_name = account_details['name']
        capabilities = '\n'.join([f"[ϟ] {k.replace('_', ' ').title()} : {v.title()}" for k, v in account_details['capabilities'].items()])
        response_text = f"""
[ϟ] 𝗡𝗮𝗺𝗲 : {title_case(display_name)}
[ϟ] 𝗘𝗺𝗮𝗶𝗹 : {title_case(account_details['email'])}
[ϟ] 𝗣𝗵𝗼𝗻𝗲 : {account_details['support_phone']}
[ϟ] 𝗨𝗥𝗟 : {account_details['url']}
[ϟ] 𝗦𝘁𝗿𝗶𝗽𝗲 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 : {account_details['account_id']}
[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 : {title_case(account_details['country'])}
[ϟ] 𝗖𝗨𝗥𝗥𝗘𝗡𝗖𝗬 : {account_details['country_currency'].upper()}
[ϟ] 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗧𝘆𝗽𝗲 : {title_case(account_details['account_type'])}
[ϟ] 𝗧𝗶𝗺𝗲 𝗭𝗼𝗻𝗲 : {account_details['timezone']}
[ϟ] 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱 : {title_case(account_details['details_submitted'])}
[ϟ] 𝗟𝗶𝘃𝗲 𝗠𝗼𝗱𝗲 : {title_case(account_details['live_mode'])}
[ϟ] 𝗠𝗖𝗖 : {account_details['mcc']}
[ϟ] 𝗖𝗮𝗽𝗮𝗯𝗶𝗹𝗶𝘁𝗶𝗲𝘀 :
{capabilities}

[ϟ] 𝗦𝗞 ➜ 
<code>{sk}</code>
[ϟ] 𝗧𝗶𝗺𝗲 𝗧𝗼𝗼𝗸 : <b><code>{toc - tic:.2f}</code> Seconds</b>
[ϟ] 𝗖𝗵𝗲𝗰𝗸𝗲𝗱 𝗕𝘆 ➜ <a href="tg://user?id={user_id}">{message.from_user.first_name}</a>
        """
    return response_text

@app.on_message(filters.command("sk2", prefixes="."))
async def msk_command(client, message):
    ttt = message.text
    skm = re.search(r"sk_live_[a-zA-Z0-9]+", ttt)
    user_id = message.from_user.id

    if skm is not None:
        sk = skm.group(0)
        response = await check_status(message, sk, user_id)
        await message.reply(response, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    else:
        error_message = "𝗡𝗼 𝘃𝗮𝗹𝗶𝗱 𝗦𝘁𝗿𝗶𝗽𝗲 𝗸𝗲𝘆 𝗳𝗼𝘂𝗻𝗱"
        await message.reply(error_message)