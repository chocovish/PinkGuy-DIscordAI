import asyncio
from aiohttp import web


async def host():
    runner = web.AppRunner()
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("======= Serving on http://127.0.0.1:8080/ ======")

async def execute():
    await host()
