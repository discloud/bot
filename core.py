from __future__ import annotations
import typing as t

from discord.ext import commands
from discord import app_commands
import discord

import discloud

import pathlib

import utils

class Tree(app_commands.CommandTree):
    def __init__(self, client: t.Type[discord.Client], *, fallback_to_global: bool = True):
        super().__init__(client, fallback_to_global=fallback_to_global)
    
    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError, /) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f"> O comando está em cooldown. Tente novamente em `{error.retry_after:.1f}s`")

        if isinstance(error, app_commands.MissingPermissions):
            return await interaction.response.send_message(f"> Você não tem permissão para executar esse comando")
        
        await super().on_error(interaction, error)

class Discloud(commands.Bot):
    def __init__(self) -> None:
        self.discloud_client = discloud.Client(utils.dotenv_get("DISCLOUD_TOKEN"))

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="",
            intents=intents,
            tree_cls=Tree
        )

    async def setup_hook(self) -> None:
        for file in pathlib.Path("./cogs").glob("**/[!_]*.py"):
            ext = ".".join(file.parts) \
                     .removesuffix(".py")
            await self.load_extension(ext)

    async def on_message(self, message: discord.Message, /) -> None:
        if message.content.lower() == "!sync":
            s = await self.tree.sync()
            await message.channel.send(str(s))

    async def on_ready(self) -> None:
        print("ready")

bot = Discloud()
bot.run(utils.dotenv_get("TOKEN"), log_level=40)