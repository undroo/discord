import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.command(name='activate', help='use at your own peril')
async def activate(ctx):
    #basically covers if the author is the bot and avoids recursively sending itself a message
    response = "YOU JUST ACTIVATED MY TRAP CARD\nhttps://tenor.com/view/yugioh-yami-yugi-atem-draws-gif-5742435"
    await ctx.send(response)

@bot.command(name='roll', help='number of dice, number of sides')
@commands.has_role('admin')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    out = ""
    for i in range(number_of_dice):
        number_gen = random.randint(1,number_of_sides)
        out = out + str(number_gen) + " "
    await ctx.send(out)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)