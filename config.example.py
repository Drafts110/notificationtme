import os

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
    TEAM_CHAT_LINK = "https://t.me/+xuScRpBN9wA3YzU8"
    GENERAL_CHAT_LINK = "https://t.me/+Ck59B4YJOjRhOGQ0"
