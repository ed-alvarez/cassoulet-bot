from discord import Guild
from discord.ext.commands import Bot, Cog

from lib.db import CacheManager
from schemas.bot import BotConfig


class OnGuildJoin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._cache_manager = CacheManager()

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        if self._cache_manager.get_guild_config(str(guild.id)):
            return

        self._cache_manager.set_guild_config(
            guildid=str(guild.id),
            config=BotConfig(
                guildid=str(guild.id)
            ).__dict__
        )


def setup(bot):
    bot.add_cog(OnGuildJoin(bot))
