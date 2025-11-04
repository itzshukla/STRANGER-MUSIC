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
from typing import Union

class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)

IGNORED_ERROR_KEYWORDS = [
    "Nᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛ ғᴏᴜɴᴅ",
    "Please start videochat",
]

IGNORED_EXCEPTION_CLASSES = (
    # AssistantErr,  # ❌ Currently disabled
)

def is_ignored_error(err: Union[Exception, BaseException]) -> bool:
    """
    Determine if the error should be skipped from full logging.
    Matches:
    - Exception type (if enabled)
    - Known substrings in error message
    """
    if isinstance(err, IGNORED_EXCEPTION_CLASSES):
        return True

    err_str = str(err).lower()
    return any(keyword.lower() in err_str for keyword in IGNORED_ERROR_KEYWORDS)