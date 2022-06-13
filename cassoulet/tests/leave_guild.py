from discord import utils

from discord.ext.commands import (
    is_owner,
    command,
    Bot,
    Context,
    Cog
)


class LeaveGuild(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    @is_owner()
    async def leave_guild(self, ctx: Context, *, guild_id: str):
        guild = utils.get(self.bot.guilds, guild_id=int(guild_id))

        if not guild:
            await ctx.send('I don\'t recognize that guild.')
            return

        await self.bot.leave_guild(guild)


def setup(bot):
    bot.add_cog(LeaveGuild(bot))
