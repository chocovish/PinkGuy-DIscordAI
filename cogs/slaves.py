
from discord.ext import commands
import discord
import asyncio
from random import randint

from cogs.utils import checks, data
from cogs.utils.translation import _

client = commands.Bot(command_prefix = 'ey ')


class Slaves(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        def predicate(ctx):
            if ctx.guild is None:
                raise commands.NoPrivateMessage()
            return True

        return commands.check(predicate(ctx))

    @commands.command()
    async def nigga(self, ctx, member: discord.Member = None):
        """Check the slave under you"""
        if member is None:
            member = ctx.author
        box = await self.bot.di.get_box(member)

        pet = [f"{x.id}: **{x.name}**" for x in box]
        description = "\n".join(pet)
        embed = discord.Embed(description=description, title=f"{member.display_name} Slave", color=randint(0, 0xFFFFFF))
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        embed.set_thumbnail(url="http://www.afropanavision.com/uploads/8/9/9/8/8998038/1373696561.png")

        await ctx.send(embed=embed)

    @commands.command(aliases=["p"], invoke_without_command=True)
    async def slave(self, ctx, member: discord.Member = None):
        """Subcommands for slave management, see ey help slave"""
        if member is None:
            member = ctx.author
        box = await self.bot.di.get_box(member)

        pet = [f"{x.id}: **{x.name}**" for x in box]
        description = "\n".join(pet)
        embed = discord.Embed(description=description, title=f"{member.display_name} Pet", color=randint(0, 0xFFFFFF))
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def edit(self, ctx, pet_id: int, attribute: str, *, value: str):
        """Edit a slave
                Usage: ey slave edit 5 description chin chin likes wet vagina!
                Valid values for the [item] (second argument):
                    name: the character's name
                    description: the description of the character
                    level: an integer representing the character's level
                    meta: used like the additional info section when creating; can be used to edit/remove all attributes
                Anything else will edit single attributes in the additional info section
                """
        pet = await self.bot.di.get_pet(ctx.author, pet_id)

        if len(attribute) + len(value) > 1024:
            await ctx.send(await _(ctx, "Can't have an attribute longer than 1024 characters!"))
            return

        pet = list(pet)
        if attribute == "name":
            await self.bot.di.remove_pet(ctx.guild, pet[1])
            pet.name = value
        elif attribute in pet[3]:
            pet[3][attribute] = value
        elif attribute == "meta":
            try:
                pet[4] = {}
                if "\n" in value:
                    res = value.split("\n")
                else:
                    res = value.split(",")
                for val in res:
                    key, value = val.split(": ")
                    key = key.strip()
                    value = value.strip()
                    if key != "maps":
                        pet[4][key] = value
            except:
                await ctx.send(await _(ctx, "Invalid formatting! Try again"))
                return
        else:
            pet[4][attribute] = value

        await self.bot.di.add_pet(ctx.author, data.Pet(*pet))
        await ctx.send(await _(ctx, "Slave edited!"))

    @commands.command(aliases=["new"])
    async def hire(self, ctx):
        """hire a new slave for yourself"""
        try:
            check = lambda x: x.channel is ctx.channel and x.author is ctx.author
            pet = dict()
            await ctx.send(await _(ctx, "In any step type 'cancel' to cancel"))
            await ctx.send(await _(ctx, "What will its nickname be?"))
            response = await self.bot.wait_for("message", check=check, timeout=60)
            if response.content.lower() == "cancel":
                await ctx.send(await _(ctx, "Cancelled"))
                return
            else:
                pet["name"] = response.content

            await ctx.send(await _(ctx, "What species of slave is it?"))
            response = await self.bot.wait_for("message", check=check, timeout=60)
            if response.content.lower() == "cancel":
                await ctx.send(await _(ctx, "Cancelled"))
                return
            else:
                pet["type"] = response.content

            await ctx.send(
                await _(ctx, "In any order, what are its stats? (e.g. level, health, attack, defense, spatk, spdef, speed, etc.)"
                             " For example `level: 5, health: 22, attack: 56`"
                             " Type 'skip' to skip."))

            pet["stats"] = dict()
            while True:
                response = await self.bot.wait_for("message", check=check, timeout=120)
                if response.content.lower() == "cancel":
                    await ctx.send(await _(ctx, "Cancelled"))
                    return
                elif response.content.lower() == "skip":
                    await ctx.send(await _(ctx, "Skipping"))
                    break
                else:
                    try:
                        if "\n" in response.content:
                            res = response.content.split("\n")
                        else:
                            res = response.content.split(",")
                        for val in res:
                            key, value = val.split(": ")
                            key = key.strip().casefold()
                            value = value.strip()
                            pet["stats"][key] = int(value)
                        else:
                            break
                    except:
                        await ctx.send(await _(ctx, "Invalid formatting! Try again"))
                        continue
                    continue

            pet["meta"] = dict()
            await ctx.send(await _(ctx, "Any additional data? (Format like the above, for example "
                                        "nature: hasty, color: black)"))

            while True:
                response = await self.bot.wait_for("message", check=check, timeout=120)
                if response.content.lower() == "cancel":
                    await ctx.send(await _(ctx, "Cancelling!"))
                    return
                elif response.content.lower() == "skip":
                    await ctx.send(await _(ctx, "Skipping!"))
                    break
                else:
                    try:
                        if "\n" in response.content:
                            res = response.content.split("\n")
                        else:
                            res = response.content.split(",")
                        for val in res:
                            key, value = val.split(": ")
                            key = key.strip().casefold()
                            value = value.strip()
                            pet["meta"][key] = value
                        else:
                            break
                    except:
                        await ctx.send(await _(ctx, "Invalid formatting! Try again"))
                        continue

            id = await self.bot.di.add_pet(ctx.author, pet)
            await ctx.send("Finished! Slave has been hired with ID {}".format(id))

        except asyncio.TimeoutError:
            await ctx.send(await _(ctx, "Timed out! Try again"))
        except Exception:
            import traceback
            traceback.print_exc()

    @commands.command()
    async def bio(self, ctx, id: data.IntConverter):
        """Get info on a slave"""
        pet = await self.bot.di.get_pet(ctx.author, id)

        embed = discord.Embed(title=f"{pet.name}", color=randint(0, 0xFFFFFF))
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        embed.add_field(name=await _(ctx, "Nickname"), value=pet.name)
        embed.add_field(name=await _(ctx, "Species"), value=pet.type)
        embed.add_field(name=await _(ctx, "ID"), value=pet.id)
        stats = "\n".join(f"{x}: {y}" for x, y in pet.stats.items())
        meta = "\n".join(f"{x}: {y}" for x, y in pet.meta.items())
        embed.add_field(name=await _(ctx, "Stats"), value=stats or "None")
        embed.add_field(name=await _(ctx, "Additional Info"), value=meta or "None")
        embed.set_thumbnail(url="http://www.afropanavision.com/uploads/8/9/9/8/8998038/1373696561.png")

        await ctx.send(embed=embed)

    @commands.command()
    async def release(self, ctx, id: data.IntConverter):
        """Release a slave from you"""
        pk = await self.bot.di.remove_pet(ctx.author, id)
        await ctx.send((await _(ctx, "This slave has been released! Gtfo {}!")).format(pk.name))

    @commands.command()
    async def trade(self, ctx, your_id: data.IntConverter, their_id: data.IntConverter, other: discord.Member):
        """Offer a trade to a user.
        `your_id` is the ID of the slave you want to give, `their_id` is the slave you want from them.
        `other` being the user you want to trade with"""

        await ctx.send(await _(ctx, "Say ey accept or ey decline to respond to the trade!"))
        try:
            resp = await self.bot.wait_for("message", timeout=120, check=lambda
                x: x.author == other and x.channel == ctx.channel and ctx.message.content in ["ey accept",
                                                                                              "ey decline"])
        except asyncio.TimeoutError:
            await ctx.send(await _(ctx, "Failed to respond in time! Cancelling."))
            return

        if resp.content == "ey accept":
            yud = await self.bot.db.get_user_data(ctx.author)
            tud = await self.bot.db.get_user_data(other)

            for your_pet in yud["box"]:
                if your_pet[0] == your_id:
                    break
            else:
                raise KeyError((await _(ctx, "{} is not a valid ID!")).format(your_id))
            yud["box"].remove(your_pet)
            tud["box"].append(your_pet)

            for their_pet in tud["box"]:
                if their_pet[0] == your_id:
                    break
            else:
                raise KeyError((await _(ctx, "{} is not a valid ID!")).format(their_id))
            tud["box"].remove(their_pet)
            yud["box"].append(their_pet)

            your_pet["id"], their_pet["id"] = their_pet["id"], your_pet["id"]

            await self.bot.db.update_user_data(ctx.author, yud)
            await self.bot.db.update_user_data(other, tud)
            await ctx.send((await _(ctx, "Trade completed! Traded {} for {}!")).format(your_pet['name'], their_pet['name']))

        else:
            await ctx.send(await _(ctx, "Trade declined! Cancelling."))

    @commands.command(hidden=True)
    async def accept(self, ctx):
        pass

    @commands.command(hidden=True)
    async def decline(self, ctx):
        pass

def setup(client):
    client.add_cog(Slaves(client))
