# disfake

![code style black](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge)
![coverage](https://img.shields.io/coveralls/github/teaishealthy/disfake?style=for-the-badge)

Module to assist in creating fake discord objects for testing purposes.

```python
from disfake.core.cache import users
from disfake.http import guild
from discord_typings import GuildData, UserData


my_guild: GuildData = guild.generate()
owner: UserData = users.get(my_guild["owner_id"])
```
