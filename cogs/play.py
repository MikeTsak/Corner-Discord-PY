import discord
from discord.ext import commands

class PlayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, query: str):
        await ctx.send(f"Playing {query}")

    # You can add more commands related to this cog here...

def setup(bot):
    bot.add_cog(PlayCommand(bot))
