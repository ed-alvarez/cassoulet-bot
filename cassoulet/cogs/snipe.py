from discord import (
    Member,
    Webhook,
    RequestsWebhookAdapter,
    File
)

from discord.ext.commands import(
    command,
    Bot,
    Cog,
    Context
)

from io import BytesIO

from lib.db import CacheManager
from schemas.bot import GuildMessage


class Snipe(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._cache_manager = CacheManager()

    async def _send_webhook(self, ctx: Context, msg: GuildMessage):
        webhook: Webhook = await ctx.channel.create_webhook(
            name=f'{msg.display_name}_bonjour_snipe')

        wh_client = Webhook.from_url(
            webhook.url, adapter=RequestsWebhookAdapter())

        files: list[File] = []

        for f in msg.files:
            files.append(File(
                filename=f['filename'],
                fp=BytesIO(f['fp']),
                spoiler=f['spoiler']
            ))

        wh_client.send(msg.content,
                       username=msg.display_name,
                       avatar_url=msg.avatar,
                       files=files,
                       allowed_mentions=None)

        wh_client.delete()

    @command()
    async def snipe(self, ctx: Context, member: Member = None):
        if not member:
            member = ctx.author

        member_msgs = self._cache_manager.get_member_msgs(
            member)

        del_msgs = []

        for msg in member_msgs:
            if msg['deleted']:
                del_msgs.append(msg)

        if len(del_msgs) == 0:
            await ctx.reply('No messages found.')
            return

        g_msg = del_msgs[0]

        await self._send_webhook(ctx, GuildMessage(**g_msg))


def setup(bot):
    bot.add_cog(Snipe(bot))
