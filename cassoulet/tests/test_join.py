from discord.ext.commands import (
    is_owner,
    command,
    Bot,
    Context,
    Cog
)


class TestJoin(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    @is_owner()
    async def test_join(self, ctx: Context):
        self.bot.dispatch('member_join', ctx.author)


def setup(bot):
    bot.add_cog(TestJoin(bot))
