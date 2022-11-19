from disfake.gateway import events
from disfake.gateway.events import __all__ as event_names
from disfake.http import user


def test_ready() -> None:
    assert events.ready(user.generate())


def test_other() -> None:
    for event in event_names:
        if event != "ready":
            assert getattr(events, event)()
