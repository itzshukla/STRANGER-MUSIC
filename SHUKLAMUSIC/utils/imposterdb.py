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
from typing import Dict, List, Union
from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB_URI).Rankings

impdb = mongo.imposter
 
async def usr_data(user_id: int) -> bool:
    user = await impdb.find_one({"user_id": user_id})
    return bool(user)

async def get_userdata(user_id: int) -> bool:
    user = await impdb.find_one({"user_id": user_id})
    return user["username"], user["first_name"], user["last_name"]

async def add_userdata(user_id: int, username, first_name, last_name):
    await impdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        },
        upsert=True,
    )

async def check_imposter(chat_id: int) -> bool:
    chat = await impdb.find_one({"chat_id_toggle": chat_id})
    return bool(chat)

async def impo_on(chat_id: int) -> bool:
    await impdb.insert_one({"chat_id_toggle": chat_id})

async def impo_off(chat_id: int):
    await impdb.delete_one({"chat_id_toggle": chat_id})
