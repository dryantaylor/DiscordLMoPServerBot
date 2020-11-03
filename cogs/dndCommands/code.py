import discord
from discord.ext import commands

import random

class dndCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"loaded cog {self.__class__.__name__}")


    @commands.command(help = "AdB + C : rolls A number of B sided die with a modifier of C")
    async def roll(self,ctx):
        try:
            out = "{} "
            msg = ctx.message.content
            try:
                numDie = int(msg.split(" ")[1].split("d")[0])
                dieType = int(msg.split(" ")[1].split("d")[1].split("+")[0].split("-")[0])
                mod = 0
                if msg.split("+")[-1] != msg:
                    mod = 1
                    mod *= int(msg.split("+")[-1])
                elif msg.split("-")[-1] != msg:
                    mod = -1
                    mod *= int(msg.split("-")[-1])

            except IndexError:
                await ctx.send("{} please format the command properly (IndexError)".format(ctx.message.author.mention));
                return
            except ValueError:
                await ctx.send("{} please format the command properly (ValueError)".format(ctx.message.author.mention));
                return
            modStr = f'+ {mod}' if mod > 0 else f'- {abs(mod)}' if mod < 0 else ''
            out += f"{numDie}d{dieType} {modStr} rolled : ("

            total = 0
            for i in range(0, int(numDie)):
                roll = random.randint(1, int(dieType))
                total+= roll
                out+= f"{roll} +"
            out= out[:-2]
            out += f") {modStr} = "
            out += f"{total} {modStr} = {max(1, total + mod)}"
            if len(out) < 2000:
                await ctx.send(out.format(ctx.message.author.mention));
            else:
                await ctx.send("{} to many dice have been rolled, roll fewer".format(ctx.message.author.mention))
        except Exception as e:
            await ctx.send(f"something has gone wrong, please tell Damien he can't code!!! (error: \n```{e}```)")
            return


def setup(bot):
    bot.add_cog(dndCommands(bot))