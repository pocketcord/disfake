from typing import Any

import pytest
import typeguard
from discord_typings import GuildData, UserData
from typing_extensions import NotRequired, get_origin, is_typeddict

from disfake.core.generator import (
    _get_type_hints,  # pyright: ignore[reportPrivateUsage]
)
from disfake.core.snowflake import Snowflake
from disfake.http import guild, user


def _check(
    name: str,
    obj: type,
    data: Any,
) -> None:
    typehints = _get_type_hints(obj)
    for key, value in typehints.items():
        if is_typeddict(value):
            _check(f"{name}.{key}", value, data[key])
        elif get_origin(value) is list:
            for i, item in enumerate(data[key]):
                _check(f"{name}.{key}[{i}]", value.__args__[0], item)
        elif get_origin(value) is not NotRequired:
            assert key in data, f"{name}.{key} not in data"
            typeguard.check_type(f"{name}:{key}", data[key], value)  # type: ignore


@pytest.fixture
def snowflake():
    return Snowflake(0, 0)


def test_user(snowflake: Snowflake) -> None:
    _check("User", UserData, user.generate(snowflake))


def test_guild(snowflake: Snowflake) -> None:
    _check("Guild", GuildData, guild.generate(snowflake))
