from discord.ext.commands import (
    is_owner,
    command,
    Bot,
    Context,
    Cog
)


class TestLeave(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    @is_owner()
    async def test_leave(self, ctx: Context):
        self.bot.dispatch('member_remove', ctx.author)


def setup(bot):
    bot.add_cog(TestLeave(bot))
