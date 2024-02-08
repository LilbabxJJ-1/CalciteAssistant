import discord
from discord.ext import commands
import asyncio
import aiohttp
from datetime import datetime, timedelta
from Commands import Info, Moderation

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), case_insensitive=True)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Ready on {bot.user.name}")


class ticketButton(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red)
    async def close(self, button: discord.Interaction, result):
        await button.channel.send("Closing ticket in 10 seconds")
        await button.response.defer()
        sess = aiohttp.ClientSession()
        blocked: list = (await (await sess.get(
            f'https://www.charm-cord.com/database/getvar?key=278fed06f22cfaf5f345e12df4fe5bde&variable=blocked')).json())[
            'value']
        blocked.append(str(button.user.id))

    @discord.ui.button(label="Block User", style=discord.ButtonStyle.blurple)
    async def java(self, button: discord.Interaction, result):
        embed = discord.Embed(
            title="Java Info",
            description="""
            IP: www.example.com
            Port: 12345
            """,
            color=discord.Color.green()
        ).set_footer(text="Join us in the game!")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/948993318770053190/ba269ae20ed99262caeaed88ad65bd84.webp?size=128")
        await button.message.edit(embed=embed, view=None)
        await button.response.defer()


@bot.event
async def on_message(msg: discord.Message):
    if isinstance(msg.channel, discord.DMChannel):
        if not msg.author.bot:
            sess = aiohttp.ClientSession()
            blocked: list = (
                await
                (
                    await sess.get(f'https://www.charm-cord.com/database/getvar?key'
                                   f'=278fed06f22cfaf5f345e12df4fe5bde&variable=blocked')
                ).json()
            )['value']
            if msg.author.id in blocked:
                embed = discord.Embed(
                    title="Error",
                    description="""
                You have been blocked by staff from sending messages.
                Anything sent here will not be sent to staff
                """,
                    color=discord.Color.red()
                )
                await msg.author.send(embed=embed)
                await sess.close()
                return
            await msg.add_reaction("☑")
            req = await sess.get(
                f'https://www.charm-cord.com/database/getuservar/{msg.author.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=haschat')
            value = await req.json()
            if value['value'] == "No":
                guild: discord.Guild = await bot.fetch_guild(927965860218425445)
                category: discord.CategoryChannel = await guild.fetch_channel(1205187451891486751)
                channel = await guild.create_text_channel(category=category,
                                                          name=f"Ticket-{msg.author.name}")
                await channel.send(f"{msg.author.name}: {msg.content}")
                await sess.post(
                    f'https://www.charm-cord.com/database/setuservar/{msg.author.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=haschat&value=Yes'
                )
                await sess.post(
                    f'https://www.charm-cord.com/database/setuservar/{msg.author.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=chat&value={channel.id}'
                )
                await sess.close()
                return
            else:
                req = await sess.get(
                    f'https://www.charm-cord.com/database/getuservar/{msg.author.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=chat'
                )
                await sess.close()
                channel_id = int((await req.json())['value'])
                channel = await bot.fetch_channel(channel_id)
                await channel.send(f"{msg.author.name}: {msg.content}")
    elif msg.channel.category.id == 1205187451891486751 and not msg.author.bot:
        user: discord.Member = discord.utils.get(msg.guild.members, name=msg.channel.name.replace("ticket-", ""))
        await user.send(f"{msg.author}: {msg.content}")
        await msg.add_reaction("☑")


async def get_commands():
    await bot.add_cog(Info(bot))
    await bot.add_cog(Moderation(bot))
    print("Successfully added cogs")


asyncio.run(get_commands())

bot.run("TOKEN")
