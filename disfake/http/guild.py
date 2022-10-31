from __future__ import annotations

from datetime import timedelta
from typing import Any

from discord_typings import GuildData, GuildMemberData, RoleData, UserData

from disfake.core import cache
from disfake.core.generator import generate as _generate
from disfake.core.snowflake import Snowflake, to_datetime
from disfake.http import user


def _promote_to_member(u: UserData, guild_id: str) -> GuildMemberData:
    created_at = to_datetime(int(u["id"]))
    joined_at = created_at + timedelta(days=1)
    return {
        "user": u,
        "nick": None,
        "avatar": None,
        "roles": [guild_id],
        "joined_at": joined_at.isoformat() + "Z",
        "deaf": False,
        "mute": False,
        "pending": False,
    }


def _fill(
    guild: GuildData, member_count: int, emoji_count: int, *, snowflake: Snowflake
) -> None:
    guild["id"] = str(snowflake.snowflake())
    guild["name"] = f"Guild {guild['id']}"

    _fill_roles(guild, snowflake=snowflake)
    _fill_members(guild, member_count, snowflake=snowflake)
    _fill_emojis(guild, emoji_count, snowflake=snowflake)


def _fill_members(guild: GuildData, member_count: int, *, snowflake: Snowflake) -> None:
    owner = user.generate(snowflake)
    cache.users.add(owner)
    guild["owner_id"] = owner["id"]

    cache.members.add(guild["id"], _promote_to_member(owner, guild["id"]))
    for _ in range(member_count):
        member = user.generate(snowflake)
        cache.users.add(member)
        cache.members.add(guild["id"], _promote_to_member(member, guild["id"]))


def _fill_roles(guild: GuildData, *, snowflake: Snowflake) -> None:
    everyone = _generate(RoleData)
    everyone["id"] = guild["id"]
    everyone["name"] = "@everyone"
    everyone["permissions"] = "0"
    guild["roles"].append(everyone)


def _fill_emojis(guild: GuildData, emoji_count: int, *, snowflake: Snowflake) -> None:
    owner = cache.users.get(guild["owner_id"])
    assert owner is not None, "Guild owner not found"

    for _ in range(emoji_count):
        id = snowflake.snowflake()
        guild["emojis"].append(
            {
                "id": str(id),
                "name": f"emoji{id}",
                "roles": [],
                "user": owner,
                "require_colons": True,
                "managed": False,
                "animated": False,
            }
        )


def generate(
    snowflake: Snowflake = cache.snowflake,
    member_count: int = 0,
    emoji_count: int = 0,
    **kwargs: Any,
) -> GuildData:
    """Generate a fake guild

    Parameters
    ----------
    kwargs
        Additional values to be added the generated guild

    Returns
    -------
    GuildData
        The generated guild
    """
    guild = _generate(GuildData)
    _fill(guild, member_count, emoji_count, snowflake=snowflake)
    guild.update(kwargs)  # type: ignore
    return guild
