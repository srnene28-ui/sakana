import re
import random
import discord
from discord.ext import commands

from database import (
    add_xp,
    get_latest_xp,
    get_best_xp,
)

XP_PATTERN = re.compile(r"(?i)\bxp\s*([0-9]{4}\.[0-9])\b")

CHEERS = [
    "更新⋯ってコト？！",
    "なんとかなれーッ！",
    "泣いても涙がでないや",
    "サイコーッ！",
    "泣いちゃった！",
    "えッッ！",
    "今度はギリギリ攻めるね！",
    "甘かったんだッ⋯処理が⋯",
]

class XP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        match = XP_PATTERN.search(message.content)

        if not match:
            return

        xp = float(match.group(1))

        latest = get_latest_xp(message.author.id)
        best = get_best_xp(message.author.id)

        if latest is not None and float(latest) == xp:
            embed = discord.Embed(
                title="📷 前回と同じXPだよ！",
                description="今回は記録してないよ！:",
                color=0x7DD3FC,
            )

            await message.reply(embed=embed)
            return

        add_xp(
            message.author.id,
            message.author.display_name,
            xp,
        )

        if latest is None:

            embed = discord.Embed(
                title="🐟 XPを初めて登録したよ！",
                description=(
                    f"💙 **現在XP**\n"
                    f"**{xp:.1f}**\n\n"
                    f"📝 今日から記録スタートだ！\n"
                    f"これから一緒にがんばろう🐟"
                ),
                color=0x7DD3FC,
            )

            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url
            )

            embed.set_footer(
                text=random.choice(CHEERS),
                icon_url=message.author.display_avatar.url
            )

            await message.reply(embed=embed)
            return

        diff = xp - float(latest)

        if diff > 0:
            icon = "📈"
        elif diff < 0:
            icon = "📉"
        else:
            icon = "➖"

        cheer = random.choice(CHEERS)

        embed = discord.Embed(
            title="🐟 XPを記録したよ！(ᐢ･ω･ᐢ)",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url
        )

        embed.add_field(
            name="💙 現在XP",
            value=f"**{xp:.1f}**",
            inline=False,
        )

        embed.add_field(
            name=f"{icon} 前回との差",
            value=f"**{diff:+.1f}XP**",
            inline=False,
        )

        if best is None or xp > float(best):

            embed.add_field(
                name="🐟 自己ベスト",
                value="**最高値更新だー！( ꈍ꒳ꈍ )**",
                inline=False,
            )

        embed.set_footer(
            text=cheer,
            icon_url=message.author.display_avatar.url
        )

        await message.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(XP(bot))
