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
        if query=='Who developed you?':
            await ctx.send('Chr0m0s0m3s')
        elif query=='Who made you?':
            await ctx.send("Chr0m0s0mes")
        elif query=='Who developed you':
            await ctx.send('Chr0m0s0m3s')
        elif query=='Who made you':
            await ctx.send('Chr0m0s0m3s')
        elif query=='Who created you?':
            await ctx.send('Chr0m0s0m3s')
        elif query=="Who created you":
            await ctx.send("Chr0m0s0m3s")
        elif query=="Who is your creator?":
            await ctx.send("Chr0m0s0m3s")
        elif query=="Who is your creator":
            await ctx.send("Chr0m0s0m3s")
        elif query=='Who made you?':
            await ctx.send("Chr0m0s0mes")
        elif query=='who developed you':
            await ctx.send('Chr0m0s0m3s')
        elif query=='who made you':
            await ctx.send('Chr0m0s0m3s')
        elif query=='who created you?':
            await ctx.send('Chr0m0s0m3s')
        elif query=="who created you":
            await ctx.send("Chr0m0s0m3s")
        elif query=="who is your creator?":
            await ctx.send("Chr0m0s0m3s")
        elif query=="who is your creator":
            await ctx.send("Chr0m0s0m3s")
        elif query=='Cake hair recipe':
            await ctx.send("After all of the ingredients are gathered, Chefs Frank, Max and Ian get to work in preparing their cake, with HowToBasic and Mr. Pirate Man assisting. While preparing their cake, the Protégé drinks and vomits all of the milk used, similar to his mixing technique used in the first Cake video. They then add all of the ingredients they had harassed Youtubers for: piss from JoeySalads, chewed banana from Jontron, pubic hair from Jacksepticeye and KSI, toenail clippings from makemebad35 and Anthony Fantano, and ass hair from PewDiePie. They then went to Vsauce (who was sleeping outside with a bag of garbage), who gave interesting spit facts while they collected saliva from him. Then the cake was done.")

        else:
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
    async def roast(self, ctx , target: discord.Member ):
            responses = [", Without a doubt your mom is gay.",
            ", A little bit of weed, hard liquor for the ladies, got me feeling like a young Dan Schneider from the 80's, with the Jewish law firm and an all-black Mercedes and she's playing with the balls like Brady's",
            ", I hope you win the lottery and die the next day and your daughter has to see you getting lowered in your grave.",
            ", You are like a dick with a boy attached to it",
            ", No offense, but you make me want to staple my cunt shut.",
            ", Did your parents have any children that lived?",
            ", I’ll plant a mango tree in your mother’s cunt and fuck your sister in its shade.",
            ", You have more dick in your personality than you do in your pants.",
            ", You’re so stupid you couldn’t pour piss out of a boot if the directions were written on the heel.",
            ", You couldn’t organize a blowjob if you were in a Nevada brothel with a pocket full of hundred-dollar bills.",
            ", You couldn’t organize a blowjob if you were in a Nevada brothel with a pocket full of hundred-dollar bills.",
            ", People like you are the reason God doesn’t talk to us anymore.",
            ", You should put a condom on your head, because if you’re going to act like a dick you better dress like one, too.",
            ", May your balls turn square and fester at the corners.",
            ", I hope your wife brings a date to your funeral.",
            ", Your mother may have told you that you could be anything you wanted, but a douchebag wasn’t what she meant.",
            ", You are so ugly that when you were born, the doctor slapped your mother.",
            ", Ready to fail like your dad’s condom?",
            ", If I wanted to commit suicide I’d climb to your chromosome numbers and jump to your IQ.",
            ", Your birth certificate is an apology letter from the condom factory.",
            ", If laughter is the best medicine, your face must be curing the world.",
            "You're so ugly, you scared the crap out of the toilet.",
            "Your family tree must be a cactus because everybody on it is a prick.",
            "No I'm not insulting you, I'm describing you.",
            "It's better to let someone think you are an Idiot than to open your mouth and prove it.",
            "If I had a face like yours, I'd sue my parents.",
            "Your birth certificate is an apology letter from the condom factory.",
            "I guess you prove that even god makes mistakes sometimes.",
            "The only way you'll ever get laid is if you crawl up a chicken's ass and wait.",
            "You're so fake, Barbie is jealous.",
            "I'm jealous of people that don't know you!",
            "My psychiatrist told me I was crazy and I said I want a second opinion. He said okay, you're ugly too.",
            "You're so ugly, when your mom dropped you off at school she got a fine for littering.",
            "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
            "You must have been born on a highway because that's where most accidents happen.",
            "Brains aren't everything. In your case they're nothing.",
            "I don't know what makes you so stupid, but it really works.",
            "I can explain it to you, but I can't understand it for you.",
            "Roses are red violets are blue, God made me pretty, what happened to you?",
            "Behind every fat woman there is a beautiful woman. No seriously, your in the way.",
            "Calling you an idiot would be an insult to all the stupid people.",
            "You, sir, are an oxygen thief!",
            "Some babies were dropped on their heads but you were clearly thrown at a wall.",
            "Don't like my sarcasm, well I don't like your stupid.",
            "Why don't you go play in traffic.",
            "Please shut your mouth when you're talking to me.",
            "I'd slap you, but that would be animal abuse.",
            "They say opposites attract. I hope you meet someone who is good-looking, intelligent, and cultured.",
            "Stop trying to be a smart ass, you're just an ass.",
            "The last time I saw something like you, I flushed it.",
            "I'm busy now. Can I ignore you some other time?",
            "You have Diarrhea of the mouth; constipation of the ideas.",
            "If ugly were a crime, you'd get a life sentence.",
            "Your mind is on vacation but your mouth is working overtime.",
            "I can lose weight, but you'll always be ugly.",
            "Why don't you slip into something more comfortable... like a coma.",
            "Shock me, say something intelligent.",
            "If your gonna be two faced, honey at least make one of them pretty.",
            "Keep rolling your eyes, perhaps you'll find a brain back there.",
            "You are not as bad as people say, you are much, much worse.",
            "I don't know what your problem is, but I'll bet it's hard to pronounce.",
            "You get ten times more girls than me? ten times zero is zero...",
            "There is no vaccine against stupidity.",
            "You're the reason the gene pool needs a lifeguard.",
            "Sure, I've seen people like you before - but I had to pay an admission.",
            "How old are you? - Wait I shouldn't ask, you can't count that high.",
            "Have you been shopping lately? They're selling lives, you should go get one.",
            "You're like Monday mornings, nobody likes you.",
            "Of course I talk like an idiot, how else would you understand me?",
            "All day I thought of you... I was at the zoo.",
            "To make you laugh on Saturday, I need to you joke on Wednesday.",
            "You're so fat, you could sell shade.",
            "I'd like to see things from your point of view but I can't seem to get my head that far up my ass.",
            "Don't you need a license to be that ugly?",
            "My friend thinks he is smart. He told me an onion is the only food that makes you cry, so I threw a coconut at his face.",
            "Your house is so dirty you have to wipe your feet before you go outside.",
            "If you really spoke your mind, you'd be speechless.",
            "Stupidity is not a crime so you are free to go.",
            "You are so old, when you were a kid rainbows were black and white.",
            "If I told you that I have a piece of dirt in my eye, would you move?",
            "You so dumb, you think Cheerios are doughnut seeds.",
            "So, a thought crossed your mind? Must have been a long and lonely journey.",
            "You are so old, your birth-certificate expired.",
            "Every time I'm next to you, I get a fierce desire to be alone.",
            "You're so dumb that you got hit by a parked car.",
            "Keep talking, someday you'll say something intelligent!",
            "You're so fat, you leave footprints in concrete.",
            "How did you get here? Did someone leave your cage open?",
            "Pardon me, but you've obviously mistaken me for someone who gives a damn.",
            "Wipe your mouth, there's still a tiny bit of bullshit around your lips.",
            "Don't you have a terribly empty feeling - in your skull?",
            "As an outsider, what do you think of the human race?",
            "Just because you have one doesn't mean you have to act like one.",
            "We can always tell when you are lying. Your lips move.",
            "Are you always this stupid or is today a special occasion?",
            "You Rock! Cancel that.",
            "Fuck off",
            "Your mother is a hamster and your father smells of elderberries!",
            "Roses are red, violets are blue, I’ve got five fingers and the middle one is for you ;)",
            "Brain the size of a planet, and they have me doing something as simple as insulting you.",
            "Your ass, your face, what's the difference?"]

            if target.id == 579618795342004224 :
                await ctx.send("Nice try fag , but my iq is higher than you retard")
            else:
                await ctx.send(target.mention + f'{random.choice(responses)}')


    @commands.command()
    async def clear(self, ctx, amount = 10000):
        await ctx.channel.purge(limit=amount)

    @commands.command
    async def help(self, ctx):
        embed = discord.Embed(title="Nibba for the resque", description="Some useful commands to use nibba")
        embed.add_field(name=".ping", value="checks the ping of the fag")
        embed.add_field(name=".help", value="shows the commands to the fag")
        embed.add_field(name=".Pink", value="used for answering the questions of the fag")
        await message.channel.send(content=None, embed=embed)

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send('{0.name} Faggot joined in {0.joined_at}'.format(member))

    @commands.command(aliases=["Hey Pink guy , tell me a joke"])
    async def joke(self, ctx):
        Jokes=["I was going to tell a dead baby joke. But I decided to abort.",
        "Why does Dr. Pepper come in a bottle? His wife is dead.",
        "Why does Helen Keller hate porcupines? They’re painful to look at.",
        "Why can’t orphans play baseball? They don’t know where home is.",
        "Give a man a match, and he’ll be warm for a few hours. Set a man on fire, and he will be warm for the rest of his life.",
        "I asked a pretty, young homeless woman if I could take her home. She smiled at me and said yes. The look on her face soon changed, however, when I walked off with her cardboard box.",
        " My wife and I have reached the difficult decision that we do not want children. If anybody does, please just send me your contact details and we can drop them off tomorrow.",
        "My elderly relatives liked to tease me at weddings, saying, “You’ll be next!” They soon stopped though, once I started doing the same to them at funerals.",
        "A blind woman tells her boyfriend that she’s seeing someone. It’s either really terrible news or really great news.",
        "I was digging in our garden when I found a chest full of gold coins. I was about to run straight home to tell my wife about it, but then I remembered why I was digging in our garden.",
        "Even people who are good for nothing have the capacity to bring a smile to your face. For instance, when you push them down the stairs.",
        "My grandfather says I’m too reliant on technology. I called him a hypocrite and unplugged his life support.",
        "One man’s trash is another man’s treasure. Wonderful saying, horrible way to find out you were adopted.",
        "I visited my friend at his new house. He told me to make myself at home. So I threw him out. I hate having visitors.",
        "What is the hardest part of a vegetable to eat? The wheelchair.","What did Kermit the frog say at Jim Henson’s funeral?  Nothing.",
        "The other day, my wife asked me to pass her lipstick but I accidentally passed her a glue stick. She still isn’t talking to me.",
        "I wish the grass in my back lawn was emo. Then it would cut itself.",
        "I bought my blind friend a cheese grater for his birthday. A week later, he told me it was the most violent book he’d ever read.","What’s yellow and can’t swim? A bus full of children.","What is black and sticks to a tree? A peeping tom after a forest fire.","Today was a terrible day. My ex got hit by a bus. And I lost my job as a bus driver!","Where does a girl with one leg work? IHOP.","What’s the last thing to go through a fly’s head as it hits the windshield of a car going 70 mph? It’s butt."]

        await ctx.send(f"{random.choice(Jokes)}")

    @commands.command()
    async def translate(self, ctx , *, query: str):
        await ctx.send(yandex_translate.translate( query , 'en')['text'][0])

    @commands.command(aliases=['pink'])
    async def boss(self, ctx, query: str):
        if query=='Hi':
            await ctx.send('Konnichiwa magnificient bastard')
        if query=='konnichiwa':
            await ctx.send('Konnichiwa magnificient bastard')
        if query=='Who developed you?':
            await ctx.send('Chr0m0s0m3s')
        elif query=='Who made you?':
            await ctx.send("Chr0m0s0mes")
        elif query=='Who developed you':
            await ctx.send('Chr0m0s0m3s')
        elif query=='Who made you':
            await ctx.send('Chr0m0s0m3s')
        elif query=='Who created you?':
            await ctx.send('Chr0m0s0m3s')
        elif query=="Who created you":
            await ctx.send("Chr0m0s0m3s")
        elif query=="Who is your creator?":
            await ctx.send("Chr0m0s0m3s")
        elif query=="Who is your creator":
            await ctx.send("Chr0m0s0m3s")
        elif query=='Who made you?':
            await ctx.send("Chr0m0s0mes")
        elif query=='who developed you':
            await ctx.send('Chr0m0s0m3s')
        elif query=='who made you?':
            await ctx.send('Chr0m0s0m3s')
        elif query=='who created you?':
            await ctx.send('Chr0m0s0m3s')
        elif query=="who created you":
            await ctx.send("Chr0m0s0m3s")
        elif query=="who is your creator?":
            await ctx.send("Chr0m0s0m3s")
        elif query=="who is your creator":
            await ctx.send("Chr0m0s0m3s")
        elif query=='Cake hair recipe':
            await ctx.send("After all of the ingredients are gathered, Chefs Frank, Max and Ian get to work in preparing their cake, with HowToBasic and Mr. Pirate Man assisting. While preparing their cake, the Protégé drinks and vomits all of the milk used, similar to his mixing technique used in the first Cake video. They then add all of the ingredients they had harassed Youtubers for: piss from JoeySalads, chewed banana from Jontron, pubic hair from Jacksepticeye and KSI, toenail clippings from makemebad35 and Anthony Fantano, and ass hair from PewDiePie. They then went to Vsauce (who was sleeping outside with a bag of garbage), who gave interesting spit facts while they collected saliva from him. Then the cake was done.")

        else:
            try:
                aiml_response = aiml_kernel.respond(query)
                await ctx.send(aiml_response)
            except:
                await ctx.send(inference(f'{query}')['answers'][0])

    @commands.command(aliases=["jp101"])
    async def japanese101(self, ctx):
        jpnese101=["Aho - Idiot",
                    "Aitsu! - That creep!",
                    "AV dan u natte mitai - I want to be a porn star",
                    "Baita - Whore",
                    "Baka - Idiot / Stupid",
                    "Baka ka - Stupid asshole",
                    "Baka ne - You fool",
                    "Bakabakashii - Idiotic",
                    "Baka yarou - Stupid asshole / fool / idiot",
                    "Busu - Ugly",
                    "Chinchin - Dick / Child's way of saying 'penis'",
                    "Chinpo - Penis",
                    "Damare - Shut up",
                    "Ecchi - Sex / Softcore eroticism",
                    "Hentai - Sexually perverted",
                    "Hitori ecchi - Single person ecchi (masturbation)",
                    "Jein wa futotte rushi, taido mo warui shi, tabako mopukapuka suu shi - Jane is fat, rude, and smokes too much",
                    "Kondo-san - Mr. Condom",
                    "Kuso - Darn / Shit",
                    "Kusokurae - Fuck you",
                    "Kutabare - Fuck you",
                    "Nanda - What the hell?",
                    "Nanda yo omae-wa? - Who the hell do you think you are?",
                    "Naraku - Hell",
                    "Nuri kabe - Plaster face",
                    "Omae o korosu - I will kill you",
                    "Omae wa dare da? - Who the hell are you?",
                    "Onara atama - Fart head",
                    "Putaro - Tramp",
                    "Sekai de ichiban daikirai - I hate you most in the world",
                    "Shine - Die",
                    "Sukebe - Pervert",
                    "Teme - You (very rude)",
                    "Tottoto dete ike - Get the hell out of here",
                    "Unko - Shit / Poop",
                    "Unko no nioi kagu hito - Poop sniffer",
                    "Urusai - Shut up",
                    "Kokujin - Nigger",
                    "Ketsu o taberu - I eat ass",
                    "この やろう"
                    "kono yarou- You shit",

                    "もんく あっか？"
                    "Monku akka?- Do you have a problem?/what’s your problem?",

                    "ばか じゃない の？"
                    "Baka ja nai no?- are you stupid?/you’re not stupid, are you?"
                    "Note: baka ja nai means “not stupid”, but adding “no” at the end makes it an informal question. You should say the “no” with a rising intonation.",

                    "なに して の あほ？"
                    "Nani shite no aho?- what are you doing idiot?",

                    "なに はなして の あほ？"
                    "Nani hanashite no aho?- what are you talking about idiot?",

                    "しね めすぶた ども！"
                    "shine mesubuta domo！- Die you whore/slut!"
                    "Note: this literally means “Die you female pig!”",

                    "Busaiku- ugly (person,clothes,place etc.)",
                    "Kimochi warui- bad feeling",
                    "Debu- fatty",
                    "Chikushou- damn it",
                    "Kuso- shit",
                    "kusottare- shit drip",
                    "Jigoku e ike!- Go to hell!",
                    "Kangaete mite! – Think about it! ",
                    "Kisama- you bastard/ motherfucker",
                    "Damare- shut up/shut the fuck up",
                    "Kyapi Kyapi Gyaru- Bimbo/ japanese valley girl",
                    "Koshinuke- Coward",
                    "kutabare- Drop dead!",
                    "Ijiwaru- Malicious, spiteful, bitchy",
                    "Sono onna wa ijiwaru.- That woman is bitchy.",
                    "iyarashii- disgusting, lewd, indecent",
                    "Your disgusting!",
                    "yowamushi- Wimp, coward",
                    "toroi- Slow to catch on, doesn’t “get it”",
                    "Anata wa toroi desu ne?- You’re slow to catch on, aren’t you?",
                    "kono yarou- You shit"]

        embed = discord.Embed(description=random.choice(jpnese101) , color=randint(0, 0xFFFFFF), title="Japanese")
        embed.set_author(name="Japanese 101")
        embed.set_thumbnail(url="https://i.ytimg.com/vi/7-IkUdg9YWM/maxresdefault.jpg")
        await ctx.send(embed=embed)


    @commands.command()
    async def meme(self, ctx):
        rnd = random.randint(0,5)
        memes = reddit.subreddit('memes').new(limit=7)
        post = [p for p in memes if not p.stickied][rnd]
        embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title="Memes")
        embed.set_author(name="Memes for cunts",icon_url="https://vignette.wikia.nocookie.net/filthy-frank/images/9/98/Salamander_Man2.png")
        embed.set_image(url=str(post.url))
        await ctx.send(embed=embed)

    @commands.command()
    async def porn(self, ctx):
            rnd = random.randint(0,5)
            memes = reddit.subreddit('porn').new(limit=7)
            post = [p for p in memes if not p.stickied][rnd]
            await ctx.send(post.url)

    @commands.command()
    async def show(self, ctx , query: str):
            rnd = random.randint(0,5)
            memes = reddit.subreddit(query).new(limit=7)
            post = [p for p in memes if not p.stickied][rnd]
            embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title="Random")
            embed.set_author(name="Random things for cunts",icon_url="https://vignette.wikia.nocookie.net/filthy-frank/images/9/98/Salamander_Man2.png")
            embed.set_image(url=str(post.url))
            await ctx.send(embed=embed)

    @commands.cooldown(5, 120, commands.BucketType.default)
    @commands.command()
    async def hentai(self, ctx):
        rnd = random.randint(0,5)
        hentai = reddit.subreddit('hentai').new(limit=7)
        post = [p for p in hentai if not p.stickied][rnd]
        embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title="Hentai")
        embed.set_author(name="Hentai for cunts",icon_url="https://vignette.wikia.nocookie.net/filthy-frank/images/9/98/Salamander_Man2.png")
        embed.set_image(url=str(post.url))
        await ctx.send(embed=embed)
    @hentai.error
    async def mine_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'Hold your dick, please masturbate after {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

    @commands.command()
    async def lesbo(self, ctx):
        rnd = random.randint(0,5)
        memes = reddit.subreddit('lesbo').new(limit=7)
        post = [p for p in memes if not p.stickied][rnd]
        embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title="Lesbians")
        embed.set_author(name="Lesbians for cunts",icon_url="https://vignette.wikia.nocookie.net/filthy-frank/images/9/98/Salamander_Man2.png")
        embed.set_image(url=str(post.url))
        await ctx.send(embed=embed)

    @commands.command()
    async def papafranku(self, ctx):
        rnd = random.randint(0,5)
        memes = reddit.subreddit('FilthyFrank').new(limit=7)
        post = [p for p in memes if not p.stickied][rnd]
        embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title="FilthyFrank")
        embed.set_author(name="Its filthyfrank motherfucker",icon_url="https://vignette.wikia.nocookie.net/filthy-frank/images/9/98/Salamander_Man2.png")
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
