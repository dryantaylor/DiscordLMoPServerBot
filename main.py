import discord
from discord.ext import commands
import praw
import multiprocessing
from cogs.redditCommands.code import load_reddit_API_info
import time
import os

def update_pictures():
    perSubPictureTotal = 51 #for some reason i need to do one more than i actually want, i dont know why
    #              (subname , link store file)
    subs = [("cats", "cat_pictures.txt"), ("dogpictures", "dog_pictures.txt"), ("snakes", "snake_pictures.txt"),
            ("rabbits", "bunny_pictures.txt")]

    while True:
        for subreddit,destination in subs:
            client_id, client_secret, user_agent = load_reddit_API_info()
            reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
            pictures = []
            x = 0
            for subbmission in reddit.subreddit(subreddit).hot(limit=1000):
                if subbmission.url.split(".")[-1] in ["png", "jpg", "jpeg"]:
                    pictures.append(subbmission.url)
                    x += 1
                if x == perSubPictureTotal:
                    break

                with open(f"./cogs/redditCommands/{destination}", "w") as file:
                    string = ""
                    for url in pictures:
                        string += f"{url}\n"
                    file.write(string)

                #  24hours = 86400 seconds
        time.sleep(86400)

prefix = "/"
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix= prefix,intents = intents)

@bot.event
async def on_ready():
    print(f"bot online as {bot.user.name}")

for folderName in os.listdir("./cogs"):
    if "code.py" in os.listdir(f"./cogs/{folderName}"):
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
    file_updater = multiprocessing.Process(target=update_pictures)
    file_updater.start()
    bot.run(secret)
    file_updater.join()
