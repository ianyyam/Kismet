from asyncio.subprocess import PIPE
import asyncio
import discord
from discord.ext import commands
import asyncio
import random
import aiohttp
import json

from discord.message import Message
client = discord.Client(intents=discord.Intents.default())
intents=discord.Intents.all()
bot = commands.Bot(command_prefix="//", intents=intents, case_insensitive = True)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#startup
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#api for dictionary bot v2
async def getdef(word:str) -> dict:
    try:
        async with aiohttp.request('GET', f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}") as resp:
            d = json.loads(await resp.read())[0]
            return d['meanings'][0]['definitions'][0]['definition']
    except Exception as e:
        return "This word doesn't exist in my database. Check your spelling or try clicking the blue text above to see whether Google Dictionary has it or not."
async def getsen(word:str) -> dict:
    try:
        async with aiohttp.request('GET', f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}") as resp:
            d = json.loads(await resp.read())[0]
            return d['meanings'][0]['definitions'][0]['example']
    except Exception as e:
        return "There is no sentence for this word in my database."
async def getpofspeech(word:str) -> dict:
    try:
        async with aiohttp.request('GET', f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}") as resp:
            d = json.loads(await resp.read())[0]
            return d['meanings'][0]['partOfSpeech']
    except Exception as e:
        return "Part of speech unavailable."
async def getphonetic(word:str) -> dict:
    try:
        async with aiohttp.request('GET', f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}") as resp:
            d = json.loads(await resp.read())[0]
            return d['phonetics'][0]['text']
    except Exception as e:
        return "Phonetics unavailable."

#--------------------
#help section
@bot.command(name = "kismethelp") 
async def help(client):
    await client.send('Hello, I am Kismet, a bot that will provide you details about a word\'s definition, part of speech, and more! Try it out with \"//def [word you want to define]\"!')
    return

#dictionary bot
@bot.command(aliases = ['definition', 'def', 'd', 'define'])
async def clientsGetDef(client, word):
    embed = discord.Embed (
        title = "Definition of " + word + ":",
        url = "https://www.google.com/search?q=definition+of+" + word,
        description = "For now, this bot only accepts one word requests.",
        color = 0x9b59b6
        )

    embed.set_author(name = "Kismet", icon_url="https://static.dezeen.com/uploads/2022/01/la-piedad-sq2-411x411.jpg")
    embed.add_field(name = "Part of Speech", value = await (getpofspeech(word)), inline = True)
    embed.add_field(name = "Phonetics:", value = await (getphonetic(word)), inline = True)
    embed.add_field(name = "Definition:", value = await (getdef(word)), inline = False)
    embed.add_field(name = "Example Sentence:", value = await (getsen(word)), inline = False)
    #embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
    embed.set_footer(text="--------------------\nBot made by Ian Yam\nFor a list of available commands, type \"//kismethelp\"!")
    await client.send(embed = embed)
    return

with open("config.json", "r") as file:
    token = json.load(file)

bot.run(token["token"])
#https://discord.com/api/oauth2/authorize?client_id=970409144106496040&permissions=2348923904&scope=bot