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
import datetime
import telebot
import time
import mysql.connector
import json
from pyrogram import filters
from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from mysql.connector import Error
from SHUKLAMUSIC import app

def find_captcha(response_text):
    if 'recaptcha' in response_text.lower():
        return ' Using Google reCAPTCHA ✅'
    elif 'hcaptcha' in response_text.lower():
        return 'Using hCaptcha ✅'
    else:
        return 'Not using Any Captcha🚫'
        
def check_stripe_live():
    return False  # Replace this with your actual logic


def detect_cloudflare(response):
    cloudfare_elements = ["cloudfare.com", "__cfduid"]
    for element in cloudfare_elements:
        if element in response.text.lower():
            return True
    cloudfare_headers = ["cf-ray", "cf-cache-status", "server"]
    for header in cloudfare_headers:
        if header in response.headers:
            return True
    return False


def find_payment_gateways(response_text):
    detected_gateways = []
    lower_text = response_text.lower()

    # Extensive list of payment gateways
    gateways = {
        "paypal": "PayPal",
        "stripe": "Stripe",
        "braintree": "Braintree",
        "square": "Square",
        "authorize.net": "Authorize.Net",
        "2checkout": "2Checkout",
        "adyen": "Adyen",
        "worldpay": "Worldpay",
        "sagepay": "SagePay",
        "checkout.com": "Checkout.com",
        "skrill": "Skrill",
        "neteller": "Neteller",
        "payoneer": "Payoneer",
        "klarna": "Klarna",
        "afterpay": "Afterpay",
        "sezzle": "Sezzle",
        "alipay": "Alipay",
        "wechat pay": "WeChat Pay",
        "tenpay": "Tenpay",
        "qpay": "QPay",
        "sofort": "SOFORT Banking",
        "giropay": "Giropay",
        # "ideal": "iDEAL",
        "trustly": "Trustly",
        "zelle": "Zelle",
        "venmo": "Venmo",
        "epayments": "ePayments",
        "revolut": "Revolut",
        "wise": "Wise (formerly TransferWise)",
        "shopify payments": "Shopify Payments",
        "woocommerce": "WooCommerce",
        "paytm": "Paytm",
        "phonepe": "PhonePe",
        "google pay": "Google Pay",
        "bhim upi": "BHIM UPI",
        "razorpay": "Razorpay",
        "instamojo": "Instamojo",
        "ccavenue": "CCAvenue",
        "payu": "PayU",
        "mobikwik": "MobiKwik",
        "freecharge": "FreeCharge",
        # "ebs": "EBS",
        "cashfree": "Cashfree",
        "jio money": "JioMoney",
        "yandex.money": "Yandex.Money",
        "qiwi": "QIWI",
        "webmoney": "WebMoney",
        "paysafe": "Paysafe",
        "bpay": "BPAY",
        "mollie": "Mollie",
        "paysera": "Paysera",
        "multibanco": "Multibanco",
        "pagseguro": "PagSeguro",
        "mercadopago": "MercadoPago",
        "payfast": "PayFast",
        "billdesk": "BillDesk",
        "paystack": "Paystack",
        "interswitch": "Interswitch",
        "voguepay": "VoguePay",
        "flutterwave": "Flutterwave",
    }

    for key, value in gateways.items():
        if key in lower_text:
            detected_gateways.append(value)

    if not detected_gateways:
        detected_gateways.append("Unknown")

    return detected_gateways


def find_stripe_version(response_text):
    # Check if the response indicates the use of Stripe 3D Secure
    if 'stripe3dsecure' in response_text.lower():
        return "3D Secured ✅"
    # Check if the response indicates the use of Stripe Checkout
    elif 'stripe-checkout' in response_text.lower():
        return "Checkout external link 🔗"
    # Default to 2D Secure if not explicitly indicated
    else:
        return "2D site ACTIVE📵"

def find_payment_gateway(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Pass the response text to the find_payment_gateways function
        detected_gateways = find_payment_gateways(response.text)
        return detected_gateways
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return ["Error"]


@app.on_message(filters.command("gate"))
async def check_payment_gateways(_, message):
    try:
        result_message = ""
        website_urls = [message.text[len('/gate'):].strip()]
        if not website_urls[0].startswith(("http://", "https://")):
            website_urls[0] = "http://" + website_urls[0]  # Add http:// if not provided

        for website_url in website_urls:
            response = requests.get(website_url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()

            # Pass the response text to the find_payment_gateways function
            detected_gateways = find_payment_gateways(response.text)
            # Detect captcha
            detected_captcha = find_captcha(response.text)
            # Detect Cloudflare protection
            is_cloudflare_protected = detect_cloudflare(response)

            result_message = f"----------------------------\n"
            result_message += f"|𝙍𝙚𝙨𝙪𝙡𝙩𝙨 𝙛𝙤𝙧 {website_url}:\n"
            result_message += f"|𝗣𝗮𝘆𝗺𝗲𝗻𝘁 𝗚𝗮𝘁𝗲𝘄𝗮𝘆𝘀: {', '.join(detected_gateways)}\n"
            result_message += f"|𝗖𝗮𝗽𝘁𝗰𝗵𝗮: {detected_captcha}\n"
            result_message += f"|𝘾𝙡𝙤𝙪𝙙𝙛𝙡𝙖𝙧𝙚 𝙋𝙧𝙤𝙩𝙚𝙘𝙩𝙞𝙤𝙣: {'✅' if is_cloudflare_protected else '🚫'}\n"
            result_message += f"----------------------------\n"
        result_message += f"𝐁𝐨𝐭 𝐛𝐲 - @SapnaMusicRobot 👑\n"
        result_message += f"---------------------------\n"
        result_message += f"𝗖𝗛𝗘𝗖𝗞𝗘𝗗 𝗕𝗬 𝗧𝗘𝗔𝗠 @StrangerAssociation\n"
        result_message += f"--------------------------------------------------------------\n"

        await message.reply(result_message, disable_web_page_preview=True)

    except requests.exceptions.RequestException as e:
        await message.reply("𝐄𝐫𝐫𝐨𝐫: 𝐈𝐧 𝐅𝐞𝐭𝐜𝐡𝐢𝐧𝐠 𝐃𝐞𝐭𝐚𝐢𝐥𝐬. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐡𝐞𝐜𝐤 𝐋𝐢𝐧𝐤 𝐢𝐟 𝐭𝐡𝐞 𝐥𝐢𝐧𝐤 𝐢𝐬 𝐫𝐞𝐚𝐜𝐡𝐚𝐛𝐥𝐞 𝐨𝐫 𝐧𝐨𝐭 ")