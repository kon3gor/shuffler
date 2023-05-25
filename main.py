import utils
import asyncio
from telethon import sync
import unread
import archive

SLEEP = 5


async def main():
    config = utils.get_config()
    async with sync.TelegramClient("session", config.api_id, config.api_hash) as client:
        while True:
            dialogs = await client.get_dialogs(archived=False)
            await unread.handle(client, dialogs)
            await archive.handle(dialogs)
            await asyncio.sleep(SLEEP)


if __name__ == "__main__":
    asyncio.run(main())
