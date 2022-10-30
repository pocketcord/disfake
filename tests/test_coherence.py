import pytest

import disfake
import disfake.http.guild
from disfake.core import cache
from disfake.core.snowflake import Snowflake


@pytest.fixture
def snowflake():
    return Snowflake(0, 0)


@pytest.fixture
def guild(snowflake: Snowflake):
    return disfake.http.guild.generate(snowflake, member_count=1)


def test_guild_owner(guild: disfake.http.guild.GuildData) -> None:
    user = cache.users.get(guild["owner_id"])
    assert user is not None, "Guild owner not in global user cache"

    members = cache.members.get(guild["id"])
    assert members is not None, "Guild members unavailable"

    assert members[0].get("user") == user, "Guild owner not in guild members"


def test_everyone_role(guild: disfake.http.guild.GuildData) -> None:
    assert guild["roles"][0]["name"] == "@everyone", "Guild roles[0] is not @everyone"

    members = cache.members.get(guild["id"])
    assert members is not None, "Guild members unavailable"

    assert all(
        member["roles"][0] == guild["id"] for member in members
    ), "Guild members do not have @everyone role"


def test_members(guild: disfake.http.guild.GuildData) -> None:
    members = cache.members.get(guild["id"])
    assert members is not None, "Guild members unavailable"

    assert len(members) == 2, "Guild members not generated"
