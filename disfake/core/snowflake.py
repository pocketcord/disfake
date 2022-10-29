import hashlib
import random
from datetime import datetime
from typing import List, Optional, TypeVar, Union

T = TypeVar("T")


class Snowflake:
    def __init__(self, worker: Union[int, str], process: Union[int, str]) -> None:

        # Result cache
        self.snowflakes: List[int] = []

        self.worker: str = str(worker).zfill(5)
        self.process: str = str(process).zfill(5)
        self._now: Optional[float] = None

    def hash(self, value: int, /) -> str:
        """Generate a discord cdn like hash from an integer

        Parameters
        ----------
        value : int
            The value to hash

        Returns
        -------
        str
            The hash
        """
        return hashlib.sha1(str(value).encode("utf-8")).hexdigest()

    def snowflake(self, offset: int = 0) -> int:
        """Generate a snowflake from the current time

        Returns
        -------
        int
            The snowflake generated
        """
        now = (self._now or datetime.now().timestamp()) + (offset)

        # Cursed black magic
        # Ref: https://discord.dev/reference#snowflakes
        timestamp = bin((int(now * 1000) - 1420070400000) << 22)[2:40].zfill(42)
        increment = bin(len(self.snowflakes))[2:].rjust(12, "0")

        snowflake = int(timestamp + self.worker + self.process + increment, 2)
        self.snowflakes.append(snowflake)
        return snowflake

    def bool(self) -> bool:
        """Generate a random boolean

        Returns
        -------
        bool
            The boolean generated
        """
        return random.choice([True, False])


__all__ = ("Snowflake",)
