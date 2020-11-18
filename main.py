import discord
from discord.ext import commands
from multiprocessing import Process
from reddit_image_updater import update_pictures
import os

prefix = "/"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix= prefix,intents = intents)

@bot.event
async def on_ready():
    print(f"bot online as {bot.user.name}")

for folderName in os.listdir("./cogs"):
    if not folderName.endswith(".py") and "code.py" in os.listdir(f"./cogs/{folderName}"):
        bot.load_extension(f"cogs.{folderName}.code")
#bot.load_extension("cogs.redditCommands.code")

with open("logins.json","r") as file:
    import json
    dict = json.loads(file.read())
    secret = dict["discord_secret"]

@bot.command()
async def qauck(ctx):
    await ctx.send("QAUCK QAUCK")

if __name__ == "__main__":
    job = Process(target=update_pictures)
    job.start()
    bot.run(secret)
    job.join()
