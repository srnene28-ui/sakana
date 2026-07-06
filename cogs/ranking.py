import random
import discord
from discord.ext import commands

from database import get_ranking

FOOTERS = [
    "簡単ッッッ！簡単ッッ！",
    "すぐにしたかったんだッ⋯「共有」ッ",
    "あきらめたくないッッ！！",
    "不思議となんだか余裕があります",
]


class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ランキング")
    async def ranking(self, ctx):

        rows = get_ranking(5)

        if not rows:
            await ctx.reply("🫧 まだXPデータがないよ！")
            return

        embed = discord.Embed(
            title="🎐 XP Ranking 🐟",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.guild.name if ctx.guild else "XP Ranking",
            icon_url=ctx.guild.icon.url if ctx.guild and ctx.guild.icon else ctx.author.display_avatar.url
        )

        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

        ranking_text = ""

        for i, (_, name, xp) in enumerate(rows):
            ranking_text += (
                f"{medals[i]} **{name}**\n"
                f"└ 💙 `{xp:.1f} XP`\n\n"
            )

        embed.description = ranking_text

        embed.set_footer(
            text=random.choice(FOOTERS),
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Ranking(bot))
