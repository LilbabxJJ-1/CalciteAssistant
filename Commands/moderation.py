import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import aiohttp


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="warn",
        description="warn a user"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.User, reason: str):
        await interaction.response.defer()
        embed = discord.Embed(
            title="You've been Warned",
            description=f"""
            You've been warned in Calcite Cube for:
            `{reason}`
            """,
            color=discord.Color.red()
        )
        await user.send(embed=embed)
        sess = aiohttp.ClientSession()
        req = await sess.get(
            f'https://www.charm-cord.com/database/getuservar/{user.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=warnings')
        value = await req.json()
        await sess.post(
            f'https://www.charm-cord.com/database/setuservar/{user.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=warnings&value={int(value['value']) + 1}')
        embed = discord.Embed(
            description=f"""Successfully warned {user.mention}!
                            They now have: {int(value['value']) + 1} warnings!""",
            color=discord.Color.green()
        )
        await interaction.channel.typing()
        await asyncio.sleep(3)
        await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="check-warns",
        description="Check how many warnings a user has"
    )
    async def check_warns(self, interaction: discord.Interaction, user: discord.User = None):
        if user is None:
            sess = aiohttp.ClientSession()
            req = await sess.get(
                f'https://www.charm-cord.com/database/getuservar/{interaction.user.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=warnings'
            )
            value = await req.json(content_type="application/json")
            await sess.close()
            embed = discord.Embed(
                title="Warning Count",
                description=f"You have a total of: {value['value']} warnings!",
                color=discord.Color.red()
            )

        else:
            sess = aiohttp.ClientSession()
            req = await sess.get(
                f'https://www.charm-cord.com/database/getuservar/{user.id}?key=278fed06f22cfaf5f345e12df4fe5bde&variable=warnings'
            )
            value = await req.json()
            embed = discord.Embed(
                title="Warning Count",
                description=f"{user.mention} has a total of: {value['value']} warnings!",
                color=discord.Color.red()
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="block",
        description="Block users from using the dm tickets"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def block(self, interaction: discord.Interaction, user: discord.User):
        sess = aiohttp.ClientSession()
        blocked: list = (
            await
            (
                await sess.get(f'https://www.charm-cord.com/database/getvar?key'
                               f'=278fed06f22cfaf5f345e12df4fe5bde&variable=blocked')
            ).json()
        )['value']
        if user.id in blocked:
            embed = discord.Embed(
                title="Error",
                description="""
                This user has been blocked from using dm tickets already
                """,
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            await sess.close()
            return
        else:
            blocked.append(user.id)
            await sess.post('https://www.charm-cord.com/database/setvar?key'
                            f'=278fed06f22cfaf5f345e12df4fe5bde&variable=blocked&value={blocked}')

            embed = discord.Embed(
                description=f"""
                Successfully blocked {user.mention} from tickets
                """,
                color=discord.Color.green()
            )
            await sess.close()
            await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="unblock",
        description="Unblock users from using the dm tickets"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def unblock(self, interaction: discord.Interaction, user: discord.User):
        sess = aiohttp.ClientSession()
        blocked: list = (
            await
            (
                await sess.get(f'https://www.charm-cord.com/database/getvar?key'
                               f'=278fed06f22cfaf5f345e12df4fe5bde&variable=blocked')
            ).json()
        )['value']
        if user.id not in blocked:
            embed = discord.Embed(
                title="Error",
                description="""
                    This user has been unblocked from using dm tickets already
                    """,
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            await sess.close()
            return
        else:
            blocked.remove(user.id)
            await sess.post('https://www.charm-cord.com/database/setvar?key'
                            f'=278fed06f22cfaf5f345e12df4fe5bde&variable=blocked&value={blocked}')

            embed = discord.Embed(
                description=f"""
                    Successfully unblocked {user.mention} from tickets
                    """,
                color=discord.Color.green()
            )
            await sess.close()
            await interaction.response.send_message(embed=embed)
