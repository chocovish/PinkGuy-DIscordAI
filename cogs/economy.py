import asyncio
from collections import Counter
from random import choice, randint
import json
from recordclass import recordclass
import time
import discord
from async_timeout import timeout
from discord.ext import commands
from cogs.utils.dataIO import fileIO
from cogs.utils import checks
from cogs.utils.data import MemberConverter, NumberConverter, get, chain, create_pages, IntConverter
from cogs.utils.translation import _

client = commands.Bot(command_prefix = 'ey ')

slot_payouts = """Slot machine payouts:
    :two: :two: :six: Bet * 5000
    :four_leaf_clover: :four_leaf_clover: :four_leaf_clover: +1000
    :cherries: :cherries: :cherries: +800
    :two: :six: Bet * 4
    :cherries: :cherries: Bet * 3
    Three symbols: +500
    Two symbols: Bet * 2"""

class Economy(commands.Cog):
    """Economy related commands: balance, market, etc"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/economy/settings.json", "load")
        self.payday_register = {}
        self.slot_register = {}
        self.bids = list()

    async def shutdown(self):
        with open("resources/lotteries.json", 'w') as lf:
            lf.write(json.dumps(self.bot.lotteries))

    def cog_check(self, ctx):
        def predicate(ctx):
            if ctx.guild is None:
                raise commands.NoPrivateMessage()
            return True

        return commands.check(predicate(ctx))

    @commands.command(aliases=["bal", "balance", "eco", "e"], invoke_without_command=True)
    async def chromosomes(self, ctx, *, member: discord.Member = None):
        """Check your or another users chromosomes.
        Example: ey chromosomes @faggot#6969
        Will not display others' balances if inventory hiding is enabled."""
        dest = ctx.channel
        if member is None:
            member = ctx.author
        gd = await self.bot.db.get_guild_data(ctx.guild)
        try:
            is_mod = checks.role_or_permissions(ctx,
                                                lambda r: r.name in ('Bot Mod', 'Bot Admin', 'Bot Moderator'),
                                                manage_server=True)
        except:
            is_mod = False

        hide = gd.get("hideinv", False)

        if not is_mod and hide:
            member = ctx.author

        if hide:
            dest = ctx.author

        bal = await ctx.bot.di.get_all_balances(member)

        data = """
You have:\t\t {} chromosomes
In the ricefields:\t {} chromosomes
Total:\t\t {} chromosomes
        """

        embed = discord.Embed(
            description=(await _(ctx, data)).format(int(bal[0]) if int(bal[0]) == bal[0] else bal[0],
                                                    int(bal[1]) if int(bal[1]) == bal[1] else bal[1],
                                                    sum(bal)
                                                    ),
            color=randint(0, 0xFFFFFF),
        )

        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        embed.set_thumbnail(url="https://www.biobm.com/images/chromosome-abstract.png")
        await dest.send(embed=embed)

    @commands.command()
    async def donate(self, ctx, amount: NumberConverter, member: discord.Member):
        """Donate chromosomes to other users
        Example: ey donate 69 @faggot#6969"""
        amount = abs(amount)
        async with self.bot.di.rm.lock(ctx.author.id):
            await self.bot.di.add_eco(ctx.author, -amount)
        async with self.bot.di.rm.lock(member.id):
            await self.bot.di.add_eco(member, amount)
        await ctx.send((await _(ctx, "Successfully paid {} chromosomes to {}")).format(amount, member))

    @commands.command(aliases=["m", "pm"], invoke_without_command=True)
    async def market(self, ctx):
        """View the current market listings"""
        um = await self.bot.di.get_guild_market(ctx.guild)
        market = list(um.values())
        desc = await _(ctx,
                       "\u27A1 to see the next page"
                       "\n\u2B05 to go back"
                       "\n\u274C to exit"
                       )
        if not market:
            await ctx.send(await _(ctx, "No items on the market to display."))
            return

        emotes = ("\u2B05", "\u27A1", "\u274C")
        embed = discord.Embed(description=desc, title=await _(ctx, "Player Market"), color=randint(0, 0xFFFFFF), )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)

        chunks = []
        clen = 10
        for i in range(0, len(market), clen):
            chunks.append(market[i:i + clen])

        i = 0
        try:
            users = get(ctx.guild.members, id=[x['user'] for x in chunks[i]])
        except Exception:
            br = []
            fr = dict()
            for listing, data in um.items():
                for datum in data:
                    if 'item' not in listing:
                        id = self.bot.randsample()
                        fr[id] = dict(id=id, item=listing, user=ctx.author.id, cost=datum['cost'],
                                      amount=datum['amount'])
                br.append(listing)

            for i in br:
                del um[i]
            um.update(fr)

            await self.bot.di.update_guild_market(ctx.guild, um)
            market = list(um.items())
            chunks = []
            for i in range(0, len(market), clen):
                chunks.append(market[i:i + clen])

            users = get(ctx.guild.members, id=[x['user'] for x in chunks[i]])

        currency = await ctx.bot.di.get_currency(ctx.guild)

        fin = [[x['id'], f"{x['cost']} {currency}", f"x{x['amount']}", x['item'], str(y)] for x, y in
               zip(chunks[i], users)]
        fin.insert(0, [await _(ctx, "ID"),
                       await _(ctx, "COST"),
                       await _(ctx, "NUMBER"),
                       await _(ctx, "ITEM"),
                       await _(ctx, "SELLER")])
        embed.description = "```\n{}\n```".format(self.bot.format_table(fin))

        max = len(chunks) - 1

        msg = await ctx.send(embed=embed)
        for emote in emotes:
            await msg.add_reaction(emote)

        while True:
            try:
                r, u = await self.bot.wait_for("reaction_add", check=lambda r, u: r.message.id == msg.id, timeout=80)
            except asyncio.TimeoutError:
                await ctx.send(await _(ctx, "Timed out! Try to be punctual faggot"))
                await msg.delete()
                return

            if u == ctx.guild.me:
                continue

            if u != ctx.author or r.emoji not in emotes:
                try:
                    await msg.remove_reaction(r.emoji, u)
                except:
                    pass
                continue

            if r.emoji == emotes[0]:
                if i == 0:
                    pass
                else:
                    i -= 1
                    users = get(ctx.guild.members, id=[x["user"] for x in chunks[i]])
                    fin = [[x['id'], f"{x['cost']} chromosomes", f"x{x['amount']}", x['item'], str(y)] for x, y in
                           zip(chunks[i], users)]
                    fin.insert(0, [await _(ctx, "ID"),
                                   await _(ctx, "COST"),
                                   await _(ctx, "NUMBER"),
                                   await _(ctx, "ITEM"),
                                   await _(ctx, "SELLER")])
                    embed.description = "```\n{}\n```".format(self.bot.format_table(fin))

                    await msg.edit(embed=embed)

            elif r.emoji == emotes[1]:
                if i == max:
                    pass
                else:
                    embed.clear_fields()
                    i += 1
                    users = get(ctx.guild.members, id=[x["user"] for x in chunks[i]])
                    fin = [[x['id'], f"{x['cost']} chromosomes", f"x{x['amount']}", x['item'], str(y)] for x, y in
                           zip(chunks[i], users)]
                    fin.insert(0, [await _(ctx, "ID"),
                                   await _(ctx, "COST"),
                                   await _(ctx, "NUMBER"),
                                   await _(ctx, "ITEM"),
                                   await _(ctx, "SELLER")])
                    embed.description = "```\n{}\n```".format(self.bot.format_table(fin))

                    await msg.edit(embed=embed)
            else:
                await msg.delete()
                await ctx.send("Closing")
                return

            try:
                await msg.remove_reaction(r.emoji, u)
            except:
                pass

    @commands.command(aliases=["createlisting","listitem", "list"])
    async def auction(self, ctx, cost: NumberConverter, amount: IntConverter, *, item: str):

        amount = abs(amount)
        cost = abs(cost)
        market = await self.bot.di.get_guild_market(ctx.guild)

        async with self.bot.di.rm.lock(ctx.author.id):
            try:
                await self.bot.di.take_items(ctx.author, (item, amount))
            except ValueError:
                await ctx.send(await _(ctx, "You don't have enough of these to sell!"))
                return

        id = self.bot.randsample()
        market[id] = dict(id=id, item=item, user=ctx.author.id, cost=cost, amount=amount)

        async with self.bot.di.rm.lock(ctx.guild.id):
            await self.bot.di.update_guild_market(ctx.guild, market)

        await ctx.send((await _(ctx, "Item listed with ID {}")).format(id))

    @commands.command(aliases=["purchase", "acheter"])
    async def buy(self, ctx, id: str):

        async with self.bot.di.rm.lock(ctx.guild.id):
            market = await self.bot.di.get_guild_market(ctx.guild)
            item = market.pop(id)

            if not item:
                await ctx.send(await _(ctx, "That is not a valid ID!"))
                return

            try:
                await self.bot.di.add_eco(ctx.author, -item['cost'])
            except ValueError:
                await ctx.send(await _(ctx, "Ey boss , you poor man"))
                return

            owner = discord.utils.get(ctx.guild.members, id=item["user"])
            if owner is None:
                owner = discord.Object(item["user"])
                owner.guild = ctx.guild

            async with self.bot.di.rm.lock(owner.id):
                await self.bot.di.add_eco(owner, item['cost'])

            async with self.bot.di.rm.lock(ctx.author.id):
                await self.bot.di.give_items(ctx.author, (item["item"], item["amount"]))

            await self.bot.di.update_guild_market(ctx.guild, market)
        await ctx.send(await _(ctx, "Items successfully bought"))
        if not isinstance(owner, discord.Object):
            await owner.send((await _(ctx,
                                      "{} bought {} {} from you for {} chromosomes with ID {} on server {}")).format(
                ctx.author, item["item"], item["amount"], item['cost'], id, ctx.guild.name))

    @commands.command()
    async def search(self, ctx, *, item: str):

        um = await self.bot.di.get_guild_market(ctx.guild)
        market = [i for i in um.values() if i['item'] == item]
        desc = await _(ctx, """
        \u27A1 to see the next page
        \u2B05 to go back
        \u274C to exit
        """)
        if not market:
            await ctx.send("No items on the market to display.")
            return

        emotes = ("\u2B05", "\u27A1", "\u274C")
        embed = discord.Embed(description=desc, title=await _(ctx, "Player Market"), color=randint(0, 0xFFFFFF), )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)

        chunks = []
        for i in range(0, len(market), 25):
            chunks.append(market[i:i + 25])

        i = 0
        try:
            users = get(ctx.guild.members, id=[x['user'] for x in chunks[i]])
        except Exception:
            br = []
            fr = dict()
            for listing, data in um.items():
                for datum in data:
                    if 'item' not in listing:
                        id = self.bot.randsample()
                        fr[id] = dict(id=id, item=listing, user=ctx.author.id, cost=datum['cost'],
                                      amount=datum['amount'])
                br.append(listing)

            for i in br:
                del um[i]
            um.update(fr)

            await self.bot.di.update_guild_market(ctx.guild, um)
            market = list(um.items())
            chunks = []
            for i in range(0, len(market), 25):
                chunks.append(market[i:i + 25])

            users = get(ctx.guild.members, id=[x['user'] for x in chunks[i]])

        # items = [f"{x['id']}\t| {x['cost']} dollars\t| x{x['amount']}\t| {x['item']}\t| {y.mention}" for x, y in zip(chunks[i], users)]
        # items.insert(0, "ID\t\t| COST\t\t| NUMBER\t\t| ITEM\t\t| SELLER")
        fin = [[x['id'], f"{x['cost']} chromosomes", f"x{x['amount']}", x['item'], str(y)] for x, y in
               zip(chunks[i], users)]
        fin.insert(0, [await _(ctx, "ID"),
                       await _(ctx, "COST"),
                       await _(ctx, "NUMBER"),
                       await _(ctx, "ITEM"),
                       await _(ctx, "SELLER")])
        embed.description = "```\n{}\n```".format(self.bot.format_table(fin))

        max = len(chunks) - 1

        msg = await ctx.send(embed=embed)
        for emote in emotes:
            await msg.add_reaction(emote)

        while True:
            try:
                r, u = await self.bot.wait_for("reaction_add", check=lambda r, u: r.message.id == msg.id, timeout=80)
            except asyncio.TimeoutError:
                await ctx.send(await _(ctx, "Timed out! Try again"))
                await msg.delete()
                return

            if u == ctx.guild.me:
                continue

            if u != ctx.author or r.emoji not in emotes:
                try:
                    await msg.remove_reaction(r.emoji, u)
                except:
                    pass
                continue

            if r.emoji == emotes[0]:
                if i == 0:
                    pass
                else:
                    i -= 1
                    users = get(ctx.guild.members, id=[x["user"] for x in chunks[i]])
                    fin = [[x['id'], f"{x['cost']} chromosomes", f"x{x['amount']}", x['item'], str(y)] for x, y in
                           zip(chunks[i], users)]
                    fin.insert(0, [await _(ctx, "ID"),
                                   await _(ctx, "COST"),
                                   await _(ctx, "NUMBER"),
                                   await _(ctx, "ITEM"),
                                   await _(ctx, "SELLER")])
                    embed.description = "```\n{}\n```".format(self.bot.format_table(fin))

                    await msg.edit(embed=embed)

            elif r.emoji == emotes[1]:
                if i == max:
                    pass
                else:
                    embed.clear_fields()
                    i += 1
                    users = get(ctx.guild.members, id=[x["user"] for x in chunks[i]])
                    fin = [[x['id'], f"{x['cost']} chromosomes", f"x{x['amount']}", x['item'], str(y)] for x, y in
                           zip(chunks[i], users)]
                    fin.insert(0, [await _(ctx, "ID"),
                                   await _(ctx, "COST"),
                                   await _(ctx, "NUMBER"),
                                   await _(ctx, "ITEM"),
                                   await _(ctx, "SELLER")])
                    embed.description = "```\n{}\n```".format(self.bot.format_table(fin))

                    await msg.edit(embed=embed)
            else:
                await msg.delete()
                await ctx.send("Closing")
                return

            try:
                await msg.remove_reaction(r.emoji, u)
            except:
                pass

    @commands.command(aliases=["rm"], name="remove")
    async def _market_remove(self, ctx, id: str):

        async with self.bot.di.rm.lock(ctx.guild.id):
            market = await self.bot.di.get_guild_market(ctx.guild)
            try:
                item = market.pop(id)
            except KeyError:
                await ctx.send( "That is not a valid ID faggot!")
                return

            if item["user"] == ctx.author.id:
                await self.bot.di.give_items(ctx.author, (item["item"], item["amount"]))
                await self.bot.di.update_guild_market(ctx.guild, market)
            else:
                await ctx.send("This is not your item to remove!")


    @commands.command()
    async def leaderboard(self, ctx):

        req = f"""SELECT ("UUID", info->'{ctx.guild.id}'->>'chromosomes') FROM market.userdata;"""
        async with self.bot.db._conn.acquire() as connection:
            resp = await connection.fetch(req)

        users = [(discord.utils.get(ctx.guild.members, id=int(x["row"][0])), x["row"][1]) for x in resp if
                 (len(x["row"]) == 2) and (x["row"][1] is not None)]
        users = [x for x in users if x[0]]
        users.sort(key=lambda x: -float(x[1]))

        currency = await ctx.bot.di.get_currency(ctx.guild)
        msg = "\n".join(f"{x}: {y[0]} {y[1]} {currency}" for x, y in zip(range(1, 11), users))
        await ctx.send(f"```\n{msg}\n```")

    @commands.command(aliases=["bank"], invoke_without_command=True)
    async def register(self, ctx):
        bal = (await self.bot.di.get_all_balances(ctx.author))[1]

        await ctx.send( "Welcome to the ricefields motherfucker, You have {} chromosomes".format(int(bal) if int(bal) == bal else bal))

    @commands.command()
    async def deposite(self, ctx, amount: float):

        async with self.bot.di.rm.lock(ctx.author.id):
            bal = (await self.bot.di.get_all_balances(ctx.author))
            if amount > bal[0]:
                await ctx.send(await _(ctx, "You don't have enough chromosomes to deposit!"))
                return
            await ctx.bot.di.set_balances(ctx.author, bal[0] - amount, bal[1] + amount)

            await ctx.send("Successfully transferred {} chromosomes to your ricefields. You have {} chromosomes total in the ricefields".format(amount,bal[1] + amount))

    @commands.command()
    async def withdraw(self, ctx, amount: float):


        async with self.bot.di.rm.lock(ctx.author.id):
            bal = (await self.bot.di.get_all_balances(ctx.author))
            if amount > bal[1]:
                await ctx.send(await _(ctx, "You don't have enough chromosomes to withdraw!"))
                return
            await ctx.bot.di.set_balances(ctx.author, bal[0] + amount, bal[1] - amount)

            await ctx.send("Successfully transferred {} chromosomes from your ricefields. You have {} chromosomes total in the ricefields".format(amount, bal[1] - amount))

    @commands.command(pass_context=True, no_pm=True)
    async def reward(self, ctx):
        """Get some free credits"""
        author = ctx.author
        id = author.id
        amount = int(self.settings["PAYDAY_CREDITS"])
        if id in self.payday_register:
            seconds = abs(self.payday_register[id] - int(time.perf_counter()))
            if seconds  >= self.settings["PAYDAY_TIME"]:
                async with self.bot.di.rm.lock(id):
                    await self.bot.di.add_eco(author , amount)
                self.payday_register[id] = int(time.perf_counter())
                await ctx.send("{} ey b0ss, take some chromosomes. Enjoy! (+{} chromosomes!)".format(author.mention, str(self.settings["PAYDAY_CREDITS"])))
            else:
                await ctx.send("{} ey b0ss, you had enough men {}.".format(author.mention, self.display_time(self.settings["PAYDAY_TIME"] - seconds)))
        else:
            self.payday_register[id] = int(time.perf_counter())
            async with self.bot.di.rm.lock(id):
                await self.bot.di.add_eco(author , amount)
            await ctx.send("{} ey b0ss, take some chromosomes. Enjoy! (+{} chromosomes!)".format(author.mention, str(self.settings["PAYDAY_CREDITS"])))

    @commands.command(pass_context=True)
    async def payouts(self, ctx):
        """Shows chromosome machine payouts"""
        await ctx.send(slot_payouts)

    @commands.command(pass_context=True, no_pm=True)
    async def sacrifice(self, ctx, bid : int):
        """Play the sacrifice"""
        author = ctx.message.author
        async with self.bot.di.rm.lock(ctx.author.id):
            bal = (await self.bot.di.get_all_balances(ctx.author))
            if bid > bal[0]:
                await ctx.send(await _(ctx, "ey b0ss, you p00r man"))
            if bid >= self.settings["SLOT_MIN"] and bid <= self.settings["SLOT_MAX"]:
                if author.id in self.slot_register:
                    if abs(self.slot_register[author.id] - int(time.perf_counter()))  >= self.settings["SLOT_TIME"]:
                        self.slot_register[author.id] = int(time.perf_counter())
                        await self.slot_machine(ctx.message, bid)
                    else:
                        await ctx.send("chromosome machine is still cooling off! Wait {} seconds between each sacrifice".format(self.settings["SLOT_TIME"]))
                else:
                    self.slot_register[author.id] = int(time.perf_counter())
                    await self.slot_machine(ctx.message, bid)
            else:
                await ctx.send("{0} ey b0ss, sacrifice must be made between {1} and {2} chromosomes.".format(author.mention, self.settings["SLOT_MIN"], self.settings["SLOT_MAX"]))

    async def slot_machine(self, message, bid):
        reel_pattern = [":cherries:", ":cookie:", ":two:", ":four_leaf_clover:", ":cyclone:", ":sunflower:", ":six:", ":mushroom:", ":heart:", ":snowflake:"]
        padding_before = [":mushroom:", ":heart:", ":snowflake:"] # padding prevents index errors
        padding_after = [":cherries:", ":cookie:", ":two:"]
        reel = padding_before + reel_pattern + padding_after
        reels = []
        for i in range(0, 3):
            n = randint(3,12)
            reels.append([reel[n - 1], reel[n], reel[n + 1]])
        line = [reels[0][1], reels[1][1], reels[2][1]]

        display_reels = "  " + reels[0][0] + " " + reels[1][0] + " " + reels[2][0] + "\n"
        display_reels += ">" + reels[0][1] + " " + reels[1][1] + " " + reels[2][1] + "\n"
        display_reels += "  " + reels[0][2] + " " + reels[1][2] + " " + reels[2][2] + "\n"

        if line[0] == ":two:" and line[1] == ":two:" and line[2] == ":six:":
            bid = bid * 5000
            await message.channel.send( "{}{} 226! Your bet is multiplied * 5000! {}! ".format(display_reels, message.author.mention, str(bid)))
        elif line[0] == ":four_leaf_clover:" and line[1] == ":four_leaf_clover:" and line[2] == ":four_leaf_clover:":
            bid += 1000
            await message.channel.send("{}{} Three FLC! +1000! ".format(display_reels, message.author.mention))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" and line[2] == ":cherries:":
            bid += 800
            await message.channel.send("{}{} Three cherries! +800! ".format(display_reels, message.author.mention))
        elif line[0] == line[1] == line[2]:
            bid += 500
            await message.channel.send("{}{} Three symbols! +500! ".format(display_reels, message.author.mention))
        elif line[0] == ":two:" and line[1] == ":six:" or line[1] == ":two:" and line[2] == ":six:":
            bid = bid * 4
            await message.channel.send("{}{} 26! Your bet is multiplied * 4! {}! ".format(display_reels, message.author.mention, str(bid)))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" or line[1] == ":cherries:" and line[2] == ":cherries:":
            bid = bid * 3
            await message.channel.send( "{}{} Two cherries! Your bet is multiplied * 3! {}! ".format(display_reels, message.author.mention, str(bid)))
        elif line[0] == line[1] or line[1] == line[2]:
            bid = bid * 2
            await message.channel.send("{}{} Two symbols! Your bet is multiplied * 2! {}! ".format(display_reels, message.author.mention, str(bid)))
        else:
            await message.channel.send("{}{} ey b0ss, you lost men. ".format(display_reels, message.author.mention))

            async with self.bot.di.rm.lock(message.author.id):
                await self.bot.di.add_eco(message.author , -bid)
                await message.channel.send("chromosomes left: {}".format(str(await self.bot.di.get_all_balances(ctx.author))))
            return True

        async with self.bot.di.rm.lock(message.author.id):
            await self.bot.di.add_eco(message.author, bid)
            await message.channel.send("Current chromosomes: {}".format(str(await self.bot.di.get_all_balances(ctx.author))))

    def display_time(self, seconds, granularity=2):
        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),    # 60 * 60 * 24
            ('hours', 3600),    # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
            )

        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

def check_folders():
    if not os.path.exists("data/economy"):
        print("Creating data/economy folder...")
        os.makedirs("data/economy")

def check_files():
    settings = {"PAYDAY_TIME" : 300, "PAYDAY_CREDITS" : 69, "SLOT_MIN" : 5, "SLOT_MAX" : 100, "SLOT_TIME" : 300}

    f = "data/economy/settings.json"
    if not fileIO(f, "check"):
        print("Creating default economy's settings.json...")
        fileIO(f, "save", settings)
    else: #consistency check
        current = fileIO(f, "load")
        if current.keys() != settings.keys():
            for key in settings.keys():
                if key not in current.keys():
                    current[key] = settings[key]
                    print("Adding " + str(key) + " field to economy settings.json")
            fileIO(f, "save", current)


def setup(client):
    client.add_cog(Economy(client))
