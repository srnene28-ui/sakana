import discord
from discord.ext import commands

from database import get_user_stats, get_goal


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="プロフィール")
    async def profile(self, ctx):
        stats = get_user_stats(ctx.author.id)

        if stats is None:
            await ctx.reply(" まだXPが登録されてないよ(;o;)")
            return

        goal = get_goal(ctx.author.id)

        embed = discord.Embed(
            title="🐟 プロフィール",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )

        diff = stats["diff"]
        icon = "📈" if diff > 0 else "📉" if diff < 0 else "➖"

        embed.add_field(
            name="💙 現在XP",
            value=f"**{stats['latest_xp']:.1f}**",
            inline=False,
        )

        embed.add_field(
            name="👑 最高XP",
            value=f"**{stats['best_xp']:.1f}**",
            inline=False,
        )

        embed.add_field(
            name=f"{icon} 前回との差",
            value=f"**{diff:+.1f}XP**",
            inline=False,
        )

        if goal is not None:
            remain = goal - stats["latest_xp"]

            if remain <= 0:
                goal_text = f"**{goal:.1f}XP**\n🎉 目標達成してるよ！⁝(ᵒ̴̶̷᷄⌑ ᵒ̴̶̷᷅   )⁝"
            else:
                goal_text = f"**{goal:.1f}XP**\nあと **{remain:.1f}XP**"

            embed.add_field(
                name="⭐️ 目標XP",
                value=goal_text,
                inline=False,
            )

        embed.add_field(
            name="📝 登録回数",
            value=f"**{stats['count']}回**",
            inline=True,
        )

        embed.add_field(
            name="📅 初回登録",
            value=f"`{stats['first_date']}`",
            inline=False,
        )

        embed.add_field(
            name="🕒 最終更新",
            value=f"`{stats['last_date']}`",
            inline=False,
        )

        embed.set_footer(
            text="🌀 これからも一緒にがんばろう🐟",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Profile(bot))
