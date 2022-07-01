from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any, List, Type, TypeVar

from discord_typings import ChannelData, GuildData, GuildMemberData, TextChannelData
from discord_typings.shared import Snowflake

from disfake.user import User

from .base import MISSING, Base

if TYPE_CHECKING:
    from .state import State


T = TypeVar("T", bound=ChannelData)


class Guild(Base):
    def __init__(self, state: State, sparse: bool = True) -> None:
        super().__init__(state, sparse)
        self.channels: List[ChannelData] = []

    def _generate_channel(self, channel_type: Type[T]) -> T:
        channel = super()._generate(channel_type)
        if channel.get("name") is not None:
            channel["id"] = str(self.state.snowflake(10))
            channel["name"] = f"Channel {channel['id']}"  # type: ignore
        return channel

    def _generate_field(self, key: str, value: Any):
        if value is Snowflake:
            return str(self.state.snowflake())

        if key.endswith("channel_id"):
            if not self.state.bool():
                if self._optional(value):
                    return None
                elif self._not_required(value):
                    return MISSING

            channel = self._generate_channel(TextChannelData)
            self.channels.append(channel)
            return channel["id"]

        return super()._generate_field(key, value)

    def generate(self, **kwargs: Any) -> GuildData:
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
        self.channels = []
        guild = self._generate(GuildData)
        members: List[GuildMemberData] = []
        user = User(self.state)
        for _ in range(10):
            member = super()._generate(GuildMemberData)
            member["user"] = user.generate()
            members.append(member)

        id_ = str(self.state.snowflake())
        guild["id"] = id_
        guild["name"] = f"Guild {id_}"
        guild["owner_id"] = random.choice(members)["user"]["id"]  # type: ignore
        guild.update(kwargs)  # type: ignore

        self.state.guilds.append(guild)
        self.state.channels[id_].extend(self.channels)
        self.state.members[id_].extend(members)

        return guild
