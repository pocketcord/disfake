from typing import Any, Dict

from discord_typings import UserData

from .base import Base


class User(Base):
    def generate(self, **kwargs: Dict[str, Any]) -> UserData:
        """Generate a fake user

        Returns
        -------
        UserData
            The generated user
        """
        id_ = str(self.state.snowflake())
        user: UserData = {
            "id": id_,
            "username": f"User {id_}",
            "discriminator": id_[-4:],
            "avatar": None,
        }
        user.update(kwargs)  # type: ignore
        return user


__all__ = ("User",)
