from discord import Member

from discord.ext.commands import(
    command,
    has_permissions,
    Bot,
    Cog,
    Context
)


class Ban(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @Cog.listener()
    # async def on_member_ban(self, guild: Guild, user: User):
    #     return

    @command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: Member, *kwargs):
        if not member or member == ctx.author:
            await ctx.reply('You can\'t ban yourself')
            return

        reason = kwargs

        if not kwargs:
            reason = 'No reason given.'

        await ctx.guild.ban(member, reason=reason, delete_message_days=0)

        await ctx.channel.send(f':hammer: {member} has been banned.\n\n' +
                               f'Reason: {reason}')


def setup(bot):
    bot.add_cog(Ban(bot))
