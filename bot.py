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

async def add_cog(bot, cog):
    await bot.add_cog(cog)

asyncio.run(add_cog(bot, MusicCog(bot)))
asyncio.run(add_cog(bot, AICog(bot)))

bot.run(os.getenv("CLIENT_TOKEN"))
