import os
import asyncio
import json
import toml
import dotenv
from telethon import sync
import telethon.tl.functions.messages as functions
from telethon.tl.types import DialogFilter, DialogFilterDefault
import unread
import utils

dotenv.load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
ONE_TO_ONE_FOLDER = 118
SLEEP = 5


async def main():
    async with sync.TelegramClient("session", API_ID, API_HASH) as client:
        while True:
            dialogs = await client.get_dialogs(archived=False)
            await unread.handle(client, dialogs)
            await asyncio.sleep(SLEEP)


if __name__ == "__main__":
    asyncio.run(main())
