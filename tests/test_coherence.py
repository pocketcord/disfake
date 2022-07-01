from typing import Tuple

import pytest
from discord_typings import GuildData

import disfake


@pytest.fixture
def state_guild():
    state = disfake.State(0, 0)
    return state, disfake.Guild(state).generate()


def test_owner_coherence(state_guild: Tuple[disfake.State, GuildData]):
    state, guild = state_guild
    members = state.members[guild["id"]]
    assert any(
        member["user"]["id"] == guild["owner_id"] for member in members
    ), "Owner not found in members"


def test_member_coherence(state_guild: Tuple[disfake.State, GuildData]):
    state, guild = state_guild
    members = state.members[guild["id"]]
    for member in members:
        assert int(member["user"]["id"]) < int(
            guild["id"]
        ), "Member is newer than guild"


def test_channel_coherence(state_guild: Tuple[disfake.State, GuildData]):
    state, guild = state_guild
    channels = state.channels[guild["id"]]
    for channel in channels:
        assert int(channel["id"]) > int(guild["id"]), "Channel is older than guild"
