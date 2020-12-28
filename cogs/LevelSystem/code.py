import json
import random
import time
from discord.ext import commands
from math import floor

class LevelSystem(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.fileLoc = "./cogs/LevelSystem/exp.json"
        with open(self.fileLoc,"r") as file:
            self.exp_table = json.load(file)
            #self.exp_table = {}
            #print(file.read())

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded cog {self.__class__.__name__}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id not in self.exp_table.keys():
            self.exp_table[str(member.id)] = [0,0,0]
            with open(self.fileLoc, "w") as file:
                json.dump(self.exp_table, file)



    @commands.Cog.listener()
    async def on_message(self,message):

        if not message.author.bot:
            try:
                minTimeBetween = 180 #3 mins in seconds
                currTime = int(time.time())
                if currTime - self.exp_table[str(message.author.id)][0] > minTimeBetween:
                    exp = self.exp_table[str(message.author.id)][1]
                    level = self.exp_table[str(message.author.id)][2]
                    self.exp_table[str(message.author.id)][0] = currTime #time since last exp gain
                    exp += random.randint(20,150) #exp in that level

                    changed = False
                    while True:
                        next_level_needed = self.calc_exp_to_next_level(level)
                        if exp > next_level_needed:
                            level+=1
                            exp-= next_level_needed
                            changed = True
                        else:
                            break
                    if changed:
                        await message.channel.send(f"{message.author.mention} leveled up\n```Level: {level} exp:\n{self.calc_exp_bar_draw([currTime,exp,level])} {exp}/{self.calc_exp_to_next_level(level)}```")

                    self.exp_table[str(message.author.id)][1] = exp
                    self.exp_table[str(message.author.id)][2] = level
                    with open(self.fileLoc,"w") as file:
                        json.dump(self.exp_table,file)

            except KeyError:
                await message.channel.send(f"A user isn't in the EXP table something is broken!!!!!!!")
            except Exception as e:
                print(e)

    @commands.Cog.listener()
    async def on_guild_join(self,ctx):
        print("hello")
        for member in ctx.members:
            if member.id not in self.exp_table.keys() and not member.bot:
                self.exp_table[str(member.id)] = [0, 0, 0]

        with open(self.fileLoc,"w") as file:
            json.dump(self.exp_table,file)




    @commands.command()
    async def exp(self,ctx):
        user = self.exp_table[str(ctx.author.id)]
        exp_to_next_level = self.calc_exp_to_next_level(user[2])

        exp_bar = self.calc_exp_bar_draw(user)
        rank,n_users = self.calc_user_rank(str(ctx.author.id))
        # ◕  ◔  ⬤  ○ ◐

        await ctx.send(f"{ctx.author.mention}\n```Level: {user[2]} rank: {rank}/{n_users}exp:\n{exp_bar} {user[1]}/{exp_to_next_level}```")


    def calc_exp_to_next_level(self,current_level):
        #TODO: decide an algortithm for a gradual exp to level up increase
        next_level = current_level+1
        return 1000

    def calc_exp_bar_draw(self,user):
        exp_bar_length = 10

                                    #EXAMPLES WILL ASSUME THE exp_bar_length = 10
        fullDot = 100/exp_bar_length #the %age equal to a ⬤  | e.g 100/10 = 10%
        half_dot = fullDot/2 #the %age equal to a ◐ | e.g 10/2 = 5%
        quart_dot = fullDot/4 #the %age equal to a ◔ | e.g 10/4  = 2.5%
        three_quart_dot = quart_dot * 3 #the %age equal to a ◕ | e.g 2.5 * 3 = 7.5%

        mid_point_between_dots = (fullDot - three_quart_dot)/2 #the mid point between the dot values, used to determine which dot is used

        exp_to_next_level = self.calc_exp_to_next_level(user[2] - 1)
        percentage = (user[1] / exp_to_next_level) * 100

        exp_bar = "⬤" * floor(percentage / fullDot)

        percentage -= fullDot * floor(percentage / fullDot)
        if percentage > (half_dot + mid_point_between_dots):
            exp_bar += "◕"
        elif percentage > quart_dot + mid_point_between_dots:
            exp_bar += "◐"
        elif percentage > mid_point_between_dots:
            exp_bar += "◔"

        exp_bar += "○" * (exp_bar_length - len(exp_bar))
        # ◕  ◔  ⬤  ○ ◐
        return exp_bar

    def calc_user_rank(self,user_id: str):

        user_level = int(self.exp_table[user_id][2])
        user_exp = int(self.exp_table[user_id][1])
        rank = 1
        n_users = 0
        user_id = user_id
        print(type(user_id))
        for user in self.exp_table.items():
            if user[0] != user_id:
                print(user)
                pass
                if int(user[1][2]) > user_level or (int(user[1][2]) == user_level and int(user[1][1]) > user_exp): #fiz
                    rank+=1

            n_users+=1

        return (rank,n_users)

def setup(bot):
    bot.add_cog(LevelSystem(bot))