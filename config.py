from dataclasses import dataclass
from typing import List
from typing import Dict


@dataclass
class Archive:
    bots: bool
    users: bool
    chats: bool
    pinned: bool
    channels: bool
    display_time: int

    @staticmethod
    def from_dict(d: Dict) -> 'Archive':
        bots = d["bots"]
        users = d["users"]
        chats = d["chats"]
        pinned = d["pinned"]
        channels = d["channels"]
        display_time = d["display_time"]

        return Archive(bots, users, chats, pinned, channels, display_time)


@dataclass
class Unread:
    folder_id: int
    ignore_bots: bool
    const_chat: str
    lifetime: int
    ignore: List[str]

    @staticmethod
    def from_dict(d: Dict) -> 'Unread':
        folder_id = d["folder_id"]
        ignore_bots = d["ignore_bots"]
        const_chat = d["const_chat"]
        lifetime = d["lifetime"]
        ignore = d["ignore"]

        return Unread(folder_id, ignore_bots, const_chat, lifetime, ignore)


@dataclass
class Config:
    api_id: str
    api_hash: str
    unread: Unread
    archive: Archive

    @staticmethod
    def from_dict(d: Dict) -> 'Config':
        api_id = d["api_id"]
        api_hash = d["api_hash"]
        unread = Unread.from_dict(d["unread"])
        archive = Archive.from_dict(d["archive"])

        return Config(api_id, api_hash, unread, archive)
