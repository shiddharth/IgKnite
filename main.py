'''
Veron1CA
An open source Discord Moderation Bot
'''


# Import default libraries.
import os
import sys
import time
import math
import random
import asyncio
import traceback
import functools
import itertools

# Import third-party libraries.
import discord
import youtube_dl
from discord.ext import commands
from async_timeout import timeout
from keep_alive import keep_alive


# Define command prefix and description.
prefix = os.getenv('COMMAND_PREFIX')
bot = commands.Bot(commands.when_mentioned_or('//'), description='Visit https://shiddharth.github.io/Veron1CA for more information about me. You can also ping me to access the commands!')

# Bug reports.
youtube_dl.utils.bug_reports_message = lambda: ''

class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass

# Opening wordlist file for word filter feature.
with open('filtered.txt', 'r') as filtered_wordfile:
    global filtered_wordlist
    global filtered_messages
    filtered_wordlist = filtered_wordfile.read().split()
    filtered_messages = list()

# Opening members list for jail command and guild list for freeze command.
global jail_members
jail_members = list()
global frozen
frozen = list()


# Events.
@bot.event
async def on_ready():
    os.system('clear')
    print("Veron1CA | Viewing Terminal\n")
    print(f"\nLog: {bot.user.name} has been deployed in total {len(bot.guilds)} servers.\n~~~")
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = f'{prefix}help, call me anytime! | Injected in {len(bot.guilds)} servers.'))

@bot.event
async def on_member_join(ctx, member):
    await member.send(f'Hi there, {member.mention}! Hope you enjoy your stay at {member.guild.name}!')

@bot.event
async def on_message(message):
    skip_command = False
    skip_swearcheck = False

    if message.author == bot.user:
        return

    if not message.author.bot:
        for frozen_guild in frozen:
            if frozen_guild[1] == message.guild:
                if frozen_guild[0] != message.author:
                    await message.delete()
                    skip_command = True
                    skip_swearcheck = True

        if skip_swearcheck != True:
            msg = message.content
            symbols = ['?', '.', ',', '(', ')', '[', ']', '{', '}', '+', '-', '/', '=', '_', '*', '&', '!', '@', '#', '$', '%', '^', '<', '>', '`', '~']

            for msg_word in msg.split():
                for symbol in symbols:
                    if symbol in msg_word:
                        msg_word = msg_word.replace(symbol, '')

                for filtered_word in filtered_wordlist:
                    if filtered_word.lower() == msg_word.lower():
                        filtered_messages.append([message.author, message.guild, message.content, message.created_at])
                        await message.delete()
                        skip_command = True

                    elif filtered_word.lower() in msg_word.lower():
                        await message.add_reaction('😠')

            for jail_member in jail_members:
                if jail_member[1] == message.guild:
                    if jail_member[0] == message.author:
                        if skip_command != True:
                            await message.delete()
                            skip_command = True

        if skip_command != True:
            await bot.process_commands(message)


