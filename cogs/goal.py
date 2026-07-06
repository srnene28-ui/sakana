import discord
from discord.ext import commands

from database import set_goal, get_goal, get_latest_xp


class Goal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="目標")
    async def goal(self, ctx, goal: float = None):

        if goal is None:
            saved = get_goal(ctx.author.id)

            if saved is None:
                await ctx.reply("🐟 まだ目標が設定されてないよ！\n`!目標 3200` ⬅️みたいに設定してね( ᴖ⩊ᴖ )")
                return

            latest = get_latest_xp(ctx.author.id)

            embed = discord.Embed(
                title="🎐 Goal 🐟",
                color=0x7DD3FC,
            )

            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url
            )

            embed.add_field(
                name="👑 目標XP",
                value=f"**{saved:.1f}**",
                inline=False,
            )

            if latest is not None:
                remain = saved - latest

                if remain <= 0:
                    embed.add_field(
                        name="🎉 達成！",
                        value="目標達成おめでとう！！( ᵒ̴̶̷̥́ ·̫ ᵒ̴̶̷̣̥ )",
                        inline=False,
                    )
                else:
                    embed.add_field(
                        name="💙 あと",
                        value=f"**{remain:.1f}XP**",
                        inline=False,
                    )

            await ctx.reply(embed=embed)
            return

        set_goal(ctx.author.id, goal)

        embed = discord.Embed(
            title="🏆 目標を設定したよ！‎( > ·̫ <)👍🏻🌟",
            description=f"**{goal:.1f}XP** を目指そう🐟",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )

        embed.set_footer(
            text="泣いても涙がでないや",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Goal(bot))
