from __future__ import annotations
import typing as t

import discloud
import discord

from collections import OrderedDict

import views
import utils

__all__ = (
    "AppManager",
    "App",
    "File"
)

if t.TYPE_CHECKING:
    from core import Discloud

    from io import BufferedReader
    from discloud.discloud import (
        Client, 
        AppData, 
        AppsPayload, 
        Backup,
        Action,
        File as DiscloudFile
    )

class AppDataWithDiscord(discloud.discloud.AppData):
    name: str
    avatar: str

class TerminalData(t.TypedDict):
    url: str
    small: str
    big: str

class LogsData(t.TypedDict):
    id: str
    terminal: TerminalData 

class Logs:
    def __init__(self, data: LogsData) -> None:
        terminal = data["terminal"]
        self.url = terminal["url"]
        self.small = terminal["small"]
        self.full = self.big = terminal["big"]

    def __str__(self) -> str:
        return self.small 

    def reset(self) -> Action:
        return NotImplemented
    
class File(discloud.discloud.File):
    def __init__(self, fp: t.Union[str, BufferedReader]) -> None:
        super().__init__(fp)
        self.filename = fp

class App(discloud.discloud.Application):
    def __init__(self, client: Client, payload: AppDataWithDiscord) -> None:
        self.avatar = payload.get("avatar")
        
        nick = payload.get("name")
        name, discriminator = nick.split("#", maxsplit=1)
        self.name = name
        self.discriminator = discriminator
        self.fullname = f"{name}#{discriminator}"

        super().__init__(client, payload)
        self.is_online = self.status == "Online"

    def __repr__(self) -> str:
        return f"<name={repr(self.name)} discriminator={repr(self.discriminator)} id={repr(self.id)} cpu={repr(self.cpu)}>"

    def to_embed(self) -> discord.Embed:
        e = discord.Embed(
            title=self.name,
            color=utils.DISCLOUD_COLOR,
            description=(
                f"***Status:*** *{self.status}*\n"
                f"***CPU:*** *{self.cpu}*\n"
                f"***RAM:*** *{self.memory.using}/{self.memory.available}*\n"
            )
        )
        e.set_author(name=self.fullname, icon_url=self.avatar)
        return e
    
    def dashboard(self) -> views.Dashboard:
        return views.Dashboard(self)

    @t.overload
    async def _client_backup(self, target: str) -> Backup:
        ...

    @t.overload
    async def _client_backup(self, target: t.Literal["all"]) -> t.List[Backup]:
        ...

    async def _client_backup(
        self, target: t.Union[str, t.Literal["all"]]
    ) -> t.Union[Backup, t.List[Backup]]:
        return await self._client.backup(target)

    async def backup(self) -> Backup:
        return await self._client_backup(self.id)
    
    @t.overload
    async def _client_terminal(self, target: str) -> Logs:
        ...

    @t.overload
    async def _client_terminal(self, target: t.Literal["all"]) -> t.List[Logs]:
        ...

    async def _client_terminal(
        self, target: t.Union[str, t.Literal["all"]]
    ) -> t.Union[Logs, t.List[Logs]]:
        r = await self._client.http.fetch_logs(target)
        return Logs(r.data["apps"])

    async def terminal(self) -> Logs:
        return await self._client_terminal(self.id)
    
    async def restart(self) -> Action:
        return await self._client.restart(self.id)
    
    async def start(self) -> Action:
        return await self._client.start(self.id)
    
    async def stop(self) -> Action:
        return await self._client.stop(self.id)

    async def commit(self, file: DiscloudFile) -> Action:
        return await self._client.commit(self.id, file)

_KT = t.TypeVar("_KT")
_VT = t.TypeVar("_VT")

_VT_A: t.TypeAlias = t.Union[_VT, t.List[_VT]]
_KT_A: t.TypeAlias = t.Union[_KT, t.Literal["all"]]

class GenericCache(t.Generic[_KT, _VT]):
    """LRU Caching"""
    def __init__(self, size: int) -> None:
        self._lru_order: OrderedDict[_KT_A, None] = OrderedDict()
        self._cache: t.Dict[_KT_A, _VT_A] = {}
        self._size = size

    def _update_lru(self, __key: _KT_A) -> None:
        del self._lru_order[__key]
        self._lru_order[__key] = None

    def __getitem__(self, __key: _KT_A) -> _VT_A:
        self._update_lru(__key)
        return self._cache[__key]

    def __setitem__(self, __key: _KT_A, __value: _VT_A) -> None:
        if __key in self._cache:
            self._update_lru(__key)
            self._cache[__key] = __value
        else:
            if len(self._cache) == self._size:
                lru_key = next(iter(self._lru_order))
                del self._cache[lru_key]
                del self._lru_order[lru_key]
            self._cache[__key] = __value
            self._lru_order[__key] = None

    def __contains__(self, __o: _KT_A) -> bool:
        return __o in self._cache

    def get_all(self) -> t.List[_VT]:
        return self._cache["all"]

class AppManager:
    def __init__(self, bot: Discloud) -> None:
        self._client = bot.discloud_client
        self.bot = bot

        self._cache = GenericCache[str, App](128)

    @staticmethod
    def _add_discord_attrs(app: AppData, usr: discord.User) -> AppDataWithDiscord:
        copy: AppDataWithDiscord = {
            **app, 
            "name": f"{usr.display_name}#{usr.discriminator}", 
            "avatar": usr.display_avatar.url
        } 
        return copy

    async def _instantiate_apps(self, apps: t.Iterable[AppData]) -> t.List[App]:
        instanciaded_apps: t.List[App] = []
        for raw_app in apps:
            usr = await self.bot.fetch_user(int(raw_app["id"]))
            treated = self._add_discord_attrs(raw_app, usr)

            app = App(self._client, treated)
            instanciaded_apps.append(app)
        return instanciaded_apps

    @t.overload
    async def get_app(self, target: t.Literal["all"]) -> t.List[App]:
        ...

    @t.overload
    async def get_app(self, target: str) -> App:
        ...

    async def get_app(
        self, target: t.Union[str, t.Literal["all"]]
    ) -> t.Union[t.List[App], App]:
        if target in self._cache:
            if target != "all" and target in self._cache.get_all(): # `target` is cached on the `all` list
                r = discord.utils.get(self._cache.get_all(), id=target)
                if r:
                    return r
            return self._cache[target]

        req_error = discloud.errors.RequestError
        try:
            raw_result = await self._client.http.fetch_app(target)
        except req_error as e:
            raise req_error("O App solicitado não foi encontrado") from e

        data: AppsPayload = raw_result.data
        apps: t.Union[t.List[AppData], AppData] = data["apps"]

        if isinstance(apps, list):
            instanciaded_apps = await self._instantiate_apps(apps)
            self._cache["all"] = instanciaded_apps
            return instanciaded_apps

        raw_app: AppData = apps
        app = await self._instantiate_apps([raw_app])
        app = app[0]

        self._cache[target] = app
        return app
