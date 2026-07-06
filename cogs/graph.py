import os
from collections import defaultdict
from datetime import datetime, timedelta

import discord
from discord.ext import commands

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from database import get_all_history

#plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False

Y_TICKS = [2000, 2300, 2500, 2800, 3000, 3100, 3200, 3300]


def to_jst(dt):
    return dt + timedelta(hours=9)


def round_to_slot_hour(dt):
    hour = dt.hour

    if hour % 2 == 0:
        hour += 1

    if hour < 5:
        hour = 5

    if hour > 23:
        hour = 23

    return hour


class Graph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="グラフ")
    async def graph(self, ctx):
        rows = get_all_history()

        if not rows:
            await ctx.reply(" まだXPデータがないよ(;o;)")
            return

        users = defaultdict(dict)

        for user_id, name, xp, created_at in rows:
            dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            dt = to_jst(dt)

            hour = round_to_slot_hour(dt)
            label = f"{dt.strftime('%m/%d')}\n{hour:02d}:00"

            users[name][label] = float(xp)

        labels = sorted(
            {label for history in users.values() for label in history.keys()}
        )

        os.makedirs("data", exist_ok=True)
        file_path = "data/team_xp_graph.png"

        fig, ax = plt.subplots(figsize=(10, 6))

        fig.patch.set_facecolor("#DDF5FF")
        ax.set_facecolor("#F7FDFF")

        ax.grid(
            True,
            color="#D6EFFF",
            linestyle="--",
            linewidth=0.7
        )

        ax.set_yticks(Y_TICKS)
        ax.set_ylim(1950, 3350)

        ax.set_ylabel("XP")
        ax.set_title("XP History", weight="bold")

        for name, history in users.items():
            values = [history.get(label, None) for label in labels]

            ax.plot(
                labels,
                values,
                marker="o",
                linewidth=3,
                markersize=8,
                label=name,
            )

            valid_points = [
                (i, value)
                for i, value in enumerate(values)
                if value is not None
            ]

            if valid_points:
                best_i, best_y = max(valid_points, key=lambda item: item[1])

                ax.scatter(
                    labels[best_i],
                    best_y,
                    marker="*",
                    s=220,
                    zorder=5,
                )

        ax.tick_params(axis="x", rotation=0)

        ax.legend()

        plt.tight_layout()

        plt.savefig(
            file_path,
            dpi=200,
            facecolor=fig.get_facecolor()
        )

        plt.close()

        file = discord.File(
            file_path,
            filename="team_xp_graph.png"
        )

        embed = discord.Embed(
            title="🎐 XP History 🐟",
            description="⭐ は自己ベストだよ‎！",
            color=0x7DD3FC,
        )

        embed.set_author(
            name=ctx.guild.name if ctx.guild else "XP Bot",
            icon_url=(
                ctx.guild.icon.url
                if ctx.guild and ctx.guild.icon
                else ctx.author.display_avatar.url
            )
        )

        embed.set_image(
            url="attachment://team_xp_graph.png"
        )

        embed.set_footer(
            text="今日もXP更新がんばろう‎( > ·̫ <)👍🏻🌟",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(
            file=file,
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Graph(bot))
