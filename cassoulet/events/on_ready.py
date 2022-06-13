import discord
from loguru import logger
from discord import Activity, ActivityType
from discord.ext.commands import Bot, Cog


class OnReady(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        logger.success(
            f'Bonjour is now up and running using {discord.__version__}')

        await self.bot.change_presence(activity=Activity(
            type=ActivityType.playing,
            name='bonjour-backend@1.0.0+rc1'
        ))


def setup(bot):
    bot.add_cog(OnReady(bot))
