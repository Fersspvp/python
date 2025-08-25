import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import yt_dlp
from collections import deque
import re
import getpass
from discord.ui import View, Button

# ----- Intents -----
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ----- Globale Variablen -----
ALLOWED_ROLES = ["Admin", "Moderators", "Owner"]
owner = [1278754690582188158, 1405281511158055053]
queues = {}
TICKET_EMOJI = "🎫"

ADMIN_ROLE_ID = 1392592314714685580
MOD_ROLE_ID = 1385248655446900786

# Badwords einlesen
with open("en.txt", "r") as f:
    badwords = f.read().splitlines()

# ----- Rollen Check -----
def rollen_check(interaction: discord.Interaction):
    if not interaction.guild:
        return False
    user_roles = [role.name.lower() for role in interaction.user.roles]
    return any(allowed_role.lower() in user_roles for allowed_role in ALLOWED_ROLES)

# ----- Events -----
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot eingeloggt als {bot.user}. Slash-Commands global synchronisiert!")

@bot.event
async def on_member_join(member):
    kanal = member.guild.system_channel or discord.utils.get(member.guild.text_channels, name="willkommen")
    if kanal:
        await kanal.send(f"Herzlich Willkommen auf dem Server, {member.mention}!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if any(word in message.content.lower() for word in badwords):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, this server doesnt allow swear words if you have a issue open a ticket in the ticket channel", delete_after=5)
    await bot.process_commands(message)

# ----- Slash Commands -----
@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(member="The member to ban", reason="Reason for the ban")
@app_commands.check(rollen_check)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        await interaction.response.send_message("You cannot ban yourself.", ephemeral=True)
        return
    if member == interaction.guild.me:
        await interaction.response.send_message("I cannot ban myself.", ephemeral=True)
        return
    if interaction.user.top_role <= member.top_role:
        await interaction.response.send_message("You cannot ban a member with an equal or higher role.", ephemeral=True)
        return
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Member {member} has been banned.\nReason: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("I lack the permissions to ban this member.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("Failed to ban the member due to an unexpected error.", ephemeral=True)

@ban.error
async def ban_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.CheckFailure):
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)

@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.check(rollen_check)
@app_commands.describe(member="The member to kick", reason="Reason for the kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member} has been kicked. Reason: {reason}")
    except discord.Forbidden:
        await interaction.response.send_message("I lack the required permissions to kick this member.", ephemeral=True)
    except discord.HTTPException:
        await interaction.response.send_message("Failed to kick the member due to an unexpected error.", ephemeral=True)

@kick.error
async def kick_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.CheckFailure):
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)

@bot.tree.command(name="bot_info", description="Shows information about the bot")
async def bot_info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot Info",
        description="Custom bot made by ferssss for fritz.exe and pixel.network",
        color=discord.Color.red()
    )
    embed.add_field(name="Version", value="1.0.0", inline=True)
    embed.add_field(name="Owner", value="fritz.exe", inline=True)
    embed.add_field(name="Developer", value="ferssss", inline=True)
    embed.set_footer(text="Danke fürs Nutzen des Bots!")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1303769014635462728/64be2c5f2a798b593e3e38620ad565a7.png?size=1")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="server_info", description="Shows server information")
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(
        title=f"Server Info: {guild.name}",
        color=discord.Color.green()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Guild ID", value=guild.id, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Owner", value=str(guild.owner), inline=True)
    await interaction.response.send_message(embed=embed)

# ----- Reminder Command -----
@bot.tree.command(name="reminder", description="Reminds you after a certain time")
@app_commands.describe(time="Time like 10s, 5m, 2h, 1d", message="What to remind you about?")
async def reminder(interaction: discord.Interaction, time: str, message: str):
    def parse_time(t: str) -> int:
        pattern = r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?"
        match = re.fullmatch(pattern, t.strip().lower())
        if not match:
            return -1
        days, hours, minutes, seconds = [int(x) if x else 0 for x in match.groups()]
        return days*86400 + hours*3600 + minutes*60 + seconds

    seconds = parse_time(time)
    if seconds <= 0:
        await interaction.response.send_message("Example: `1h30m`, `45s`, `2d`", ephemeral=True)
        return
    if any(re.search(pattern, message, re.IGNORECASE) for pattern in badwords):
        await interaction.response.send_message("This bot cannot send bad words", ephemeral=True)
        return

    await interaction.response.send_message(f"I will remind you in {time}: **{message}**", ephemeral=True)
    await asyncio.sleep(seconds)
    try:
        await interaction.user.send(f"Reminder: **{message}**")
    except discord.Forbidden:
        await interaction.followup.send(f"{interaction.user.mention}, I couldn't DM you, but this was the reminder: **{message}**", ephemeral=True)

# ----- Ticket System -----
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton())

class TicketButton(Button):
    def __init__(self):
        super().__init__(label="Open Ticket", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        channel_name = f"ticket-{member.name.lower()}"
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"You already have a ticket: {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)
        await channel.send(f"{member.mention}, welcome to the support ticket", view=CloseView())

class CloseView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseButton())

class CloseButton(Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Closing ticket...", ephemeral=True)
        await interaction.channel.delete()

@bot.command()
async def ticketsetup(ctx):
    allowed_users = owner  # nur Owner
    if ctx.author.id not in allowed_users:
        await ctx.send("You cannot use this command.")
        return
    await ctx.send("Click to open a support ticket", view=TicketView())

@bot.command()
async def close(ctx):
    if ctx.channel.name.startswith("ticket-"):
        await ctx.send("Closing ticket...")
        await ctx.channel.delete()
    else:
        await ctx.send("This is not a ticket channel.")

# ----- Music Commands -----
def create_source(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extractaudio': True,
        'audioformat': 'mp3',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return discord.FFmpegPCMAudio(info['url'], options='-vn')

async def play_next(ctx, guild_id):
    queue = queues[guild_id]
    if queue:
        source = queue.popleft()
        voice_client = ctx.guild.voice_client
        voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, guild_id), bot.loop))
    else:
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect()

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined voice channel {channel.name}!")
    else:
        await ctx.send("You are not in a voice channel!")

@bot.command()
async def leave(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def play(ctx, *, url):
    guild_id = ctx.guild.id
    if guild_id not in queues:
        queues[guild_id] = deque()

    if not ctx.guild.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not in a voice channel!")
            return

    source = create_source(url)
    queues[guild_id].append(source)

    if not ctx.guild.voice_client.is_playing():
        await play_next(ctx, guild_id)
        await ctx.send(f"Now playing: {url}")
    else:
        await ctx.send(f"Added to queue: {url}")

@bot.command()
async def skip(ctx):
    if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.stop()
        await ctx.send("Skipped the current song!")
    else:
        await ctx.send("Nothing is playing right now!")

@bot.command()
async def pause(ctx):
    if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.pause()
        await ctx.send("Paused the song!")
    else:
        await ctx.send("Nothing is playing right now!")

@bot.command()
async def resume(ctx):
    if ctx.guild.voice_client and ctx.guild.voice_client.is_paused():
        ctx.guild.voice_client.resume()
        await ctx.send("Resumed the song!")
    else:
        await ctx.send("The song is not paused!")

# ----- Start Bot mit Token Input -----
token = getpass.getpass("Please enter your Discord Bot Token: ")
bot.run(token)
