from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from io import BytesIO
import requests
import os
from discord.ext import commands
import discord


class ChatBridgeBot(commands.Bot):
	def __init__(self, **options):
		self.channel_ids = [
			1234,  # First servers channel to be linked
			1234  # Second servers channel to be linked
		]
		self.webhook_urls = [
			'server1_webhook_url',  # First servers webhook url
			'server2_webhook_url'  # Second servers webhook url
		]
		self.token = ""

		super().__init__(command_prefix="!", **options)

	@staticmethod
	async def on_ready():
		print(f"Logged in as {bot.user}\n{bot.user.id}\nI'm up and running :]")

	async def on_message(self, msg):
		if msg.channel.id in self.channel_ids and not str(msg.author).endswith('#0000'):
			file = await msg.attachments[0].to_file() if msg.attachments else None
			async with aiohttp.ClientSession() as session:
				webhook_url = self.webhook_urls[0] if msg.channel.id == self.channel_ids[1] else self.webhook_urls[1]
				webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
				await webhook.send(
					msg.content, username=msg.author.name, avatar_url=msg.author.avatar_url, file=file
				)

	def run(self):
		super().run(self.token)


bot = ChatBridgeBot(max_messages=100)
bot.allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=False)
bot.run()
