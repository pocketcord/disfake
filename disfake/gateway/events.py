from discord_typings import (
    HeartbeatACKEvent,
    HeartbeatCommand,
    HelloEvent,
    InvalidSessionEvent,
    ReadyEvent,
    ReconnectEvent,
    ResumedEvent,
    UserData,
)

from ..core.generator import generate

__all__ = (
    "hello",
    "heartbeat_command",
    "heartbeat_ack",
    "ready",
    "invalid_session",
    "reconnect",
    "resumed",
)


def hello() -> HelloEvent:
    base = generate(HelloEvent)
    base["d"]["heartbeat_interval"] = 1000
    return base


def heartbeat_command() -> HeartbeatCommand:
    return generate(HeartbeatCommand)


def heartbeat_ack() -> HeartbeatACKEvent:
    return generate(HeartbeatACKEvent)


def ready(user: UserData) -> ReadyEvent:
    ready_data = generate(ReadyEvent)
    ready_data["d"]["user"] = user
    ready_data["d"]["application"]["id"] = user["id"]
    return ready_data


def invalid_session() -> InvalidSessionEvent:
    return generate(InvalidSessionEvent)


def reconnect() -> ReconnectEvent:
    return generate(ReconnectEvent)


def resumed() -> ResumedEvent:
    return generate(ResumedEvent)
