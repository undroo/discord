import os
import random

#covid API
import requests
import json

#discord stuff
import discord
import asyncio
from discord import TextChannel, abc, Message
from discord.ext import commands
from dotenv import load_dotenv

#decrypto stuff
from database import *

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

@bot.command(name='roll', help='number of dice, number of sides')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    if number_of_dice is None or number_of_sides is None:
        await ctx.send("Missing information, please insert: number of dice, number of sides")
    
    out = ""
    for i in range(number_of_dice):
        number_gen = random.randint(1,number_of_sides)
        out = out + str(number_gen) + " "
    await ctx.send(out)

#random fun stuff
@bot.command(name='activate', help='use at your own peril')
async def activate(ctx):
    #basically covers if the author is the bot and avoids recursively sending itself a message
    response = "YOU JUST ACTIVATED MY TRAP CARD\nhttps://tenor.com/view/yugioh-yami-yugi-atem-draws-gif-5742435"
    await ctx.send(response)

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

# COVID commands
@bot.command(name='covid', help='random covid stuff')
async def covid(ctx, *args):
    url = "https://api.covid19api.com/summary"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)
    result = json.loads(response.text)
    
    country = " ".join(args[:])
    country.strip()
    for country_data in result["Countries"]:
        if country_data["Country"].lower() == country.lower():
            output = country_data
    
    out = ""
    for x,y in output.items():
        if x == "Slug":
            pass
        else:
            out = out + str(x) + ": " + str(y) + "\n"
   # print(out)

    await ctx.send(str(out))
    await ctx.send("Last updated: " + str(result["Date"]))

# red flags stuff



# decrypto
@bot.command(name='decrypto_roll', help='number of dice, number of sides')
async def decrypto_roll(ctx):
    out = []
    total = 1
    while total <= 3:
        rand_num = random.randint(1,4)
        if rand_num not in out:
            out.append(rand_num)
            total += 1

    await ctx.send(out)

@bot.command(name='insert', help='insert into word list for decrypto')
async def insert(ctx, *args):
    conn = create_connection("decrypto.db")
    for arg in args:
        try:
            insert_into_table(conn,arg.lower())
        except Error as e:
            await ctx.send(e)
    await ctx.send("Added to list")
    conn.commit()
    conn.close()

@bot.command(name='remove_word', help='remove word from list')
async def word_removal(ctx, *args):
    conn = create_connection("decrypto.db")
    for arg in args:
        try:
            delete_from_table(conn,arg.lower())
        except Error as e:
            await ctx.send(e)
    await ctx.send("Removed from list")

    conn.commit()
    conn.close()

@bot.command(name='pull_all', help='gets all the words from the decrypto word list')
async def pull_all(ctx):
    conn = create_connection("decrypto.db")
    rows = select_from_table(conn)
    out = ""
    for row in rows:
        out = out + row[0] + "\n"
    await ctx.send(out)
    conn.commit()
    conn.close()

@bot.command(name='word_generate', help='generates a number of words')
async def word_generate(ctx):
    await ctx.send("Your words are: ")
    conn = create_connection("decrypto.db")
    rows = select_from_table(conn)
    random_list = []
    for row in rows:
        random_list.append(row[0])
    random.shuffle(random_list)
    random_list = random.sample(random_list, k=4)
    await ctx.send(" ".join(random_list))
    conn.close()



bot.run(TOKEN)