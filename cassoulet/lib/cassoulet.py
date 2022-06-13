import os
import sys
from loguru import logger

from pymongo.errors import (
    ServerSelectionTimeoutError,
    OperationFailure
)

from discord import Intents
from discord.ext.commands import Bot

from lib.config import Config
from lib.mongodb import load_mongo_client


class Cassoulet:
    _intents = Intents.default()

    _intents.members = True
    _intents.presences = True
    _intents.messages = True

    _bot = Bot(command_prefix='.',
               intents=_intents,
               help_command=None)

    _bot_config = Config()
    _mongo_db = load_mongo_client()

    def _load_cogs(self):
        for evt in os.listdir('cassoulet/events'):
            if evt.endswith('.py'):
                try:
                    self._bot.load_extension(f'events.{evt[:-3]}')
                    logger.debug(f'Loaded event {evt[:-3]}')
                except Exception as err:
                    logger.error(
                        f'Failed to load event {evt}\n{type(err).__name__}: {err}')

        for cog in os.listdir('cassoulet/cogs'):
            if cog.endswith('.py'):
                try:
                    self._bot.load_extension(f'cogs.{cog[:-3]}')
                    logger.debug(f'Loaded extension {cog[:-3]}')
                except Exception as err:
                    logger.error(
                        f'Failed to load extension {cog}\n{type(err).__name__}: {err}')

        for test_cmd in os.listdir('cassoulet/tests'):
            if test_cmd.endswith('.py'):
                try:
                    self._bot.load_extension(f'tests.{test_cmd[:-3]}')
                    logger.debug(f'Loaded test command {test_cmd[:-3]}')
                except Exception as err:
                    logger.error(
                        f'Failed to load extension {test_cmd}\n{type(err).__name__}: {err}')

    def _load_db(self):
        logger.info('Connecting to MongoDB...')

        try:
            server_info = self._mongo_db.server_info()

            logger.success(
                f'Connected to MongoDB - Version {server_info["version"]}')

            return True
        except OperationFailure as err:
            logger.error(
                f'Unable to connect to MongoDB: {err}')
        except ServerSelectionTimeoutError as err:
            logger.error(
                f'Unable to connect to MongoDB: {err}')

        return False

    def bootstrap(self):
        if not self._load_db():
            sys.exit(-1)

        self._load_cogs()
        self._bot.run(self._bot_config.DISCORD_TOKEN)
