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

# Add the cogs directly
bot.add_cog(MusicCog(bot))
bot.add_cog(AICog(bot))

print("==================Bot is running==================")
print(os.getenv("CLIENT_TOKEN"))
bot.run(os.getenv("CLIENT_TOKEN"))