import os
import random

import discord
import asyncio
from discord import TextChannel, abc, Message
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

@bot.command(name='clear_all', help='removes all message in the channel')
@commands.has_role('admin')
async def clear_all(ctx):
    await ctx.send("Bot in progress")
    async for message in abc.Messageable.history(ctx.message.channel,oldest_first=True):
        await Message.delete(message)
    await ctx.send("Welcome to your empty chat")

@bot.command(name='roll', help='number of dice, number of sides')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    if number_of_dice is None or number_of_sides is None:
        await ctx.send("Missing information, please insert: number of dice, number of sides")
    
    out = ""
    for i in range(number_of_dice):
        number_gen = random.randint(1,number_of_sides)
        out = out + str(number_gen) + " "
    await ctx.send(out)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "allan is gay" in message.content:
        await message.channel.send("True")
    await bot.process_commands(message)

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     await Message.delete(message)

# red flags
# decrypto
# 

bot.run(TOKEN)