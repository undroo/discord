# bot.py
import os

import discord
import asyncio
from discord import TextChannel, abc, Message
from discord.ext import commands
import discord
from dotenv import load_dotenv

# English dictionary related imports. 
import enchant 
from random_word import RandomWords

# Import other files. 
from word_ladder import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

#utility functions
@bot.command(name='clear_all', help='removes all message in the channel')
@commands.has_role('admin')
async def clear_all(ctx):
    await ctx.send("Bot in progress")
    async for message in abc.Messageable.history(ctx.message.channel,oldest_first=True):
        await Message.delete(message)
    await ctx.send("Welcome to your empty chat")

# Function to check if a word is acceptable for word ladder.

@bot.command(name='check', help='check if a word is acceptable for word ladder')
async def check(ctx, *args):
    if len(args) != 1:
        await ctx.send('Too many words')
    else: 
        word = args[0].strip()
        dictionary = enchant.Dict("en_US")
        if dictionary.check(word):
            await ctx.send('Word is acceptable')
        else: 
            await ctx.send('Word is not acceptable')


@bot.command(name='generate', help='generate two words for a round of word ladder, input for number of letters in word otherwise default is 4')
async def generate(ctx, *args):
    wordLength = 4
    if len(args) == 0:
        print('0 arguments')
        result = generate_words(wordLength)
        print(result)
        await ctx.send(result)
    elif len(args) == 1:
        print('1 argument')
        if is_number(args[0]):
            print('is a number')
            wordLength = int(args[0].strip())
            if wordLength > 7:
                await ctx.send('Try less letters')
            else:
                result = generate_words(wordLength)
                print(result)
                await ctx.send(result)
        else: 
            await ctx.send('Please use a number')
    else: 
        await ctx.send('incorrect number of arguments')

@bot.command(name='solve', help='insert two words to get the solution')
async def solve(ctx, *args):
    if len(args) == 2:
        word1 = args[0].strip()
        word2 = args[1].strip()
        dictionary = enchant.Dict("en_US")
        if dictionary.check(word1) and dictionary.check(word2):
            if len(word1) == len(word2):
                result = await find_path(word1,word2)
                await ctx.send(result)
            else:
                await ctx.send('Words need to match in length')
        else:
            await ctx.send('words are not accepted')
    else:
        await ctx.send('Please insert two words')

bot.run(TOKEN)