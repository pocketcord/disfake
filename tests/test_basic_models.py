from typing import Tuple

import pytest
import typeguard
from discord_typings import GuildData, UserData
from typing_extensions import NotRequired, get_origin, is_typeddict

import disfake
from disfake.base import _get_type_hints


def _check(
    name,
    obj,
    data,
):
    typehints = _get_type_hints(obj)
    for key, value in typehints.items():
        if is_typeddict(value):
            _check(f"{name}.{key}", value, data[key])

        if get_origin(value) is not NotRequired:
            assert key in data
            typeguard.check_type(f"{name}:{key}", data[key], value)


@pytest.fixture
def state():
    return disfake.State(0, 0)


def test_user(state: disfake.State):
    user = disfake.User(state)
    _check("User", UserData, user.generate())


def test_guild(state: disfake.State):
    guild = disfake.Guild(state)
    _check("Guild", GuildData, guild.generate())
