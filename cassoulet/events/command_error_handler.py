from loguru import logger

from discord.ext.commands import (
    Context,
    Cog,
    CommandError,
    CommandNotFound
)


class CommandErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def _get_instance_of_error(ctx: Context, error: CommandError):
        match type(error).__name__:
            case 'DisabledCommand':
                await ctx.send(f'{ctx.command} has been disabled.')
            case 'BadArgument':
                await ctx.send('I could not find that member. Please try again.')
            case 'CommandInvokeError' | 'Forbidden':
                await ctx.reply(f'Error running command `{ctx.command}`.' +
                                '\n\nPlease ensure Bonjour has `Administrator` permissions.')
                logger.exception(error)
            case 'MissingPermissions':
                await ctx.send('You can\'t run this command.')
            case 'MissingRequiredArgument':
                await ctx.reply('Invalid usage. If you need help with this command, simply run:' +
                                f'\n\n`.help {ctx.command}`')

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (CommandNotFound)

        if isinstance(error, ignored):
            return

        await self._get_instance_of_error(ctx, error)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
