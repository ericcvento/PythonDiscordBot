import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Template():
	name = '!template'

	desc = 'This does nothing. Developer only'

	synt = '!template'

	loop = False

	group = 'Owner'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	async def run(self, message):
		return

	async def stop(self, message):
		self.loop = False
