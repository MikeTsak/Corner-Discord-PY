import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio


from music_cog import MusicCog
from ai_cog import AICog

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
# intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

asyncio.run(bot.add_cog(MusicCog(bot)))
asyncio.run(bot.add_cog(AICog(bot)))

bot.run(os.getenv("CLIENT_TOKEN"))
