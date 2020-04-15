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
import asyncpg


try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    uvloop = None

class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uptime = datetime.datetime.utcnow()
        self.commands_used = Counter()
        self.server_commands = Counter()
        self.socket_stats = Counter()
        self.shutdowns = []
        self.lotteries = dict()
        self.in_character = defaultdict(lambda: defaultdict(str))
        self.logger = logging.getLogger('discord')  # Discord Logging
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename=os.path.join('resources', 'discord.log'), encoding='utf-8',
                                           mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

        self.shutdowns.append(self.shutdown)


        with open("resources/dnditems.json", 'r') as dndf:
            self.dnditems = json.loads(dndf.read())

        with open("resources/dnditems.json", 'r') as dndf2:
            self.dndmagic = json.loads(dndf2.read())

        with open("resources/pokemonitems.json", 'r') as dndf3:
            self.pokemonitems = json.loads(dndf3.read())

        with open("resources/starwars.json", 'r') as swf:
            self.switems = json.loads(swf.read())


        self.db: db.Database = db.Database(self)
        self.di: data.DataInteraction = data.DataInteraction(self)
        self.default_udata = data.default_user
        self.default_servdata = data.default_server
        self.rnd = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.db.connect()

        with open("resources/newtranslations.json", 'rb') as trf:
            self.translations = json.loads(trf.read().decode())
            self.languages = ["en", "fr", "de", "ru", "es"]

        with open("resources/blacklist.json") as blf:
            self.blacklist = json.loads(blf.read())

        packages = [
            'cogs.economy',
            'cogs.inventory',
            'cogs.slaves',
            'cogs.salary',
            'cogs.music',
            'cogs.image',
            'cogs.gay',
            'cogs.getinfo',
            'cogs.client',
        ]

        for cog in packages:
            self.load_extension(cog)


        init_dd()
        self.stats = ThreadStats()
        self.stats.start()

        self._first = True

        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.db.connect())

    async def on_ready(self):
        await client.change_presence(status=discord.Status.idle , activity=discord.Game('with your mom'))
        print(f"We have logged in as {client.user}")

    @staticmethod
    def get_exp(level):
        return int(0.1 * level ** 2 + 5 * level + 4)

    @staticmethod
    def get_ram():
        """Get the bot's RAM usage info."""
        mem = psutil.virtual_memory()
        print(f"{mem.used / 0x40_000_000:.2f}/{mem.total / 0x40_000_000:.2f}GB ({mem.percent}%)")

    @staticmethod
    def format_table(lines, separate_head=True):
        """Prints a formatted table given a 2 dimensional array"""
        # Count the column width
        widths = []
        for line in lines:
            for i, size in enumerate([len(x) for x in line]):
                while i >= len(widths):
                    widths.append(0)
                if size > widths[i]:
                    widths[i] = size

        # Generate the format string to pad the columns
        print_string = ""
        for i, width in enumerate(widths):
            print_string += "{" + str(i) + ":" + str(width) + "} | "
        if not len(print_string):
            return
        print_string = print_string[:-3]

        # Print the actual data
        fin = []
        for i, line in enumerate(lines):
            fin.append(print_string.format(*line))
            if i == 0 and separate_head:
                fin.append("-" * (sum(widths) + 3 * (len(widths) - 1)))

        return "\n".join(fin)

    async def shutdown(self):
        with open("savedata/prefixes.json", 'w') as prf:
            json.dump(self.prefixes, prf)

        await self.session.close()

client = Bot(command_prefix= "ey ", pm_help=True, shard_count=7)
client.run('token')
