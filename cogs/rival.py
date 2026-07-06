import discord
from discord.ext import commands

from database import get_current_ranking_all


class Rival(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ライバル")
    async def rival(self, ctx):
        rows = get_current_ranking_all()

        if not rows:
            await ctx.reply(" まだXPデータがないよ(;o;)")
            return

        user_id = ctx.author.id
        my_index = None

        for i, (uid, name, xp) in enumerate(rows):
            if uid == user_id:
                my_index = i
                break

        if my_index is None:
            await ctx.reply(" まだXPが登録されてないよ(;o;)")
            return

        my_rank = my_index + 1
        my_name = rows[my_index][1]
        my_xp = rows[my_index][2]

        embed = discord.Embed(
            title="🐟 Rival",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )

        embed.add_field(
            name="💙 じぶん",
            value=f"**{my_rank}位**　`{my_xp:.1f} XP`",
            inline=False,
        )

        if my_index > 0:
            upper_name = rows[my_index - 1][1]
            upper_xp = rows[my_index - 1][2]
            diff_up = upper_xp - my_xp

            embed.add_field(
                name="⬆ 上のライバル",
                value=f"**{upper_name}** まであと **{diff_up:.1f}XP**",
                inline=False,
            )
        else:
            embed.add_field(
                name="👑 上のライバル",
                value="今あなたが1位だよ！o̴̶̷̤ ̫ o̴̶̷̤✨️",
                inline=False,
            )

        if my_index < len(rows) - 1:
            lower_name = rows[my_index + 1][1]
            lower_xp = rows[my_index + 1][2]
            diff_down = my_xp - lower_xp

            embed.add_field(
                name="⬇ 下のライバル",
                value=f"**{lower_name}** に **{diff_down:.1f}XP** リード中",
                inline=False,
            )
        else:
            embed.add_field(
                name="🎣 下のライバル",
                value="下にはまだ誰もいないよ！",
                inline=False,
            )

        embed.set_footer(
            text="不思議となんだか余裕があります",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Rival(bot))
