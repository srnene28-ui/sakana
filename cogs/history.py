import discord
from discord.ext import commands
from datetime import datetime, timedelta

from database import get_history


class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="履歴")
    async def history(self, ctx, page: int = 1):
        if page < 1:
            page = 1

        rows = get_history(ctx.author.id, limit=10, offset=(page - 1) * 10)

        if not rows:
            await ctx.reply("🎣 履歴がまだないよ(;o;)")
            return

        embed = discord.Embed(
            title="️📝 XP History 🐟",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )

        previous = None

        for i, (xp, created_at) in enumerate(rows, start=1):
            dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S") + timedelta(hours=9)

            if previous is None:
                diff = "🎐 初回"
            else:
                value = xp - previous
                diff = f"📈 +{value:.1f}" if value > 0 else f"📉 {value:.1f}" if value < 0 else "➖ ±0.0"

            previous = xp

            embed.add_field(
                name=f"{i}. {xp:.1f}",
                value=f"{diff}\n🕘 {dt.strftime('%m/%d %H:%M')}",
                inline=False,
            )

        embed.set_footer(
            text=f"Page {page}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(History(bot))
