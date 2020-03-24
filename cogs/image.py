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

class Image(commands.Cog):
    """Image related commands."""

    def __init__(self, bot):
        self.bot = bot
        #Reserved for further ... stuff

    """Commands section"""

    @commands.command(no_pm=True)
    async def pic(self, ctx, text):
        """Retrieves a picture from the given query
        """
        imgurclient = ImgurClient("7aea8f3499a8c45", "8e47bce5d977e01723a9486a00d784d7286c5346")
        items = imgurclient.gallery_search(" ".join(text[1:len(text)]), advanced=None, sort='time', window='all', page=0)
        await ctx.send(items[0].link)

class ModuleNotFound(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

def setup(client):
    client.add_cog(Image(client))
