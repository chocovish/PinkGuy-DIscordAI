async def _(ctx, translation):
    currency = "chromosomes"
    if ctx.guild is not None:
        gd = await ctx.bot.db.get_guild_data(ctx.guild)
        lang = gd.get("lang", "en")
        currency = gd.get("currency") or currency
        if lang != "en":
            try:
                translation = ctx.bot.translations[translation][lang]
            except:
                pass

    return translation.replace("chromosomes", currency)
