import discord
from discord.ext import commands

from pytube import YouTube, Search

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
        print("Music Cog Loaded")

    def search_yt(self, item):
        try:
            # First, try to treat the input as a direct link.
            yt = YouTube(item)
        except Exception:
            # If it fails, treat the input as a search query.
            s = Search(item)
            if not s.results:
                return False
            yt = s.results[0]
        
        # get the highest resolution audio stream
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if not stream:
            return False
        return {'source': stream.url, 'title': yt.title, 'video_id': yt.video_id}

        
    def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True

            # Remove the song that has just been played.
            self.queue.pop(0)
            
            # Check again if there are songs left in the queue.
            if len(self.queue) > 0:
                m_url = self.queue[0][0]['source']
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            else:
                self.is_playing = False
        else:
            self.is_playing = False


    async def play_music(self, ctx):

        if len(self.queue) > 0:
            self.is_playing = True
            m_url = self.queue[0][0]['source']
            title = self.queue[0][0]['title']
            video_id = self.queue[0][0]['video_id']
            # print(self.queue[0][0])

            classic_yt_url = f"https://www.youtube.com/watch?v={video_id}"  # Construct classic YouTube URL

            if self.vc == None or not self.vc.is_connected() or self.vc == False:
                self.vc = await ctx.author.voice.channel.connect()

                if self.vc == None:
                    await ctx.send("No voice channel detected")
                    return
            else:
                await self.vc.move_to(ctx.author.voice.channel)

            # self.queue.pop(0)
            # Send the message indicating the song is now playing
            await ctx.send(f"Now playing: {title}\n{classic_yt_url}")

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False
            await ctx.send("Queue is empty")
        
    @commands.command(name="play",aliases=["p","π"], help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You are not in a voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword")
            else:
                await ctx.send("Song added to the queue")
                self.queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)
    
    @commands.command(name="pause",aliases=["pa"], help="Pauses the current song")
    async def pause(self, ctx):
        if self.vc.is_playing():
            self.vc.pause()
            self.is_paused = True
            self.is_playing = False
            await ctx.send("Paused ⏸️")
        elif self.is_paused():
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
    
    @commands.command(name="skip",aliases=["s","sk"], help="Skips the current song")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await ctx.send("Skipped ⏩")
            await self.play_music(ctx)

    @commands.command(name="queue",aliases=["q"], help="Shows the current queue")
    async def queue_info(self, ctx):
        retval = ""
        for i in range(0, len(self.queue)):
            retval += f"{i+1}. {self.queue[i][0]['title']}\n"
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Queue is empty")

    @commands.command(name="clear",aliases=["cl"], help="Clears the current queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.queue = []
        await ctx.send("Queue cleared")

    @commands.command(name="leave",aliases=["l"], help="Leaves the voice channel")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()