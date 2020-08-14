from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import json
import os
from discord.ext import commands
import discord


class ChatBridgeBot(commands.Bot):
	def __init__(self, **options):
		config = {
			"token": None,
			"channel_one": None,
			"channel_two": None,
			"webhook_url_one": None,
			"webhook_url_two": None
		}
		if os.path.isfile("./config.json"):
			with open("./config.json", "r") as f:
				config = json.load(f)
		if not config["token"]:
			print("Type in the bot token")
			config["token"] = input()
		if not config["channel_one"]:
			print("Type in the channel_id for the first channel")
			config["channel_one"] = int(input())
		if not config["channel_two"]:
			print("Type in the channel_id for the second channel")
			config["channel_two"] = int(input())
		if not config["webhook_url_one"]:
			print("Type in the URL of the webhook in the first channel")
			config["webhook_url_one"] = input()
		if not config["webhook_url_two"]:
			print("Type in the URL of the webhook in the first channel")
			config["webhook_url_two"] = input()

		with open("./config.json", "w+") as f:
			json.dump(config, f)

		self.channel_ids = [
			config["channel_one"],  # First servers channel to be linked
			config["channel_two"]  # Second servers channel to be linked
		]
		self.webhook_urls = [
			config["webhook_url_one"],  # First servers webhook url
			config["webhook_url_two"]   # Second servers webhook url
		]
		self.token = config["token"]

		super().__init__(command_prefix="!", **options)

	@staticmethod
	async def on_ready():
		print(f"Logged in as {bot.user}\n{bot.user.id}\nI'm up and running :]")

	async def on_message(self, msg):
		if msg.channel.id in self.channel_ids and not str(msg.author).endswith('#0000'):
			files = [await attachment.to_file() for attachment in msg.attachments]
			embed = msg.embeds[0] if msg.embeds else None
			async with aiohttp.ClientSession() as session:
				webhook_url = self.webhook_urls[0] if msg.channel.id == self.channel_ids[1] else self.webhook_urls[1]
				webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
				await webhook.send(
					msg.content, username=msg.author.name, avatar_url=msg.author.avatar_url, files=files, embed=embed
				)

	def run(self):
		super().run(self.token)


bot = ChatBridgeBot(max_messages=100)
bot.allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=False)
bot.run()
