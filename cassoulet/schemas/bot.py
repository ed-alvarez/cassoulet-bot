from dataclasses import dataclass
from datetime import datetime
from discord import Attachment, Embed


@dataclass
class BotConfig:
    guildid: str = '0'

    pinsoffermsg: bool = False
    trafficoffermsg: bool = False


@dataclass
class MessageFile:
    filename: str
    fp: str
    spoiler: bool


@dataclass
class GuildMessage:
    guildid: str
    channelid: str
    memberid: str
    messageid: str
    date: datetime
    avatar: str
    display_name: str
    content: str
    files: list[MessageFile]
    deleted: bool
    pinned: bool
