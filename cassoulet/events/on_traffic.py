import textwrap

from discord import (
    utils,
    Guild,
    Member,
    TextChannel,
    Webhook,
    RequestsWebhookAdapter
)

from discord.ext.commands import Bot, Cog

from lib.db import CacheManager


class OnTraffic(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self._cache_manager = CacheManager()

    async def _handle_traffic_offer(self, member: Member):
        guild: Guild = member.guild
        guild_owner: Member = guild.owner

        await guild_owner.send(textwrap.dedent(
            '''
            :wave: Hey there, a user has joined your guild

            Did you know Bonjour has a user welcomer feature too?

            To enable it, simply create a text channel named "traffic" with
            the appropriate permissions.
            '''
        ))

        self._cache_manager.set_guild_config(str(guild.id), {
            'trafficoffermsg': True
        })

    async def _send_webhook(self, member: Member, status: bool):
        guild_bot_conf = self._cache_manager.get_guild_config(
            str(member.guild.id))

        traffic_channel: TextChannel = utils.get(
            member.guild.channels, name='traffic')

        has_seen_traffic_offer = guild_bot_conf.trafficoffermsg

        if not traffic_channel and not has_seen_traffic_offer:
            await self._handle_traffic_offer(member)
            return

        if not traffic_channel:
            return

        webhook: Webhook = await traffic_channel.create_webhook(
            name=f'{member.display_name}_bonjour_traffic')

        action = 'joined' if status else 'left'

        wh_client = Webhook.from_url(
            webhook.url, adapter=RequestsWebhookAdapter())

        wh_client.send(action,
                       username=member.display_name,
                       avatar_url=member.avatar_url,
                       allowed_mentions=None)

        wh_client.delete()

    async def _alert_user(self, member: Member):
        ver_channel = utils.get(member.guild.channels, name='verification')

        if not ver_channel:
            return

        await ver_channel.send(f'Welcome <@{member.id}>\n\n' +
                               'Tag one of our admins if you want to access the server.')

    async def _handle_traffic(self, member: Member, status: bool):
        if status:
            await self._alert_user(member)

        await self._send_webhook(member, status)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        await self._handle_traffic(member, True)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        await self._handle_traffic(member, False)


def setup(bot):
    bot.add_cog(OnTraffic(bot))
