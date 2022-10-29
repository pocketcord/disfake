import pytest

import disfake
from disfake.core.cache import users, Key
import disfake.http.guild
from disfake.core.snowflake import Snowflake


@pytest.fixture
def snowflake():
    return Snowflake(0, 0)


@pytest.fixture
def guild(snowflake: Snowflake):
    return disfake.http.guild.generate(snowflake)


def test_guild_owner(guild: disfake.http.guild.GuildData):
    assert Key(None, guild["owner_id"]) in users, "Guild owner not in users cache"
