from __future__ import annotations
import typing as t

from discord.ext import commands, tasks
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
    if t.TYPE_CHECKING:
        discloud_client: discloud.Client
        app_manager: utils.AppManager
        tree: Tree

    def __init__(self) -> None:
        self.discloud_client = discloud.Client(utils.dotenv_get("DISCLOUD_TOKEN"))
        self.app_manager = utils.AppManager(self)

        intents = discord.Intents.default()
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            tree_cls=Tree
        )

    async def setup_hook(self) -> None:
        for file in pathlib.Path("./cogs").glob("**/[!_]*.py"):
            ext = ".".join(file.parts) \
                     .removesuffix(".py")
            await self.load_extension(ext)

        self._reset_apps_cache.start()

    @tasks.loop(hours=1)
    async def _reset_apps_cache(self) -> None:
        self.app_manager._cache.clear()

bot = Discloud()
bot.run(utils.dotenv_get("TOKEN"), log_level=40)