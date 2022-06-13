from discord import Message, MessageType
from discord.ext.commands import Bot, Cog

from lib.db import CacheManager


class OnMessage(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._cache_manager = CacheManager()

    @Cog.listener()
    async def on_message(self, msg: Message):
        if 'oracle' in msg.content.lower():
            await msg.delete()

        if msg.author.bot or msg.type != MessageType.default:
            return

        await self._cache_manager.cache_message(msg)
        return

    @Cog.listener()
    async def on_message_delete(self, msg: Message):
        if msg.author.bot:
            return

        self._cache_manager.mark_deleted_msg(msg)
        return


def setup(bot):
    bot.add_cog(OnMessage(bot))
