import os
import re
import sys
import asyncio
import discord
import time
import socket
import threading
from string import printable
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
from datetime import datetime
import random
import pkgutil

sys.dont_write_bytecode = True

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

# Chicken

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')

global obj_list
global channels_list
global modules
obj_list = []
channels_list = []

path = os.path.join(os.path.dirname(__file__), "plugins")
modules = pkgutil.iter_modules(path=[path])

class CustomClient(discord.Client):
	global obj_list
	global members_list
	global channels_list
	global modules

	conf_path = os.path.join(os.path.dirname(__file__), "plugins/configs")
	#conf_path = os.path.dirname(os.path.abspath(__file__))

	members_list = []

	def __init__(self, discord_intents: discord.Intents):
		super().__init__(intents=discord_intents)

		print('Init done')

	def get_class_name(self, mod_name):
		output = ""

		words = mod_name.split("_")[1:]

		for word in words:
			output += word.title()
		return output


	# Bot connects to discord server
	async def on_ready(self):
		print (f'{self.user} has connected to Discord!')

		for guild in client.guilds:
#			if guild.name == GUILD:
#				break

			print(
				f'\n{client.user} is connected to the following guild:\n'
				f'{guild.name}(id: {guild.id})\n'
			)

			file_name = str(guild.name) + '_' + str(guild.id) + '_conf.json'

			if not os.path.isfile(os.path.join(self.conf_path, file_name)):
				print('Guild configuration file not found. Creating...')
				with open(os.path.join(self.conf_path, file_name), 'w'):
					pass

			print('Member count: ' + str(guild.member_count))

			for member in guild.members:
				members_list.append(member.name)

			print('len(members_list): ' + str(len(members_list)))

			print ('Guild Roles:')
			for role in guild.roles:
				print('\t' + role.name)


			print ()

			print('Guild text channels:')
			for channel in guild.channels:
				if str(channel.type) == 'text':
					channels_list.append(channel)
					print('\t' + str(channel.name))

			print ()

		# This needs to be AFTER creating/importing guild config files
		for loader, mod_name, ispkg in modules:
			if (mod_name not in sys.modules) and (mod_name.startswith('plugin_')):
			
				loaded_mod = __import__(path+"."+mod_name, fromlist=[mod_name])

				class_name = self.get_class_name(mod_name)
				loaded_class = getattr(loaded_mod, class_name)

				instance = loaded_class(client)
				obj_list.append(instance)

		# Show all plugins and start all services that can be started
		print('Plugins loaded:')
		for obj in obj_list:
			print('\t' + str(obj.name))
			if obj.is_service:
				try:
					await obj.startService()
				except:
					continue

	async def on_guild_join(self, guild):
		file_name = str(guild.name) + '_' + str(guild.id) + '_conf.json'

		if not os.path.isfile(os.path.join(self.conf_path, file_name)):
			print('Guild configuration file not found. Creating...')
			with open(os.path.join(self.conf_path, file_name), 'w'):
				pass

		for obj in obj_list:
			print('Generating config for ' + str(obj.name))
			obj.generatePluginConfig(file_name)

	# Member joins the discord server
	async def on_member_join(self, member):
		print(f'{member.name}, welcome to the WillStunForFood server. Be sure to check out the "rules" channel so you can pick your roles. If you would like to support me, consider following me on Twitch at https://twitch.tv/willstunforfood')
		await member.create_dm()
		await member.dm_channel.send(f'{member.name}, welcome to the WillStunForFood server. Be sure to check out the "rules" channel so you can pick your roles. If you would like to support me, consider following me on Twitch at https://twitch.tv/willstunforfood')

	# Bot received a message on discord server
	async def on_message(self, message):
		try:
			output = '[' + str(datetime.now()) + '][' + str(message.channel.name) + ']'
		except:
			output = '[' + str(datetime.now()) + ']'

		# Ignore bot's own messages
		if message.author == client.user:
			return

		output = output + ' ' + message.author.name + ': ' + message.content

		print (output)

		# Work response
		if message.content == '!muster':
			await message.channel.send(message.author.mention + ' Here')

		# Check if multipart command
		if ' ' in str(message.content):
			cmd = str(message.content).split(' ')[0]
		else:
			cmd = str(message.content)

		for obj in obj_list:
			if cmd == obj.name:
				await obj.run(message, obj_list)
				break

intents = discord.Intents.all()
client = CustomClient(intents)

client.run(TOKEN)
client.main.start()
