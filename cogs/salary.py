import datetime
import time
import asyncio
import json
from collections import defaultdict

import discord
from discord.ext import commands
from random import randint

from cogs.utils.data import NumberConverter
from cogs.utils import data, checks
from cogs.utils.translation import _

client = commands.Bot(command_prefix = 'ey ')


class Salary(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.first = True

    # async def on_ready(self):
    # self.bot.loop.create_task(self.run_salaries())

    async def run_salaries(self):
        if self.first:
            self.first = False
            _today = datetime.datetime(*datetime.datetime.utcnow().timetuple()[:3])
            time_until = (_today + datetime.timedelta(days=1)).timestamp() - datetime.datetime.utcnow().timestamp()
            await asyncio.sleep(time_until)
            while True:
                try:
                    dels = defaultdict(list)

                    req = f"""SELECT UUID, info ->> 'salaries' FROM guilddata;"""
                    async with self.bot.db._conn.acquire() as connection:
                        response = await connection.fetch(req)
                    guilds = (y for y in ((x["uuid"], json.loads(x["?column?"])) for x in response if x["?column?"]) if
                              y[1])

                    for guild, roles in guilds:
                        try:
                            gob = self.bot.get_guild(guild)
                            if gob:
                                for role, amount in roles.items():
                                    rob = discord.utils.get(gob.roles, id=int(role))
                                    if rob:
                                        for member in rob.members:
                                            if isinstance(amount, (int, float)):
                                                try:
                                                    await self.bot.di.add_eco(member, amount)
                                                except ValueError:
                                                    await self.bot.di.set_eco(member, 0)
                                            else:
                                                payamount, giveamount = sum(
                                                    filter(lambda x: isinstance(x, (int, float)), amount)), tuple(
                                                    filter(
                                                        lambda x: isinstance(x, (list, tuple)), amount))
                                                if payamount:
                                                    try:
                                                        await self.bot.di.add_eco(member, payamount)
                                                    except ValueError:
                                                        await self.bot.di.set_eco(member, 0)
                                                if giveamount:
                                                    await self.bot.di.update_items(member, *giveamount)
                                    else:
                                        dels[gob].append((roles, role))
                        except:
                            pass
                    try:
                        for g, rs in dels.items():
                            for allroles, r in rs:
                                del allroles[r]
                            await self.bot.di.update_salaries(g, allroles)
                    except:
                        pass
                except:
                    pass
                finally:
                    await asyncio.sleep(86400)

    def cog_check(self, ctx):
        def predicate(ctx):
            if ctx.guild is None:
                raise commands.NoPrivateMessage()
            return True

        return commands.check(predicate(ctx))

    @commands.command()
    async def salaries(self, ctx):

        currency = await ctx.bot.di.get_currency(ctx.guild)
        sals = await self.bot.di.get_salaries(ctx.guild)
        if not sals:
            await ctx.send(await _(ctx, "There are no current salaries on this server"))
        else:
            dels = []
            cdata = {}
            for role, amount in sals.items():
                roleobj = discord.utils.get(ctx.guild.roles, id=int(role))
                if roleobj is None:
                    dels.append(role)
                    continue
                interval = 60 * 60 * 24
                if isinstance(amount, dict):
                    interval = amount['int']
                    amount = amount['val']
                cdata[f"{roleobj.name} - {interval}s"] = "\n".join(
                    ("{} {}".format(item, currency)
                     if isinstance(item, (int, float)) else "{}x{}".format(*item)) for item in amount)
            for d in dels:
                del sals[d]
            if dels:
                await self.bot.di.update_salaries(ctx.guild, sals)

            await data.create_pages(ctx, cdata.items(), lambda x: x, author=await _(ctx, "Guild Salaries"),
                                    author_url=ctx.guild.icon_url)

    @commands.command(invoke_without_command=True, aliases=["sal"])
    async def salary(self, ctx, role: discord.Role):

        salary = (await self.bot.di.get_salaries(ctx.guild)).get(str(role.id), None)
        if salary is None:
            await ctx.send(await _(ctx, "That role does not have a salary!"))
        else:
            await ctx.send((await _(ctx, "{} has a daily salary of {}")).format(role, salary))

    @commands.command()
    @checks.mod_or_permissions()
    async def pay(self, ctx, role: discord.Role, interval: NumberConverter, *items_or_number: data.ItemOrNumber):
        """Create a daily salary for a user with the given role.
         The time interval is the interval which must pass before the user may collect the salary again, in seconds.
         If a role with a salary is deleted, the salary will also be deleted.
         For example
         `ey pay @faggot Creator 3600 69` Will create a salary of 69 chromosomes for a user hourly
        """
        if not items_or_number:
            await ctx.send(await _(ctx, "Missing argument, see ey help"))
            return

        sals = await self.bot.di.get_salaries(ctx.guild)
        if len(items_or_number) == 1 and isinstance(items_or_number[0], int):
            items_or_number = items_or_number[0]

        sals[role.id] = {'int': interval, 'val': items_or_number}
        await self.bot.di.update_salaries(ctx.guild, sals)
        await ctx.send((await _(ctx, "Successfully created a daily salary of {} for {}")).format(items_or_number, role))

    @commands.command()
    @checks.mod_or_permissions()
    async def fire(self, ctx, *, role: discord.Role):

        sals = await self.bot.di.get_salaries(ctx.guild)
        if str(role.id) in sals:
            del sals[str(role.id)]
            await self.bot.di.update_salaries(ctx.guild, sals)
            await ctx.send((await _(ctx, "Successfully deleted the daily salary for {}")).format(role))
        else:
            await ctx.send(await _(ctx, "That role has no salaries!"))

    @commands.command()
    @checks.mod_or_permissions()
    async def payout(self, ctx, role: discord.Role = None):

        dels = []
        roles = await self.bot.di.get_salaries(ctx.guild)
        try:
            if role is not None:
                roles = {role.id: roles[str(role.id)]}
        except KeyError:
            await ctx.send(await _(ctx, "That role doesn't have a salary!"))
        for role, amount in roles.items():
            rob = discord.utils.get(ctx.guild.roles, id=int(role))
            if rob:
                for member in rob.members:
                    if isinstance(amount, (int, float)):
                        try:
                            await self.bot.di.add_eco(member, amount)
                        except ValueError:
                            await self.bot.di.set_eco(member, 0)
                    else:
                        if isinstance(amount, dict):
                            amount = amount["val"]

                        payamount, giveamount = sum(
                            filter(lambda x: isinstance(x, (int, float)), amount)), tuple(filter(
                            lambda x: isinstance(x, (list, tuple)), amount))
                        if payamount:
                            try:
                                await self.bot.di.add_eco(member, payamount)
                            except ValueError:
                                await self.bot.di.set_eco(member, 0)
                        if giveamount:
                            await self.bot.di.update_items(member, *giveamount)
            else:
                dels.append(role)

        if dels:
            await ctx.send((await _(ctx, "Roles {} were missing")).format(dels))
            for role in dels:
                del roles[role]

            await self.bot.di.update_salaries(ctx.guild, roles)

        await ctx.send(await _(ctx, "Salaries payed out"))

    @commands.command()
    async def collect(self, ctx: commands.Context):

        salaries = await self.bot.di.get_salaries(ctx.guild)
        spayments = await self.bot.di.get_salary_ctime(ctx.author)
        ctime = time.time()

        roles = ctx.author.roles

        collected = False
        for role in roles:
            if str(role.id) in salaries:
                amount = salaries[str(role.id)]
                if isinstance(amount, dict):
                    interval, amount = amount['int'], amount['val']
                else:
                    interval = 3600 * 24
                if (ctime - spayments.get(str(role.id), 0)) > interval:
                    spayments[str(role.id)] = ctime

                    if isinstance(amount, (int, float)):
                        try:
                            await self.bot.di.add_eco(ctx.author, amount)
                        except ValueError:
                            await self.bot.di.set_eco(ctx.author, 0)
                    else:
                        payamount, giveamount = sum(
                            filter(lambda x: isinstance(x, (int, float)), amount)), tuple(filter(
                            lambda x: isinstance(x, (list, tuple)), amount))
                        if payamount:
                            try:
                                await self.bot.di.add_eco(ctx.author, payamount)
                            except ValueError:
                                await self.bot.di.set_eco(ctx.author, 0)
                        if giveamount:
                            await self.bot.di.update_items(ctx.author, *giveamount)
                    collected = True

                else:
                    delta = datetime.timedelta(seconds=interval) - (
                        datetime.timedelta(seconds=time.time() - spayments[str(role.id)]))
                    await ctx.send((await _(ctx, "{} cannot be collected for another {}")).format(role, delta))

        if collected:
            await ctx.send(await _(ctx, "Successfully collected salaries"))
            await self.bot.di.set_salary_ctime(ctx.author, spayments)
        else:
            await ctx.send(await _(ctx, "Failed to collect salaries"))

def setup(client):
    client.add_cog(Salary(client))
