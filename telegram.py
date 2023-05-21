from telethon import sync
import telethon.tl.functions as functions


def provide_client(api_id: str, api_hash: str) -> sync.TelegramClient:
    return sync.TelegramClient("session", api_id, api_hash)


async def get_folders(client: sync.TelegramClient):
    return await client(functions.messages.GetDialogFiltersRequest())
