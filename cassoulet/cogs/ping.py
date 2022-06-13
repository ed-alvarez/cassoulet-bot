from discord.ext.commands import(
    command,
    Bot,
    Cog,
    Context
)


class Ping(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def ping(self, ctx: Context):
        await ctx.send('https://media.discordapp.net/emojis/726283695241297984.gif')


def setup(bot):
    bot.add_cog(Ping(bot))
