'''
Veron1CA
An open source Discord moderation bot.
'''


# Import default libraries.
import os
import sys
import math
import random
import asyncio
import traceback
import functools
import itertools
from datetime import datetime

# Import third-party libraries.
import discord
import youtube_dl
from discord.ext import commands
from async_timeout import timeout
from keep_alive import keep_alive

# Define command prefix and description.
prefix = os.getenv('COMMAND_PREFIX')
bot = commands.Bot(commands.when_mentioned_or(prefix), help_command=None)

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

# Creating variables for command uses.
last_restarted = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
global jail_members
jail_members = list()
global frozen
frozen = list()


# Events.
@bot.event
async def on_ready():
    os.system('clear')
    print(f'{bot.user.name} | Viewing Terminal\n')
    print(f'\nLog: {bot.user.name} has been deployed in total {len(bot.guilds)} servers.\n~~~')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{prefix}help and I\'m Injected in {len(bot.guilds)} servers!'))


@bot.event
async def on_member_join(ctx, member):
    await member.send(f'Hi there, {member.mention}! Hope you enjoy your stay at {member.guild.name}!')


@bot.event
async def on_message(message):
    skip_command = False
    skip_swearcheck = False
    skip_jail = False

    if message.author == bot.user:
        return

    for frozen_guild in frozen:
        if frozen_guild[1] == message.guild and frozen_guild[2] == message.channel and frozen_guild[0] != message.author:
            await message.delete()
            skip_command = True
            skip_swearcheck = True
            skip_jail = True

    if skip_swearcheck is not True:
        if not message.author.bot:
            msg = message.content
            symbols = ['?', '.', ',', '(', ')', '[', ']', '{', '}', '+', '-', '/', '=', '_', '*', '&', '!', '@', '#', '$', '%', '^', '<', '>', '`', '~']

            for msg_word in msg.split():
                for symbol in symbols:
                    if symbol in msg_word:
                        msg_word = msg_word.replace(symbol, '')

                for filtered_word in filtered_wordlist:
                    if filtered_word.lower() == msg_word.lower():
                        filtered_messages.append([message.author, message.guild, message.content])
                        await message.delete()
                        skip_command = True

                    elif filtered_word.lower() in msg_word.lower():
                        await message.add_reaction('😠')

    if skip_jail is not True:
        for jail_member in jail_members:
            if jail_member[1] == message.guild and jail_member[0] == message.author and skip_command is not True:
                await message.delete()
                skip_command = True

    if skip_command is not True:
        await bot.process_commands(message)


# Help command.
@bot.group(invoke_without_command=True)
async def help(ctx, cmd=None):
    if not cmd:
        embed = discord.Embed(title=f'It\'s {bot.user.name} onboard!', color=discord.Color.blurple())

        embed.add_field(name='Some quick, basic stuff...', value='I\'m an open source Discord music & moderation bot, and I can help you to manage your server properly. From assigning roles to freezing chat, there\'s a ton of stuff that I can do! Visit [my official website](https://shiddharth.github.io/Veron1CA) to learn more about me and maybe add me to your own Discord server. Peace!')
        embed.add_field(name='How to access me?', value=f'My default command prefix is `{prefix}` and you can type `{prefix}help all` to get an entire list of usable commands or `{prefix}help commandname` to get information on a particular command.', inline=False)
        embed.add_field(name='A handful of clickables!', value='[Invite Me](https://discord.com/api/oauth2/authorize?client_id=828196184845713469&permissions=808971638&scope=bot) / [View My Website](https://shiddharth.github.io/Veron1CA) / [Join My Discord Server](https://discord.gg/rxd5v4n6KV)', inline=False)

        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Help requested by {ctx.author.display_name}')
        await ctx.send(embed=embed)

    elif cmd.lower() == 'all':
        embed = discord.Embed(title='Here\'s an entire list of commands!', color=discord.Color.blurple())

        def get_cog_commands(cog_name):
            all_commands = str()
            cog = bot.get_cog(cog_name)
            for command in cog.get_commands():
                all_commands += f'`{command}` '
            return all_commands


        embed.add_field(name='Chill', value=get_cog_commands('Chill'))
        embed.add_field(name='Moderation', value=get_cog_commands('Moderation'))
        embed.add_field(name='Music', value=get_cog_commands('Music'))
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Command list requested by {ctx.author.display_name}')
        await ctx.send(embed=embed)

    else:
        for command in bot.commands:
            if str(command.name) == str(cmd.lower()):
                embed = (discord.Embed(title=f'Command Docs -> {command.name}', color=discord.Color.blurple()).add_field(name='Description', value=command.help).add_field(name='Type', value=command.cog_name).add_field(name='Usage', value=f'`{prefix}{command.name} {command.signature}`', inline=False).set_footer(icon_url=ctx.author.avatar_url, text=f'Command help requested by {ctx.author.display_name}'))

                aliases = str()
                if command.aliases == []:
                    aliases = "No aliases available!"
                else:
                    aliases = str(command.aliases).replace('[', '').replace(']', '').replace('\'', '')

                embed.add_field(name='Aliases', value=aliases, inline=False)
                await ctx.send(embed=embed)


