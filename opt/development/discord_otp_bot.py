# important imports
import os
import sys
import datetime
import pyotp
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio


# discord configurations
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)






