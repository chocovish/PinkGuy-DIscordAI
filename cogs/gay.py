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

client=commands.Bot(command_prefix="ey ")

class Gay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ship(self, ctx, name1 : clean_content, name2 : clean_content):
        shipnumber = random.randint(0,100)
        if 0 <= shipnumber <= 10:
            status = "Really low! {}".format(random.choice(["Friendzone ;(",
                                                            'Just "friends"',
                                                            '"Friends"',
                                                            "Little to no love ;(",
                                                            "ey b0ss , pink guy not approve man ;("]))
        elif 10 < shipnumber <= 20:
            status = "Low! {}".format(random.choice(["Still in the friendzone",
                                                     "Still in that friendzone ;(",
                                                     "There's not a lot of love there... ;("]))
        elif 20 < shipnumber <= 30:
            status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!",
                                                     "But there's a small bit of love somewhere",
                                                     "I sense a small bit of love!",
                                                     "But someone has a bit of love for someone..."]))
        elif 30 < shipnumber <= 40:
            status = "Fair! {}".format(random.choice(["There's a bit of love there!",
                                                      "There is a bit of love there...",
                                                      "A small bit of love is in the air..."]))
        elif 40 < shipnumber <= 60:
            status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO",
                                                          "It appears one sided!",
                                                          "There's some potential!",
                                                          "I sense a bit of potential!",
                                                          "There's a bit of romance going on here!",
                                                          "I feel like there's some romance progressing!",
                                                          "The love is getting there..."]))
        elif 60 < shipnumber <= 70:
            status = "Good! {}".format(random.choice(["I feel the romance progressing!",
                                                      "There's some love in the air!",
                                                      "I'm starting to feel some love!"]))
        elif 70 < shipnumber <= 80:
            status = "Great! {}".format(random.choice(["There is definitely love somewhere!",
                                                       "I can see the love is there! Somewhere...",
                                                       "I definitely can see that love is in the air"]))
        elif 80 < shipnumber <= 90:
            status = "Over average! {}".format(random.choice(["Love is in the air!",
                                                              "I can definitely feel the love",
                                                              "I feel the love! There's a sign of a match!",
                                                              "There's a sign of a match!",
                                                              "I sense a match!",
                                                              "A few things can be imporved to make this a match made in heaven!"]))
        elif 90 < shipnumber <= 100:
            status = "True love! {}".format(random.choice(["It's a match!",
                                                           "There's a match made in heaven!",
                                                           "It's definitely a match!",
                                                           "Love is truely in the air!",
                                                           "ey b0ss, pink guy approve man"]))

        if shipnumber <= 33:
            shipColor = 0xE80303
        elif 33 < shipnumber < 66:
            shipColor = 0xff6600
        else:
            shipColor = 0x3be801

        emb = (discord.Embed(color=shipColor, \
                             title="Love test for:", \
                             description="**{0}** and **{1}** {2}".format(name1, name2, random.choice([
                                                                                                        ":sparkling_heart:",
                                                                                                        ":heart_decoration:",
                                                                                                        ":heart_exclamation:",
                                                                                                        ":heartbeat:",
                                                                                                        ":heartpulse:",
                                                                                                        ":hearts:",
                                                                                                        ":blue_heart:",
                                                                                                        ":green_heart:",
                                                                                                        ":purple_heart:",
                                                                                                        ":revolving_hearts:",
                                                                                                        ":yellow_heart:",
                                                                                                        ":two_hearts:"]))))
        emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
        emb.add_field(name="Status:", value=(status), inline=False)
        emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
        emb.set_thumbnail(url="https://vignette.wikia.nocookie.net/filthy-frank/images/8/8c/Sticker%2C375x360.u3.png/revision/latest?cb=20160825123857&path-prefix=es")
        await ctx.send(embed=emb)

    @commands.command(aliases=['gay-scanner', 'gayscanner', 'gay'])
    async def gay_scanner(self, ctx,* ,user: discord.Member=None):
        """Gay sensor to detect gay users"""
        if not user:
            user = ctx.author.name
        gayness = random.randint(0,100)
        if gayness <= 33:
            gayStatus = random.choice(["No homo",
                                       "Ey boss , you not gay man",
                                       '"Only sometimes"',
                                       "Straight-ish",
                                       "No homo bro",
                                       "Girl-kisser",
                                       "Hella straight"])
            gayColor = 0xFFC0CB
        elif 33 < gayness < 66:
            gayStatus = random.choice(["Possible homo",
                                       "My gay-sensor is picking something up",
                                       "Ey boss , you gay man?",
                                       "Gay-ish",
                                       "Looking a bit homo",
                                       "lol half  g a y",
                                       "safely in between for now"])
            gayColor = 0xFF69B4
        else:
            gayStatus = random.choice(["LOL YOU GAY XDDD",
                                       "HOMO ALERT",
                                       "MY GAY-SESNOR IS OFF THE CHARTS",
                                       "STINKY GAY",
                                       "BIG GEAY",
                                       "Ey boss , fuck you man",
                                       "HELLA GAY"])
            gayColor = 0xFF00FF
        emb = discord.Embed(description=f"Gayness for **{user}**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus}")
        emb.set_author(name="Gay Censor™", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        emb.set_image(url="https://media1.tenor.com/images/fd2f4709084e5085182292d7902a06bc/tenor.gif")
        await ctx.send(embed=emb)
def setup(client):
    client.add_cog(Gay(client))
