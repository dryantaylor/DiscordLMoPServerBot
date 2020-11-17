import discord
from discord.ext import commands
import json
import datetime
import random

import praw

class redditCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        #              (subname , link store file)
        self.subs = [("cats", "cat_pictures.txt"),("dogpictures","dog_pictures.txt"),("snakes","snake_pictures.txt"),("rabbits","bunny_pictures.txt")]
        self.update_pictures()
        self.lastUpdated = datetime.datetime.now()
        

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded cog {self.__class__.__name__}")

    @commands.command()
    async def cat_pic(self,ctx):
        imgFile = "./cogs/redditCommands/cat_pictures.txt"
        await self.send_random_link_from_file(ctx,imgFile)
        
    @commands.command()
    async def dog_pic(self, ctx):
        imgFile = "./cogs/redditCommands/dog_pictures.txt"
        await self.send_random_link_from_file(ctx,imgFile)
     
    
    @commands.command()
    async def snake_pic(self,ctx):
        imgFile = "./cogs/redditCommands/snake_pictures.txt"
        await self.send_random_link_from_file(ctx,imgFile)

    @commands.command()
    async def bnuuy_pic(self,ctx):
        imgFile = "./cogs/redditCommands/bunny_pictures.txt"
        await self.send_random_link_from_file(ctx, imgFile)
    
    def update_pictures(self):
        perSubPictureTotal = 50
        for subreddit,destination in self.subs:
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


    async def send_random_link_from_file(self,ctx,file):
        now = datetime.datetime.now()
        duration = now - self.lastUpdated
        if duration.days >= 1.0:
            self.update_pictures()
            self.lastUpdated = now

        with open(file, "r") as f:
            url = random.choice(f.readlines()).replace("\n", "")
        await ctx.send(url)

def setup(bot):
    bot.add_cog(redditCommands(bot))


def load_reddit_API_info():
    with open("logins.json","r") as file:
        dict = json.loads(file.read())
        return (dict["reddit_client_id"],dict["reddit_client_secret"],dict["reddit_user_agent"])

