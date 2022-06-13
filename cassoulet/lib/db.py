import pymongo
from discord import Message, Member, Asset
from loguru import logger
from typing import Union

from lib.mongodb import load_db

from schemas.bot import BotConfig, GuildMessage


class CacheManager:
    _db = load_db()

    def get_guild_config(self, guildid: str) -> Union[BotConfig, bool]:
        bot_config = self._db.get_collection('bot_config')

        res: dict = bot_config.find_one({
            'guildid': guildid
        })

        if not res:
            return False

        return BotConfig(
            guildid=guildid,
            pinsoffermsg=res.get('pinsoffermsg', False),
            trafficoffermsg=res.get('trafficoffermsg', False)
        )

    def set_guild_config(self, guildid: str, config: dict):
        bot_config = self._db.get_collection('bot_config')

        logger.debug(f'Set guild config to {config}')

        bot_config.update_one({
            'guildid': guildid
        }, {
            '$set': config
        }, upsert=True)

    def mark_pinned_msg(self, msg: Message):
        guild_messages = self._db.get_collection('guild_messages')

        guild_messages.update_one({
            'messageid': str(msg.id)
        }, {
            '$set': {
                'pinned': True
            }
        })

    def mark_deleted_msg(self, msg: Message):
        guild_messages = self._db.get_collection('guild_messages')

        guild_messages.update_one({
            'messageid': str(msg.id)
        }, {
            '$set': {
                'deleted': True
            }
        })

    def get_member_msgs(self, member: Member, limit: int = 50):
        guild_messages = self._db.get_collection('guild_messages')

        cur_msgs = guild_messages.find({
            'memberid': str(member.id)
        }, {'_id': 0}).limit(limit).sort('date', pymongo.DESCENDING)

        msgs = []

        for msg in cur_msgs:
            msgs.append(msg)

        return msgs

    async def cache_message(self, msg: Message):
        guild_messages = self._db.get_collection('guild_messages')

        avatar: Asset = msg.author.avatar_url
        files = []

        for att in msg.attachments:
            f = await att.to_file()

            files.append({
                'filename': f.filename,
                'fp': f.fp.getvalue(),
                'spoiler': f.spoiler
            })

        msg_obj = GuildMessage(
            guildid=str(msg.guild.id),
            channelid=str(msg.channel.id),
            messageid=str(msg.id),
            memberid=str(msg.author.id),
            avatar=f'{avatar.BASE}{avatar._url}',
            display_name=f'{msg.author.display_name}#{msg.author.discriminator}',
            content=msg.clean_content,
            date=msg.created_at,
            files=files,
            deleted=False,
            pinned=False
        )

        guild_messages.insert_one(msg_obj.__dict__)
