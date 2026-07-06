import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import init_db

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True


class XPBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        init_db()
        await self.load_extension("cogs.xp")
        await self.load_extension("cogs.profile")
        await self.load_extension("cogs.ranking")
        await self.load_extension("cogs.graph")
        await self.load_extension("cogs.help")
        await self.load_extension("cogs.delete")
        await self.load_extension("cogs.history")
        await self.load_extension("cogs.goal")
        await self.load_extension("cogs.rival")

bot = XPBot()


@bot.event
async def on_ready():
    print(f"🐟 {bot.user} がログインしたよ！")


async def main():
    async with bot:
        await bot.start(TOKEN)


asyncio.run(main())
