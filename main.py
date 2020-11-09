import discord
from discord.ext import commands

import threading
import os

prefix = "/"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix= prefix,intents = intents)

"""
@bot.command()
async def load(ctx,extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f"cogs.{extension}")
"""

@bot.event
async def on_ready():
    print(f"bot online as {bot.user.name}")

for folderName in os.listdir("./cogs"):
    if "code.py" in os.listdir(f"./cogs/{folderName}"):
        bot.load_extension(f"cogs.{folderName}.code")


with open("logins.json","r") as file:
    import json
    dict = json.loads(file.read())
    secret = dict["discord_secret"]

@bot.command()
async def qauck(ctx):
    await ctx.send("QAUCK QAUCK")

bot.run(secret)

