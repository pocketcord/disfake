from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from discord_typings import GuildMemberData, UserData

from disfake.core.snowflake import Snowflake

__all__ = ("users", "members", "snowflake")

snowflake: Snowflake = Snowflake(0, 0)  # type: Optional[Snowflake]


@dataclass(frozen=True)
class Key:
    guild_id: Optional[str]
    user_id: Optional[str]


class UserCache(Dict[Key, UserData]):
    def add(self, user: UserData) -> None:
        key = Key(None, user["id"])
        self[key] = user

    def get(self, user_id: str) -> Optional[UserData]:
        key = Key(None, user_id)
        return super().get(key)


class MemberCache(Dict[Key, List[GuildMemberData]]):
    def add(self, id: str, member: GuildMemberData) -> None:
        key = Key(id, None)
        if key not in self:
            self[key] = []
        self[key].append(member)

    def get(self, id: str) -> Optional[List[GuildMemberData]]:
        key = Key(id, None)
        return super().get(key)


users: UserCache = UserCache()
members: MemberCache = MemberCache()
