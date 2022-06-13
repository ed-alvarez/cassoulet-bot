import textwrap

from discord import (
    utils,
    Message,
    Guild,
    Member,
    Webhook,
    RequestsWebhookAdapter,
    TextChannel,
    File,
    Embed
)

from discord.ext.commands import Bot, Cog

from lib.db import CacheManager


class OnMessagePin(Cog):
    _pins_channel: TextChannel = None

    def __init__(self, bot: Bot):
        self.bot = bot
        self._cache_manager = CacheManager()

    async def _handle_pins_offer(self, msg: Message):
        await msg.reply(textwrap.dedent(
            '''
            :wave: Hey there, seems like you've pinned a message.

            Did you know Bonjour has its own pinboard feature?

            To enable it, simply create a text channel named `pins`
            with the appropriate permissions, and all pinned messages
            will be transferred to said channel.
            '''
        ))

        self._cache_manager.set_guild_config(str(msg.guild.id), {
            'pinsoffermsg': True
        })

    async def _send_webhook(self, msg: Message, content: str,
                            files: list[File] = [], embeds: list[Embed] = []):
        msg_author: Member = msg.author
        display_name = msg_author.display_name
        discriminator = msg_author.discriminator

        webhook: Webhook = await self._pins_channel.create_webhook(
            name=f'{msg_author.display_name}_bonjour_pin')

        wh_client = Webhook.from_url(
            webhook.url, adapter=RequestsWebhookAdapter())

        wh_client.send(content,
                       username=f'{display_name}#{discriminator}',
                       avatar_url=msg_author.avatar_url,
                       files=files,
                       embeds=embeds,
                       allowed_mentions=None)

        wh_client.delete()

    async def _handle_pin(self, msg: Message):
        await msg.unpin()

        self._cache_manager.mark_pinned_msg(msg)

        files: list[File] = []
        embeds: list[Embed] = []

        if len(msg.attachments) > 0:
            for att in msg.attachments:
                att_file = await att.to_file()

                files.append(att_file)

        if len(msg.embeds) > 0:
            for i_embed in msg.embeds:
                embed: Embed = i_embed

                embeds.append(embed)

                if (embed.type == 'video' or embed.type == 'image'
                        or embed.provider is not None):
                    await self._send_webhook(msg, msg.content)
                    return

        await self._send_webhook(msg, msg.content, files, embeds)

    @Cog.listener()
    async def on_message_edit(self, msg: Message, msg_after: Message):
        if (not msg.pinned and not msg_after.pinned or
                msg.pinned and not msg_after.pinned):
            return

        c_guild: Guild = msg.guild

        guild_bot_conf = self._cache_manager.get_guild_config(str(c_guild.id))

        self._pins_channel = utils.get(c_guild.channels, name='pins')

        has_seen_pins_offer = guild_bot_conf.pinsoffermsg

        if not self._pins_channel and not has_seen_pins_offer:
            await self._handle_pins_offer(msg)
            return

        if self._pins_channel:
            await self._handle_pin(msg)


def setup(bot):
    bot.add_cog(OnMessagePin(bot))
