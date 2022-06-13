from discord import Member

from discord.ext.commands import(
    command,
    has_permissions,
    Bot,
    Cog,
    Context
)


class Kick(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: Member, *kwargs):
        if not member or member == ctx.author:
            await ctx.reply('You can\'t ban yourself')
            return

        reason = kwargs

        if not kwargs:
            reason = 'No reason given.'

        await ctx.guild.kick(member, reason=reason)

        await ctx.channel.send(f'{member} has been kicked out.\n\n' +
                               f'Reason: {reason}')


def setup(bot):
    bot.add_cog(Kick(bot))
