from typing import List, TypedDict

from discord_typings import (
    ChannelCreateData,
    GuildCreateData,
    GuildData,
    GuildMemberData,
    GuildScheduledEventData,
    StageInstanceData,
    ThreadChannelData,
    UpdatePresenceData,
    VoiceStateData,
)

from ..core import cache


class UniqueCreateData(TypedDict):
    joined_at: str
    large: bool
    unavailable: bool
    member_count: int
    voice_states: List[VoiceStateData]
    members: List[GuildMemberData]
    channels: List[ChannelCreateData]
    threads: List[ThreadChannelData]
    presences: List[UpdatePresenceData]
    stage_instances: List[StageInstanceData]
    guild_scheduled_events: List[GuildScheduledEventData]


def promote_guild(guild: GuildData, include_members: bool = False) -> GuildCreateData:
    data: GuildCreateData = guild.copy()  # type: ignore

    members: List[GuildMemberData] = []
    if include_members:
        members = cache.members.get(guild["id"]) or []

    unique: UniqueCreateData = {
        "joined_at": "2021-01-01T00:00:00.000000+00:00",
        "large": False,
        "unavailable": False,
        "member_count": len(members),
        "voice_states": [],
        "members": members,
        "channels": [],
        "threads": [],
        "presences": [],
        "stage_instances": [],
        "guild_scheduled_events": [],
    }

    data.update(unique)  # type: ignore
    return data
