import asyncio
import praw
import discord
import youtube_dl
import random
import codecs
import logging
import wolframalpha
import time
import re
from discord.ext import commands
from bs4 import BeautifulSoup
import codecs
from urllib import parse
import json
import requests
import wikipedia
import datetime
import socket
from yandex_translate import YandexTranslate
import pkg_resources
from discord.ext import commands
import aiml
import os
import aiohttp
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from imgurpython import ImgurClient
from discord.ext.commands import clean_content
from cogs.utils.dataIO import fileIO
from random import randint
from io import BytesIO
from collections import Counter, defaultdict
from random import sample, seed
from cogs.utils import checks
import time
from random import choice
from pyhtml import server
import cogs
from cogs.utils import db, data
from cogs.utils.translation import _
import psutil
from datadog import ThreadStats
from datadog import initialize as init_dd
from cogs.chatdata.nmtchatbot.inference import inference

client=commands.Bot(command_prefix="ey ")

STARTUP_FILE = "std-startup.xml"

ipv4_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

ipv6_regex = re.compile(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')


yandex_translate = YandexTranslate('trnsl.1.1.20200115T181807Z.8e6b4604510292d3.d5719471240fb85faff34e0473257a8e31b5161f')

bot = wolframalpha.Client('625H23-RAK22L29HA')

lapi_key='e97dfc49e0a7a627d36d243dfdf3fc001afe28e6233e3a7d168cf172'

aiml_kernel = aiml.Kernel()
initial_dir = os.getcwd()
os.chdir(pkg_resources.resource_filename(__name__, ''))  # Change directories to load AIML files properly
startup_filename = pkg_resources.resource_filename(__name__, STARTUP_FILE)
aiml_kernel.learn(startup_filename)
aiml_kernel.respond("LOAD AIML B")
os.chdir(initial_dir)

reddit = praw.Reddit(client_id ="2Z8hwp0EVd0_vQ",
                     client_secret = "eJdhbSuqx2iTuVidz1FeADXEV-Y",
                     user_agent="Pink_Guy (by /u/Som_S_Som")

class Client(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    async def ban(self ,ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(client.latency * 1000)} ms')

    @commands.command()
    async def ask(self, ctx, *,query: str):
       try:
          try:
            res = bot.query(query)
                    ans = next(res.results).text
                    await ctx.send(ans)
                except:
                    r = wikipedia.summary(query, sentences=2)
                    await ctx.send(r)
            except:
                await ctx.send("Try again later")

    @commands.command()
    async def clear(self, ctx, amount = 10000):
        await ctx.channel.purge(limit=amount)

    @commands.command
    async def help(self, ctx):
        embed = discord.Embed(title="Nibba for the resque", description="Some useful commands to use nibba")
        embed.add_field(name=".ping", value="checks the ping")
        embed.add_field(name=".help", value="shows the commands")
        embed.add_field(name=".Pink", value="used for answering the questions")
        await message.channel.send(content=None, embed=embed)

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

    @commands.command()
    async def translate(self, ctx , *, query: str):
        await ctx.send(yandex_translate.translate( query , 'en')['text'][0])

    @commands.command(aliases=['pink'])
    async def boss(self, ctx, query: str):
            try:
                aiml_response = aiml_kernel.respond(query)
                await ctx.send(aiml_response)
            except:
                await ctx.send(inference(f'{query}')['answers'][0])

    @commands.command()
    async def meme(self, ctx):
        rnd = random.randint(0,5)
        memes = reddit.subreddit('memes').new(limit=7)
        post = [p for p in memes if not p.stickied][rnd]
        embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title="Memes")
        embed.set_author(name="Memes",icon_url="https://vignette.wikia.nocookie.net/filthy-frank/images/9/98/Salamander_Man2.png")
        embed.set_image(url=str(post.url))
        await ctx.send(embed=embed)


    @commands.command()
    async def show(self, ctx , query: str):
            rnd = random.randint(0,5)
            memes = reddit.subreddit(query).new(limit=7)
            post = [p for p in memes if not p.stickied][rnd]
            embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title="Random")
            embed.set_author(name="Random things",icon_url="https://vignette.wikia.nocookie.net/filthy-frank/images/9/98/Salamander_Man2.png")
            embed.set_image(url=str(post.url))
            await ctx.send(embed=embed)
    
    
    def lookup_ip(ip_address):
    	response = requests.get(f'https://api.ipdata.co/{ip_address}?api-key={lapi_key}')
    	response_json = json.loads(response.text)
    	return f'''
    ```
    IP: {str(response_json['ip'])}
    IP LOCATION INFO
    City: {str(response_json['city'])}
    Region: {str(response_json['region'])}
    Region code: {str(response_json['region_code'])}
    Country: {str(response_json['country_name'])}
    Country code: {str(response_json['country_code'])}
    Flag: {str(response_json['emoji_flag'])}
    Continent: {str(response_json['continent_name'])}
    Continent code: {str(response_json['continent_code'])}
    Postal code: {str(response_json['postal'])}
    Latitude: {str(response_json['latitude'])}
    Longitude: {str(response_json['longitude'])}
    Calling code: {str(response_json['calling_code'])}
    Time zone: {str(response_json['time_zone']['name'])}
    Time zone current time: {str(response_json['time_zone']['current_time'])}
    Currency: {str(response_json['currency']['name'])}
    Currency code: {str(response_json['currency']['code'])}
    Currency symbol: {str(response_json['currency']['symbol'])}
    Language: {str(response_json['languages'][0]['name'])}
    Native language: {str(response_json['languages'][0]['native'])}
    BASIC INFO
    asn: {str(response_json['asn']['asn'])}
    Name: {str(response_json['asn']['name'])}
    Domain: {str(response_json['asn']['domain'])}
    Route: {str(response_json['asn']['route'])}
    Type: {str(response_json['asn']['type'])}
    EXTRA INFO
    TOR: {str(response_json['threat']['is_tor'])}
    Proxy: {str(response_json['threat']['is_proxy'])}
    Anonymous: {str(response_json['threat']['is_anonymous'])}
    Abuser: {str(response_json['threat']['is_known_abuser'])}
    Threat: {str(response_json['threat']['is_threat'])}
    Bogon: {str(response_json['threat']['is_bogon'])}```'''

    @commands.command(aliases=['ip'])
    async def geo(self, ctx, *, ip):
    	"""looks up an ip address"""
    	#above is the description for the command

    	#runs the command
    	try:
    		#gets ip address
    		ip_address = socket.gethostbyname(ip)
    		#sends the info about the ip
    		await ctx.send(lookup_ip(ip_address))

    	#message if there is socket error aka if there is no such an ip or domain
    	except socket.gaierror:
    		await ctx.send('There is no such an ip or domain')

    	#if some other kind of error occurs
    	except:
    		await ctx.send('Error has occured!')
    		print('Error has occured!')
    @commands.command(pass_context=True)
    async def avatar(self, ctx, user: discord.Member=None):
        """Displays users avatar."""
        if not user:
            embed = discord.Embed(color=0x176cd5)
            embed = discord.Embed(title="View full image.", url=str(ctx.message.author.avatar_url), color=0x176cd5)
            embed.set_image(url=str(ctx.message.author.avatar_url))
            embed.set_author(name=ctx.message.author, icon_url=str(ctx.message.author.avatar_url))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0x176cd5)
            embed = discord.Embed(title="View full image.", url=str(user.avatar_url), color=0x176cd5)
            embed.set_image(url=str(user.avatar_url))
            embed.set_author(name=ctx.message.author, icon_url=str(ctx.message.author.avatar_url))
            await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def slap(self, ctx, member: discord.Member):
        """Slap someone."""
        embed = discord.Embed(title="Wapow!", description="**{1}** slaps **{0}**!".format(member.name, ctx.message.author.name), color=0x176cd5)
        embed.set_image(url="https://i.makeagif.com/media/6-28-2014/76yLMF.gif")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def punch(self, ctx, member: discord.Member):
        """Punch someone."""
        embed = discord.Embed(title="Kapow!", description="**{1}** punches **{0}**!".format(member.name, ctx.message.author.name), color=0x176cd5)
        embed.set_image(url="https://media1.tenor.com/images/e65569919a3f3afb15b062ee16cedf98/tenor.gif")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def shoot(self, ctx, member: discord.Member):
        """Shoot someone."""
        embed = discord.Embed(title="Pow Pow Pow!", description="**{1}** shoots **{0}**!".format(member.name, ctx.message.author.name), color=0x176cd5)
        embed.set_image(url="http://images.rapgenius.com/2a3d0051e08c975ab8c9449753de0d02.500x281x59.gif")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def kiss(self, ctx, member: discord.Member):
        """kisses."""
        embed = discord.Embed(title="MUAAAAAAAAAH", description="**{1}** shoots **{0}**!".format(member.name, ctx.message.author.name), color=0x176cd5)
        embed.set_image(url="https://thumbs.gfycat.com/GoldenReliableAmericanbadger-size_restricted.gif")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def lick(self, ctx, member: discord.Member):
        """licks."""
        embed = discord.Embed(title="*Slick* *Slick*", description="**{1}** shoots **{0}**!".format(member.name, ctx.message.author.name), color=0x176cd5)
        embed.set_image(url="https://static1.fjcdn.com/thumbnails/comments/Lick+de+pusi+b0ss+_635e1e6779e38ea8744f5766fd849d53.gif")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Client(client))
