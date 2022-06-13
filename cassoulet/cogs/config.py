from typing import Union
from dataclasses import dataclass
from loguru import logger

from discord.ext.commands import(
    command,
    has_permissions,
    Bot,
    Cog,
    Context
)

from lib.db import CacheManager


@dataclass
class ConfigProp:
    name: str
    text_channel: bool = False
    role: bool = False
    flake: bool = False

    def __post_init__(self):
        if self.text_channel and self.role:
            raise TypeError(
                'You can\'t set both text_channel and role properties to True')

        if (self.text_channel or self.role) and self.flake:
            raise TypeError(
                'Flake properties can\'t be used with text_channel and role set to True')


class ConfigCommand(Cog):
    _config_props: list[ConfigProp] = [
        # ConfigProp(
        #     name='pinschannelid',
        #     text_channel=True
        # ),
        # ConfigProp(
        #     name='trafficchannelid',
        #     text_channel=True
        # )
    ]

    def __init__(self, bot: Bot):
        self.bot = bot
        self._cache_manager = CacheManager()

    @staticmethod
    def _vars(val: str) -> Union[str, bool]:
        # I know
        match val:
            case '0':
                return '0'
            case 'true':
                return True
            case 'false':
                return False
            case _:
                return str(val)

    @command()
    @has_permissions(administrator=True)
    async def config(self, ctx: Context, config_prop: str, config_value: str):
        if not any(prop.name == config_prop for prop in self._config_props):
            await ctx.reply(
                f'`{config_prop}` is not a valid configuration property. ' +
                'For more information about how you can configure Bonjour, ' +
                'checkout `.help config`')
            return

        if any(prop.name == config_prop and prop.text_channel and config_value != '0'
               for prop in self._config_props) and not self.bot.get_channel(int(config_value)):
            await ctx.reply(f'Channel ID `{config_value}` does not exist in this guild.\n\n' +
                            'If you want to disable this setting, simply set it to `0`. Example: ' +
                            f'\n\n`.config {config_prop} 0`')
            return

        if any(prop.name == config_prop and prop.flake and config_value not in ('true', 'false')
               for prop in self._config_props):
            await ctx.reply(f'`{config_prop}` can only be set to either `true` or `false`. Example:\n\n' +
                            f'`.config {config_prop} true`')
            return

        config_dict = {}
        config_dict[config_prop] = self._vars(config_value)

        logger.debug(
            f'Bot configuration updated for guild {ctx.guild} {config_dict}')

        bot_guild_config = self._cache_manager.get_guild_config(
            str(ctx.guild.id))

        self._cache_manager.set_guild_config(
            guildid=str(ctx.guild.id),
            config={
                **bot_guild_config.__dict__,
                **config_dict
            }
        )

        await ctx.reply(f'`{config_prop}` set to `{config_value}`')


def setup(bot):
    bot.add_cog(ConfigCommand(bot))
