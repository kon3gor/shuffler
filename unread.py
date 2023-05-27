from telethon.types import User, DialogFilter, DialogFilterDefault
from telethon.tl.custom.dialog import Dialog
import utils
from telethon import sync
from telethon.functions import messages
import telegram

dialogs_to_move = {}


def should_move(dialog: Dialog):
    config = utils.get_config()
    if type(dialog.entity) is not User:
        return False

    if dialog.id in config.unread.ignore:
        return False

    if dialog.title in config.unread.ignore:
        return False

    if dialog.entity.username in config.unread.ignore:
        return False

    if dialog.entity.bot and config.unread.ignore_bots:
        return False

    if dialog.dialog.unread_mark:
        return True

    if dialog.dialog.unread_count > 0:
        return True

    if dialog.dialog.unread_mentions_count > 0:
        return True

    if dialog.dialog.unread_reactions_count > 0:
        return True

    return False


def add(dialog: Dialog):
    if dialog.id in dialogs_to_move:
        return

    dialogs_to_move.add(dialog.id)


def remove(dialog: Dialog):
    if dialog.id not in dialogs_to_move.keys():
        return

    dialogs_to_move.remove(dialog.id)


async def get_folder(client: sync.TelegramClient, folder_id: int) -> DialogFilter:
    folders = await telegram.get_folders(client)
    f = None
    for folder in folders:
        if type(folder) is DialogFilterDefault:
            continue
        if folder.id == folder_id:
            f = folder
            break
    return f


async def move_dialogs(client: sync.TelegramClient):
    config = utils.get_config()
    include_peers = []
    folder = await get_folder(client, config.unread.folder_id)
    for id in dialogs_to_move:
        dialog = await client.get_input_entity(id)
        include_peers.append(dialog)

    dialog = await client.get_input_entity(config.unread.const_chat)
    include_peers.append(dialog)
    folder.include_peers = include_peers
    request = messages.UpdateDialogFilterRequest(
        config.unread.folder_id,
        folder
    )
    await client(request)


async def handle(client, dialogs):
    for dialog in dialogs:
        if should_move(dialog):
            add(dialog)
        else:
            remove(dialog)
    await move_dialogs(client)
