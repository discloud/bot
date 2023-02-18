from __future__ import annotations
import typing as t

from .discloud_manager import *

DISCLOUD_COLOR = 0x5cf28c

def dotenv_get(var_name: str, *, path: str = ".env") -> t.Any:
    with open(path, "r", encoding="UTF-8") as f:
        for line in f:
            line: str = line.replace("\n", "").strip()
            
            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", maxsplit=1)

            if key.strip() == var_name.strip():
                if value.isdigit():
                    value = int(value)
                return value
        return None
