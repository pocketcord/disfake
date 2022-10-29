from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
from discord_typings import UserData


@dataclass(frozen=True)
class Key:
    guild_id: Optional[str]
    user_id: Optional[str]


class UserCache(Dict[Key, UserData]):
    def add(self, user: UserData):
        key = Key(None, user["id"])
        self[key] = user

    def get(self, user_id: str) -> Optional[UserData]:
        key = Key(None, user_id)
        return super().get(key)


users = UserCache()
members: Dict[Key, UserData] = {}
