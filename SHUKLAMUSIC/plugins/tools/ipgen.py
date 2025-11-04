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
from pyrogram import Client, filters
import socket
import struct
import random
import os
from SHUKLAMUSIC import app

# Function to generate a random IPv4 address
def generate_random_ipv4():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

# Command handler for /ipgen
@app.on_message(filters.command("ipgen", prefixes="/"))
async def ipgen_command(client, message):
    # Get the argument from the command (number of IPs to generate)
    try:
        command, arg = message.text.split()
        count = int(arg)
    except ValueError:
        count = 1  # Default to generating one IP if no valid count provided

    # Generate the IPs
    ip_addresses = [generate_random_ipv4() for _ in range(count)]

    # If more than 10 IPs generated, save them to a file and send as a document
    if len(ip_addresses) > 10:
        file_name = f"ip_addresses_{count}.txt"
        with open(file_name, "w") as file:
            file.write("\n".join(ip_addresses))
        await message.reply_document(document=file_name, caption=f"┏━━━━━━━⍟\n┃ GEN IP {count} IPv4 ✅\n┗━━━━━━━━━━━━━━━⊛\n⊙ Request :-")
        os.remove(file_name)  # Remove the file after sending
    else:
        # Reply with the generated IPs
        if ip_addresses:
            reply_text = "\n".join(ip_addresses)
        else:
            reply_text = "No IP addresses generated."
        await message.reply_text(f"┏━━━━━━━⍟\n┃ GEN IP {count} IPv4 ✅\n┗━━━━━━━━━━━━━━━⊛\n⊙ Request :-\n\n{reply_text}")
        