# Moderation category commands.
class Moderation(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'Oops! {error}')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='sayhi', help='Helps to greet channel members.', aliases=['greet', 'welcome'])
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def sayhi(self, ctx, member: discord.Member):
        greeting_messages = [f"Hi {member.mention} Glad you're here.", f"Hello there! {member.mention}", f"Hey {member.mention}! Nice to meet you.", f"Hey, {member.mention} What's up?", f"Looks like someone just spoke my name. Anyway, how are you doing {member.mention}?", f"Happy to see you here, {member.mention}", f"Welcome! {member.mention} Have fun chatting!", f"Nice to meet you, {member.mention}! The name's {bot.user.name} by the way."]
        await ctx.message.delete()
        response = random.choice(greeting_messages)
        await ctx.send(response)

    @commands.command(name='ping', help='Shows the current response time of the bot.', aliases=['pong'])
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def ping(self, ctx):
        await ctx.message.delete()
        embed = (discord.Embed(title="Pong!", description="Showing current response time!", color=discord.Color.blurple()).add_field(value=f"{round(bot.latency * 1000)}ms", inline=False))
        await ctx.send(embed=embed)

    @commands.command(name='send-dm', help='Helps to send DMs to specific users.', aliases=['sdm'])
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def send_dm(self, ctx, user: discord.User, *, message):
        await user.send(f"**{message}**")
        await user.send(f"Sent by {ctx.author.display_name} using IgKnite :)")
        await ctx.send('DM Sent! :slight_smile:')
        time.sleep(1)
        await ctx.channel.purge(limit=2)

    @commands.command(name='clear', help='Clears messages inside the given index.', aliases=['cls'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def clear(self, ctx, amount=1):
        amount += 1
        await ctx.channel.purge(limit=amount)

    @commands.command(name='restore-msg', help='Tries to restore previously filtered message if it was deleted by mistake.', aliases=['rest-msg'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def restore_msg(self, ctx):
        filtered_messages_guild = []
        for filtered_message in filtered_messages:
            if filtered_message[1] == ctx.guild:
                filtered_messages_guild.append(filtered_message)
                filtered_messages.remove(filtered_message)

        if not filtered_messages_guild:
            await ctx.send('No messages were removed by me in the recent timeline.')

        else:
            await ctx.message.add_reaction('✅')
            for filtered_message_guild in filtered_messages_guild:
                await ctx.message.author.send(f'Author: {filtered_message_guild[0]}, Message: ||{filtered_message_guild[2]}||, Date: {filtered_message_guild[3]}')

    @commands.command(name='jail', help='Temporarily prevents a member from chatting in server.', aliases=['capture'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def jail(self, ctx, member: discord.Member, *, reason='none'):
        do_jail = False

        if member != ctx.message.author:
            if member.guild_permissions.administrator:
                if ctx.message.author.guild_permissions.administrator:
                    do_jail = True
                else:
                    await ctx.send('You can\'t jail an admin :/')
            else:
                do_jail = True

        else:
            await ctx.send('You can\'t jail yourself :/')

        if do_jail == True:
            jail_members.append([member, ctx.guild, reason, ctx.message.author])
            await ctx.message.delete()
            await ctx.send(f'You\'ve been captured! {member.mention} | Reason: {reason}')

    @commands.command(name='jailed', help='Views jailed members.', aliases=['view-jail'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def jailed(self, ctx):
        jailed_members_guild = []
        for jail_member in jail_members:
            if jail_member[1] == ctx.guild:
                jailed_members_guild.append(jail_member)

        if not jailed_members_guild:
            await ctx.send('No members are inside the jail!')

        else:
            for jailed_member_guild in jailed_members_guild:
                await ctx.send(f'**Prisoner!** | Name: {jailed_member_guild[0].mention} | Jailed By: {jailed_member_guild[3].mention} | Reason: {jailed_member_guild[2]}')

    @commands.command(name='unjail', help='Removes a member from jail.', aliases=['release'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def unjail(self, ctx, member: discord.Member):
        for jail_member in jail_members:
            if jail_member[1] == ctx.guild:
                if member != ctx.message.author:
                    if jail_member[0] == member:
                        jail_members.remove(jail_member)
                        await ctx.message.add_reaction('✅')

                else:
                    await ctx.send('You can\'t free yourself :/')

    @commands.command(name='mk-role', help='Creates a role.')
    @commands.has_role('BotAdmin')
    async def create_new_role(self, ctx, *, role):
        guild = ctx.guild
        await guild.create_role(name = role)
        await ctx.message.add_reaction('✅')

    @commands.command(name='rm-role', help='Removes an existing role.')
    @commands.has_role('BotAdmin')
    async def remove_role(self, ctx, *, role: discord.Role):
        if role is None:
            await ctx.send('That\'s not a role, I guess? :/')

        else:
            await role.delete()
            await ctx.message.add_reaction('✅')

    @commands.command(name='assign-role', help='Assigns an existing role to a server member.', pass_context=True)
    @commands.has_role('BotAdmin')
    async def assign_role(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f'Role {role.mention} has been given to {member.mention}, peace! :partying_face:')

    @commands.command(name='mk-ch', help='Creates a server channel.')
    @commands.has_role('BotAdmin')
    async def create_channel(self, ctx, channel_name):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            await guild.create_text_channel(channel_name)
            await ctx.message.add_reaction('✅')

    @commands.command(name='rm-ch', help='Removes an existing server channel.')
    @commands.has_role('BotAdmin')
    async def delete_channel(self, ctx, channel_name: discord.TextChannel):
        await channel_name.delete()
        await ctx.message.add_reaction('✅')

    @commands.command(name='freeze-chat', help="Calms down chat / freezes it.", aliases=['kill-chat'])
    @commands.has_role('BotAdmin')
    async def freeze(self, ctx):
        frozen.append([ctx.message.author, ctx.guild])
        await ctx.message.delete()
        await ctx.send(f'**Chat was frozen by {ctx.message.author.mention}!**')

    @commands.command(name='thaw-chat', help="Removes frozen state from chat.", aliases=['open-chat'])
    @commands.has_role('BotAdmin')
    async def thaw(self, ctx):
        for frozen_guild in frozen:
            if frozen_guild[1] == ctx.guild:
                frozen.remove(frozen_guild)
                await ctx.message.add_reaction('✅')

# Music category commands.
class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return "**{0.title}** by **{0.uploader}**".format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches **{}** :('.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches **{}** :('.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch **{}** :('.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for **{}**'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now vibin\' to:',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click here to redirect]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(180):
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Sorry, this command can\'t be used in DM channels :/')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('Oops! {}'.format(str(error)))

    @commands.command(name='join', help='Joins a specific voice channel.', invoke_without_subcommand=True)
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _join(self, ctx: commands.Context):
        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon', help='Summons IgKnite to a particular voice channel.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join :/')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', help='Clears the queue and leaves the voice channel.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _leave(self, ctx: commands.Context):
        if not ctx.voice_state.voice:
            return await ctx.send('I am not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume', help='Sets the volume of the player.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        if not ctx.voice_state.is_playing:
            return await ctx.send('There\'s nothing being played at the moment :/')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100 :/')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player is now set to **{}%**'.format(volume))

    @commands.command(name='now', help='Displays the currently playing song.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _now(self, ctx: commands.Context):
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause', help='Pauses the currently playing song.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _pause(self, ctx: commands.Context):
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume', help='Resumes a currently paused song.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _resume(self, ctx: commands.Context):
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop', help='Stops playing song and clears the queue.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _stop(self, ctx: commands.Context):
        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip', help='Vote to skip a song. The requester can automatically skip.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _skip(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now, so no skipping :/')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3** votes.'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song :/')

    @commands.command(name='queue', help='Shows the player\'s queue.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle', help='Shuffles the queue.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _shuffle(self, ctx: commands.Context):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('The queue is empty, play some songs, maybe?')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove', help='Removes a song from the queue at a given index.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _remove(self, ctx: commands.Context, index: int):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('The queue is empty, can\'t remove anything :/')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop', help='Loops the currently playing song.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _loop(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play', help='Plays a song.')
    @commands.has_any_role('BotPilot', 'BotMod', 'BotAdmin')
    async def _play(self, ctx: commands.Context, *, search: str):
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('Oops! An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel :/')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('I\'m already in a voice channel :/')


# Add cogs.
bot.add_cog(Moderation(bot))
bot.add_cog(Music(bot))

# Run the bot.
keep_alive()
bot.run(os.getenv('TOKEN'))