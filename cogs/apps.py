from __future__ import annotations
import typing as t

from discord.ext import commands
from discord import app_commands
import discord

from discloud.errors import RequestError

import utils
import views

from pathlib import Path
import os

if t.TYPE_CHECKING:
    from core import Discloud

class Apps(commands.Cog):
    def __init__(self, bot: Discloud) -> None:
        self.bot = bot
        self.app_manager = utils.AppManager(bot)

    @app_commands.command(name="apps", description="Mostra todos os seus aplicativos na discloud")
    async def get_apps(self, interaction: discord.Interaction) -> None:
        apps = await self.app_manager.get_app("all")
        embed = discord.Embed(
            title="Selecione um app",
            description="Selecione um aplicativo abaixo para verificar seus status",
            color=utils.DISCLOUD_COLOR
        )

        chunks = discord.utils.as_chunks(apps, 25)
        len_chunks = sum((1 for _ in chunks))

        if len_chunks > 5:
            return await interaction.response.send_message("Você tem tantos bots, que não é possível mostrar todos no discord! Por favor, use o site")

        view = discord.ui.View()

        for chunk in chunks:
            view.add_item(
                views.SelectApp(
                    apps=chunk, 
                    manager=self.app_manager,
                    bot=self.bot
                )
            )

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="app", description="Mostra uma dos seus aplicativos na discloud")
    @app_commands.describe(id="O ID da sua aplicação")
    async def get_app(self, interaction: discord.Interaction, id: str) -> None:
        if not id.isdigit():
            return await interaction.response.send_message("> O ID deve ser um número!", ephemeral=True)

        try:
            app = await self.app_manager.get_app(id)
        except RequestError as e:
            await interaction.response.send_message(e.args[0], ephemeral=True)
            return
        await interaction.response.send_message(embed=app.to_embed(), view=app.dashboard(), ephemeral=True)

    @app_commands.command(name="commit", description="Commita os arquivos da sua aplicação na discloud")
    @app_commands.describe(id="O ID da sua aplicação", file="Os arquivos (em .zip) da sua aplicação")
    async def commit(self, interaction: discord.Interaction, id: str, file: discord.Attachment) -> None:
        if not id.isdigit():
            return await interaction.response.send_message("> O ID deve ser um número!", ephemeral=True)

        try:
            app = await self.app_manager.get_app(id)
        except RequestError as e:
            await interaction.response.send_message(e.args[0], ephemeral=True)
            return
        await file.save(Path("./commit.zip"))
        await app.commit(utils.File("commit.zip"))
        os.remove("./commit.zip")

        await interaction.response.send_message("Aplicação atualizada com sucesso!", ephemeral=True)

async def setup(bot: Discloud) -> None:
    cog = Apps(bot)
    await bot.add_cog(cog)