from __future__ import annotations
import typing as t

from discord import ui
import discord

if t.TYPE_CHECKING:
    from core import Discloud
    from utils import (
        AppManager,  
        App
    )

class SelectApp(ui.Select):
    def __init__(self, apps: t.Iterable[App], bot: Discloud, manager: AppManager) -> None:
        self.manager = manager
        self.client = bot.discloud_client
        self.bot = bot

        options = [discord.SelectOption(label=app.fullname, value=app.id) for app in apps]
        options = sorted(options, key=lambda x: x.label, reverse=True)

        super().__init__(
            placeholder="Aperte Aqui!",
            options=options
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        selected = self.values[0]
        app = await self.manager.get_app(selected)
        await interaction.response.send_message(embed=app.to_embed(), view=app.dashboard(), ephemeral=True)

class Restart(ui.Button):
    def __init__(self, app: App):
        self.app = app
        super().__init__(
            label="Restart",
            emoji="\U0001f501", 
            style=discord.ButtonStyle.red,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("O Aplicativo será reiniciado em breve", ephemeral=True)
        await self.app.restart()

class Start(ui.Button):
    def __init__(self, app: App) -> None:
        self.app = app
        super().__init__(
            label="Start",
            emoji="\U000025b6",
            style=discord.ButtonStyle.green,
        )
    
    async def callback(self, interaction: discord.Interaction) -> None:
        action = await self.app.start()
        await interaction.response.send_message(action.message, ephemeral=True)

class Stop(ui.Button):
    def __init__(self, app: App) -> None:
        self.app = app
        super().__init__(
            label="Stop",
            emoji="\U000023f9",
            style=discord.ButtonStyle.red,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("O Aplicativo será desligado em breve", ephemeral=True)
        await self.app.stop()

class Backup(ui.Button):
    def __init__(self, app: App) -> None:
        self.app = app
        super().__init__(
            label="Backup", 
            emoji="\U0001f4be", 
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        from utils import DISCLOUD_COLOR

        bckp = await self.app.backup()

        embed = discord.Embed(
            description=f"Aperte [aqui]({bckp.url}) para baixar os arquivos de {self.app.fullname}",
            color=DISCLOUD_COLOR
        )

        embed.set_author(name=self.app.fullname, icon_url=self.app.avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Terminal(ui.Button):
    def __init__(self, app: App) -> None:
        self.app = app
        super().__init__(
            label="Terminal", 
            emoji="\U0001f5a8", 
            style=discord.ButtonStyle.blurple
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        from utils import DISCLOUD_COLOR

        await interaction.response.defer(ephemeral=True)

        terminal = await self.app.terminal()
        e = discord.Embed(
            description=f"```{terminal.small}```",
            color=DISCLOUD_COLOR
        )
        await interaction.followup.send(embed=e, ephemeral=True)

class Dashboard(ui.View):
    def __init__(self, app: App):
        super().__init__(timeout=180)
        self.app = app

        if self.app.is_online:
            self.add_item(Stop(app))
            self.add_item(Restart(app))
            self.add_item(Backup(app))
            self.add_item(Terminal(app))
        else:
            self.add_item(Start(app))
            self.add_item(Backup(app))
            self.add_item(Terminal(app))