# Chill category commands.
class Chill(commands.Cog):
    @commands.command(name='avatar', help='Shows a member\'s Discord avatar.')
    async def avatar(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.message.author

        embed = (discord.Embed(title='Here\'s what I found!', color=discord.Color.blurple()).set_image(url=member.avatar_url).set_footer(icon_url=ctx.author.avatar_url, text='This looks too fancy to be honest.'))
        await ctx.send(embed=embed)

    @commands.command(name='ping', help='Shows the current response time of the bot.', aliases=['pong'])
    async def ping(self, ctx):
        embed = (discord.Embed(title='Pong Status', color=discord.Color.blurple()).add_field(name='My Latency:', value=f'Running at {round(bot.latency * 1000)}ms', inline=False).add_field(name='Last Restarted:', value=f'On {last_restarted}', inline=False).set_footer(icon_url=ctx.author.avatar_url, text='Vibing in full force!'))
        await ctx.send(embed=embed)


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

        elif isinstance(error, commands.MissingRole):
            await ctx.send(f'Oops! {error}')

        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(f'Oops! {error}')

        elif isinstance(error, commands.errors.UserNotFound):
            await ctx.send(f'Oops! {error} Try mentioning or pinging them! You can also try using their ID as an argument.')

        elif isinstance(error, commands.errors.RoleNotFound):
            await ctx.send(f'Oops! {error} Try mentioning or pinging the role. You can also try using it\'s ID as an argument.')

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'Oops, {error} Try typing `//help commandname` if you don\'t know how to use the command.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(name='clear', help='Clears messages inside the given index.', aliases=['cls'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def clear(self, ctx, amount=1):
        amount += 1
        await ctx.channel.purge(limit=amount)

    @commands.command(name='sayhi', help='Helps to greet channel members.', aliases=['greet', 'welcome'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def sayhi(self, ctx, member: discord.Member):
        greeting_messages = [f"Hi {member.mention} Glad you're here.", f"Hello there! {member.mention}", f"Hey {member.mention}! Nice to meet you.", f"Hey, {member.mention} What's up?", f"Looks like someone just spoke my name. Anyway, how are you doing {member.mention}?", f"Happy to see you here, {member.mention}", f"Welcome! {member.mention} Have fun chatting!", f"Nice to meet you, {member.mention}! The name's {bot.user.name} by the way."]
        await ctx.message.delete()
        response = random.choice(greeting_messages)
        await ctx.send(response)

    @commands.command(name='userinfo', help='Shows all important information on a user.', aliases=['userdetails'])
    async def userinfo(self, ctx, user: discord.Member=None):
        if not user:
            user = ctx.author

        embed = (discord.Embed(title=f'{user.display_name}\'s Bio', color=discord.Color.blurple()))

        embed.add_field(name='Name', value=user.name).add_field(name='Nick', value=user.display_name)
        embed.add_field(name='ID', value=user.id).add_field(name='Discriminator', value=user.discriminator)
        embed.add_field(name='Bot Bool', value='Yes, execute it.' if user.bot else 'Nah, a human. Chill!')
        embed.add_field(name='Role Count', value=len(user.roles))
        embed.add_field(name='Discord Joining Date', value=user.created_at.strftime("%b %d, %Y"), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Imagine {user.display_name} being a hacker!')

        await ctx.send(embed=embed)

    @commands.command(name='send-dm', help='Helps to send DMs to specific users.', aliases=['sdm'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def send_dm(self, ctx, user: discord.User, *, message):
        embed = (discord.Embed(title=f'{ctx.author.display_name} has something up for you!', color=discord.Color.blurple()).add_field(name='Message:', value=message).set_footer(text='Delivered with <3 by Veron1CA!').set_thumbnail(url=ctx.author.avatar_url))
        await user.send(embed=embed)
        await ctx.send(f'{ctx.author.mention} your message has been sent!')
        await ctx.message.delete()

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
                webhook = await ctx.message.channel.create_webhook(name=filtered_message_guild[0].display_name)

            webhooks = await ctx.message.channel.webhooks()
            for webhook in webhooks:
                await webhook.send(filtered_message_guild[2], username=filtered_message_guild[0].display_name, avatar_url=filtered_message_guild[0].avatar_url)
                await webhook.delete()

    @commands.command(name='jail', help='Temporarily prevents a member from chatting in server.', aliases=['capture'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def jail(self, ctx, member: discord.Member, *, reason='For smacking the chips!'):
        do_jail = False

        if member != ctx.author:
            if member.guild_permissions.administrator:
                if ctx.author.guild_permissions.administrator:
                    do_jail = True
                else:
                    await ctx.send('You can\'t jail an admin!')
            else:
                do_jail = True

        else:
            await ctx.send('You can\'t jail yourself!')

        if do_jail is True:
            jail_members.append([member, ctx.guild, reason, ctx.author])
            await ctx.message.delete()
            await ctx.send(f'You\'ve been captured! {member.mention} | Reason: {reason}')

    @commands.command(name='jailed', help='Views jailed members.', aliases=['view-jail'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def jailed(self, ctx):
        jail_has_member = False
        embed = (discord.Embed(title='Now viewing the prison!', color=discord.Color.blurple()).set_footer(icon_url=ctx.author.avatar_url, text='Imagine all being a hacker!'))
        for jail_member in jail_members:
            if jail_member[1] == ctx.guild:
                embed.add_field(name=jail_member[0].display_name, value=('Jailed by ' + jail_member[3].mention + ' | Reason: `' + jail_member[2] + '`'), inline=False)
                jail_has_member = True

        if jail_has_member is False:
            await ctx.send('No members are inside the jail.')

        else:
            await ctx.send(embed=embed)

    @commands.command(name='unjail', help='Removes a member from jail.', aliases=['release'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def unjail(self, ctx, member: discord.Member):
        for jail_member in jail_members:
            if jail_member[1] == ctx.guild and jail_member[0] == member:
                if member != ctx.author:
                    jail_members.remove(jail_member)
                    await ctx.message.add_reaction('✅')

                else:
                    await ctx.send('You can\'t free yourself!')

    @commands.command(name='block', help='Blocks a user from chatting in a specific channel.')
    async def block(self, ctx, member: discord.Member, *, reason='For talking too much.'):
        await ctx.channel.set_permissions(member, send_messages=False)
        await ctx.message.delete()
        await ctx.send(f'You\'re now blocked from chatting, {member.mention} | Reason: {reason}')

    @commands.command(name='unblock', help='Unblocks a user.')
    async def unblock(self, ctx, member: discord.Member):
        await ctx.channel.set_permissions(member, overwrite=None)
        await ctx.message.add_reaction('✅')

    @commands.command(name='kick', help='Kicks a member from server.')
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def kick(self, ctx, member: discord.User, *, reason=None):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f'Member **{member.display_name}** has been kicked!')
        await ctx.message.add_reaction('✅')

    @commands.command(name='ban', help='Bans a member from server.')
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def ban(self, ctx, member: discord.User, *, reason=None):
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f'Member **{member.display_name}** has been banned!')
        await ctx.message.add_reaction('✅')

    @commands.command(name='bans', help='Shows a list of banned users in the server.', aliases=['banlist'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def bans(self, ctx):
        bans = await ctx.guild.bans()
        embed = (discord.Embed(title='Now viewing banned members!', color=discord.Color.blurple()).set_footer(icon_url=ctx.author.avatar_url, text='Good thing you banned them!'))
        if bans:
            for ban in bans:
                embed.add_field(name=ban.user, value=f'ID: `{ban.user.id}` | Reason: `{ban.reason}`', inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send('No members are banned from this server.')

    @commands.command(name='unban', help='Unbans a member in server.')
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def unban(self, ctx, member: discord.User):
        await ctx.guild.unban(member)
        await ctx.send(f'Member **{member.display_name}** has been unbanned!')
        await ctx.message.add_reaction('✅')

    @commands.command(name='roleinfo', help='Shows all important information related to a specific role.', aliases=['roledetails'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def roleinfo(self, ctx, role: discord.Role):
        embed = (discord.Embed(title=f'Role Information: {str(role)}', color=discord.Color.blurple()))
        embed.add_field(name='Creation Date:', value=role.created_at).add_field(name='Mentionable', value=role.mentionable)
        embed.add_field(name='Managed By Integration', value=role.is_integration()).add_field(name='Managed By Bot', value=role.is_bot_managed())
        embed.add_field(name='Role Position', value=role.position).add_field(name='Role ID', value=f'`{role.id}`')
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Requested by {ctx.author.display_name}')
        await ctx.send(embed=embed)

    @commands.command(name='invites', help='Shows all active server invite codes.', aliases=['invlist', 'allinv'])
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def invites(self, ctx):
        invites = await ctx.guild.invites()
        embed = (discord.Embed(title='Now viewing invite codes!', color=discord.Color.blurple()).set_footer(icon_url=ctx.author.avatar_url, text='Who created this fancy invites?!'))

        if not invites:
            await ctx.send('No invite codes have been generated.')

        else:
            invcount = 0
            for invite in invites:
                invcount += 1
                embed.add_field(name=invite, value=f'Uses: {invite.uses} | Inviter: {invite.inviter.name} | ID: `{invite.id}`', inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='mk-inv', help='Creates an invite code or link.')
    @commands.has_any_role('BotMod', 'BotAdmin')
    async def create_invite(self, ctx, max_age=60, max_uses=1, *, reason=None):
        if not reason:
            reason = f'Inviter: {ctx.author.display_name}'

        invite = await ctx.channel.create_invite(max_age=max_age, max_uses=max_uses, reason=reason)
        embed = (discord.Embed(color=discord.Color.blurple()).add_field(name='Link', value=invite).add_field(name='ID', value=f'`{invite.id}`').add_field(name='Channel', value=invite.channel).set_author(name='An invite was created!', icon_url=ctx.author.avatar_url))

        value = str()
        if invite.max_age == 0:
            value = 'Infinity'
        else:
            value = f'{invite.max_age} Seconds'

        embed.add_field(name='Lifetime', value=value).add_field(name='Max Uses', value=invite.max_uses)
        await ctx.send(embed=embed)

    @commands.command(name='rm-inv', help='Removes a previously generated invite code or link.')
    @commands.has_role('BotAdmin')
    async def remove_invite(self, ctx, invite_id):
        invites = await ctx.guild.invites()
        for invite in invites:
            if invite.id == invite_id:
                await invite.delete()
                await ctx.send('Invite deleted!')

    @commands.command(name='mk-role', help='Creates a role.')
    @commands.has_role('BotAdmin')
    async def create_new_role(self, ctx, *, role):
        await ctx.guild.create_role(name=role)
        await ctx.message.add_reaction('✅')

    @commands.command(name='rm-role', help='Removes an existing role.')
    @commands.has_role('BotAdmin')
    async def remove_role(self, ctx, *, role: discord.Role):
        if role is None:
            await ctx.send('That\'s not a role, I guess?')

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
    async def create_channel(self, ctx, *, channel_name):
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

    @commands.command(name='freeze-chat', help='Calms down chat.', aliases=['kill-chat'])
    @commands.has_role('BotAdmin')
    async def freeze(self, ctx):
        # TODO: Make freezes immortal against restarts.
        frozen.append([ctx.author, ctx.guild, ctx.message.channel])
        await ctx.message.delete()
        await ctx.send(f'**Chat was frozen by {ctx.author.mention}!**')

    @commands.command(name='thaw-chat', help='Removes frozen state from chat.', aliases=['open-chat'])
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
            raise YTDLError('Couldn\'t find anything that matches **{}**'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches **{}**'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch **{}**'.format(webpage_url))

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
            raise commands.NoPrivateMessage('Sorry, this command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('Oops! {}'.format(str(error)))

    @commands.command(name='join', help='Joins a specific voice channel.', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon', help='Summons bot to a particular voice channel.')
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', help='Clears the queue and leaves the voice channel.')
    async def _leave(self, ctx: commands.Context):
        if not ctx.voice_state.voice:
            return await ctx.send('I am not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume', help='Sets the volume of the player.')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        if not ctx.voice_state.is_playing:
            return await ctx.send('There\'s nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100 to execute the command.')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player is now set to **{}%**'.format(volume))

    @commands.command(name='now', help='Displays the currently playing song.')
    async def _now(self, ctx: commands.Context):
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause', help='Pauses the currently playing song.')
    async def _pause(self, ctx: commands.Context):
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume', help='Resumes a currently paused song.')
    async def _resume(self, ctx: commands.Context):
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop', help='Stops playing song and clears the queue.')
    async def _stop(self, ctx: commands.Context):
        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip', help='Vote to skip a song. The requester can automatically skip.')
    async def _skip(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now, so no skipping for you.')

        voter = ctx.author
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
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue', help='Shows the player\'s queue.')
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
    async def _shuffle(self, ctx: commands.Context):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('The queue is empty, play some songs, maybe?')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove', help='Removes a song from the queue at a given index.')
    async def _remove(self, ctx: commands.Context, index: int):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('The queue is empty, so nothing to be removed.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop', help='Loops the currently playing song.')
    async def _loop(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play', help='Plays a song.')
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
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('I\'m already in a voice channel.')


# Add available cogs.
bot.add_cog(Chill(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Music(bot))

# Run the bot.
keep_alive()
bot.run(os.getenv('TOKEN'))
