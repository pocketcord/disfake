from typing import Any, Dict

from discord_typings import UserData

from ..core.snowflake import Snowflake


def generate(snowflake: Snowflake, **kwargs: Dict[str, Any]) -> UserData:
    """Generate a fake user

    Returns
    -------
    UserData
        The generated user
    """
    id_ = str(snowflake.snowflake())
    user: UserData = {
        "id": id_,
        "username": f"User {id_}",
        "discriminator": id_[-4:],
        "avatar": None,
    }
    user.update(kwargs)  # type: ignore
    return user
