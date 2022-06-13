from discord import Member

from discord.ext.commands import(
    command,
    Bot,
    Cog,
    Context
)


class Pfp(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def pfp(self, ctx: Context, member: Member = None):
        if not member:
            await ctx.send(ctx.author.avatar_url)
        else:
            await ctx.send(member.avatar_url)


def setup(bot):
    bot.add_cog(Pfp(bot))
