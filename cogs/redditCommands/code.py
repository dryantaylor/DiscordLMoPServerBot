from discord.ext import commands
import json
import datetime
import random

perSubPictureTotal = 51
#              (subname , link store file)
subs = [("cats", "cat_pictures.txt"),("dogpictures","dog_pictures.txt"),("snakes","snake_pictures.txt"),("rabbits","bunny_pictures.txt")]
class redditCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


        #self.update_pictures()
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


    async def send_random_link_from_file(self,ctx,file):
        while True:
            with open(file, "r") as f:
                read = f.readlines()
                if len(read) >= perSubPictureTotal-1:
                    url = random.choice(read).replace("\n", "")
                    await ctx.send(url)
                    return


def setup(bot):
    bot.add_cog(redditCommands(bot))

def load_reddit_API_info():
    with open("logins.json","r") as file:
        dict = json.loads(file.read())
        return (dict["reddit_client_id"],dict["reddit_client_secret"],dict["reddit_user_agent"])