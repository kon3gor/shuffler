import utils
from telethon.types import User, Chat, Channel


dialogs_to_archive = dict()


def dialog_has_unread(dialog) -> bool:
    unread_mark = dialog.unread_mark
    unread_count = dialog.unread_count
    unread_mentions_count = dialog.unread_mentions_count
    unread_reactions_count = dialog.unread_reactions_count
    # Somehow group chats with topics has bajillion number of unread.
    # Use unread_mark as main criteria to overcome this issue
    # Idk why but this archives everything
    # return unread_mark and (unread_count > 0 or unread_mentions_count > 0 or unread_reactions_count > 0)
    return unread_mark or unread_count > 0 or unread_mentions_count > 0 or unread_reactions_count > 0


def should_archive(dialog):
    config = utils.get_config()

    if type(dialog.entity) is User and not config.archive.users:
        return False

    if type(dialog.entity) is Chat and not config.archive.chats:
        return False

    if type(dialog.entity) is Channel and not config.archive.channels:
        return False

    if type(dialog.entity) is User and dialog.entity.bot and not config.archive.bots:
        return False

    if dialog.dialog.pinned and not config.archive.pinned:
        return False

    if dialog_has_unread(dialog.dialog):
        return False

    return True


def add(dialog):
    if dialog.id not in dialogs_to_archive:
        current_date = utils.get_current_date()
        dialogs_to_archive[dialog.id] = (current_date, dialog)


def remove(dialog):
    if dialog.id in dialogs_to_archive:
        del dialogs_to_archive[dialog.id]


async def archive_dialogs():
    current_date = utils.get_current_date()
    config = utils.get_config()

    ids_to_archive = []
    for dialog_id, values in dialogs_to_archive.items():
        date, _ = values
        duration = (current_date - date).total_seconds()

        if duration >= config.archive.display_time:
            ids_to_archive.append(dialog_id)

    for id in ids_to_archive:
        _, dialog = dialogs_to_archive.pop(id)
        await dialog.archive()


async def handle(dialogs):
    for dialog in dialogs:
        if should_archive(dialog):
            add(dialog)
        else:
            remove(dialog)

    await archive_dialogs()
