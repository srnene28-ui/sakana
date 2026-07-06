import discord
from discord.ext import commands

from database import delete_latest_xp, get_latest_xp


class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="削除")
    async def delete(self, ctx):
        deleted_xp = delete_latest_xp(ctx.author.id)

        if deleted_xp is None:
            await ctx.reply("🚯 削除できるXPがないよ！")
            return

        latest = get_latest_xp(ctx.author.id)

        embed = discord.Embed(
            title="🗑 XPを削除したよ！",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )

        if latest is None:
            embed.description = f"削除したXP：**{deleted_xp:.1f}**\n\n記録が空になったよ🐟"
        else:
            embed.description = (
                f"削除したXP：**{deleted_xp:.1f}**\n\n"
                f"現在の最新XP：**{latest:.1f}**"
            )

        embed.set_footer(
            text="食べすぎちゃった",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Delete(bot))
