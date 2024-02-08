from discord import app_commands
from discord.ext import commands
import discord


class InfoButton(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="BedRock", style=discord.ButtonStyle.blurple)
    async def bedrock(self, button: discord.Interaction, result):
        embed = discord.Embed(
            title="Bedrock Info",
            description="""
            IP: www.example.com
            Port: 12345
            """,
            color=discord.Color.green()
        ).set_footer(text="Join us in the game!")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/948993318770053190/ba269ae20ed99262caeaed88ad65bd84.webp?size=128")
        await button.message.edit(embed=embed, view=None)
        await button.response.defer()

    @discord.ui.button(label="Java", style=discord.ButtonStyle.blurple)
    async def java(self, button: discord.Interaction, result):
        embed = discord.Embed(
            title="Java Info",
            description="""
            IP: www.example.com
            Port: 12345
            """,
            color=discord.Color.green()
        ).set_footer(text="Join us in the game!")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/948993318770053190/ba269ae20ed99262caeaed88ad65bd84.webp?size=128")
        await button.message.edit(embed=embed, view=None)
        await button.response.defer()


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ip", description="Get the IP/Port for Calcite Cube")
    async def ip(self, button: discord.Interaction):
        embed = discord.Embed(
            description="Which version are you playing on?",
            color=discord.Color.green()
        )
        await button.response.send_message(embed=embed, view=InfoButton())

