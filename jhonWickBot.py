import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
import random

# Load .env file
load_dotenv()

# Check for required environment variables and raise an error if missing
required_vars = ['DISCORD_TOKEN', 'OTHER_ENV_VAR']
missing_vars = [var for var in required_vars if os.getenv(var) is None]

if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Get the token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# USERS WILL BE MOVED TO THIS CHANNEL IF THEY ARE DEAFEN OR MUTED
TARGET_CHANNEL_NAME = "lo k tan defen y Reni"
ROULETTE_CHANCE = 0.05

# INITIALIZE BOT
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("discord roulette is running...")
    discordRoulette.start()


@tasks.loop(seconds=5)
async def discordRoulette():
    # FOR EVERY SERVER THAT THE BOT IS IN
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            for member in channel.members:
                # Apply 0.05% (0.0005) chance to kick the user off the call
                if random.random() < ROULETTE_CHANCE:
                    try:
                        await member.move_to(None)
                        print(f"Kicked {member.name} from {channel.name}")
                    except Exception as e:
                        print(f"Could not kick {member.name}: {e}")


@tasks.loop(seconds=5)  # Check every 5 seconds
async def check_voice_channels():
    # FOR EVERY SERVER THAT THE BOT IS IN
    for guild in bot.guilds:
        target_channel = discord.utils.get(guild.voice_channels, name=TARGET_CHANNEL_NAME)
        # CHECK IF THE TARGET CHANNEL EXISTS
        if not target_channel:
            continue
        # CHECK EVERY CHANNEL IN THE SERVER THAT IS NOT THE TARGET CHANNEL
        for channel in guild.voice_channels:
            if channel != target_channel:
                for member in channel.members:
                    # IF THE USER IS MUTED AND DEAFENED, MOVE THEM TO TARGET CHANNEL
                    if (member.voice.mute or member.voice.self_mute) and (member.voice.deaf or member.voice.self_deaf):
                        await member.move_to(target_channel)
                        print(f"Moved {member.name} to {TARGET_CHANNEL_NAME}")
                        try:
                            print(f"Sent message to {member.name}")
                        except Exception as e:
                            print(f"Could not send message to {member.name}: {e}")

bot.run(TOKEN)
