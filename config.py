from dataclasses import dataclass
from typing import List
from typing import Dict, Union


@dataclass
class Archive:
    bots: bool
    users: bool
    groups: bool
    pinned: bool

    @staticmethod
    def from_dict(d: Union[Dict, None]) -> 'Archive':
        bots = d.get("bots", None)
        users = d.get("users", None)
        groups = d.get("groups", None)
        pinned = d.get("pinned", None)

        return Archive(bots, users, groups, pinned)


@dataclass
class Unread:
    folder_id: int
    ignore_bots: bool
    const_chat: str
    lifetime: int
    ignore: List[str]

    @staticmethod
    def from_dict(d: Union[Dict, None]) -> 'Unread':
        folder_id = d.get("folder_id", None)
        ignore_bots = d.get("ignore_bots", None)
        const_chat = d.get("const_chat", None)
        lifetime = d.get("lifetime", None)
        ignore = d.get("ignore", None)

        return Unread(folder_id, ignore_bots, const_chat, lifetime, ignore)


@dataclass
class Config:
    api_id: str
    api_hash: str
    unread: Unread
    archive: Archive

    @staticmethod
    def from_dict(d: Union[Dict, None]) -> 'Config':
        api_id = d.get("api_id", None)
        api_hash = d.get("api_hash", None)
        unread = Unread.from_dict(d.get("unread", None))
        archive = Archive.from_dict(d.get("archive", None))

        return Config(api_id, api_hash, unread, archive)
