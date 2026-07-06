import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ヘルプ")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🌀 XP Bot Help 🐟",
            description="使えるコマンド一覧だよ（ᐢ･ω･ᐢ）",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.guild.name if ctx.guild else "XP Bot",
            icon_url=ctx.guild.icon.url if ctx.guild and ctx.guild.icon else ctx.author.display_avatar.url
        )

        embed.add_field(
            name="🐟 XP登録",
            value="`XP 2500.0`\n小数点まで打ってね！XPを自動で記録するよo̴̶̷̤ ̫ o̴̶̷̤✨️",
            inline=False,
        )

        embed.add_field(
            name="👤 !プロフィール",
            value="現在XP・最高XP・目標XP・登録回数などなどみれるよ🦭",
            inline=False,
        )

        embed.add_field(
            name="👑 !目標",
            value="`!目標 3000`\n目標XPを設定するよ🔥\n`!目標` で確認できるよ( ᴖ⩊ᴖ )",
            inline=False,
        )

        embed.add_field(
            name="🎐 !ランキング",
            value="みんなの最新XPランキングがみれるよჱ̒( .  ̫ .",
            inline=False,
        )

        embed.add_field(
            name="🐟 !ライバル",
            value="自分の上下のライバルとの差がみれるよ( ⌯᷄௰⌯᷅ )",
            inline=False,
        )

        embed.add_field(
            name="🌧 !グラフ",
            value="みんなのXP推移グラフがみれるよ(ᐡ• ·̫ •ᐡ)",
            inline=False,
        )

        embed.add_field(
            name="🌀 !履歴",
            value="じぶんのXP履歴がみれるよ！\n`!履歴 2` でつぎのページもみられるよ(◦`꒳´◦)",
            inline=False,
        )

        embed.add_field(
            name="🗑 !削除",
            value="じぶんの最新XPを1件だけ削除するよ( ^-^)⊃⌒o",
            inline=False,
        )

        embed.add_field(
            name="🆘 !ヘルプ",
            value="このヘルプを表示するよ‎(｡•ᴗ•∩)",
            inline=False,
        )

        embed.set_footer(
            text="今日もXP更新がんばろう‎( > ·̫ <)👍🏻🌟",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
