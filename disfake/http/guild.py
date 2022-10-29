from __future__ import annotations

from typing import Any

from discord_typings import (
    GuildData,
)
from disfake.core.snowflake import Snowflake

from disfake.core.generator import generate as _generate
from disfake.core import cache
from disfake.http import user


def _fill(guild: GuildData, snowflake: Snowflake) -> None:
    owner = user.generate(snowflake)
    cache.users.add(owner)
    guild["owner_id"] = owner["id"]


def generate(snowflake: Snowflake, **kwargs: Any) -> GuildData:
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
    _fill(guild, snowflake)
    guild.update(kwargs)  # type: ignore
    return guild
