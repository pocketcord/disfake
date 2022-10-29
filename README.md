# disfake

![code style black](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge)
![coverage](https://img.shields.io/coveralls/github/teaishealthy/disfake?style=for-the-badge)

Module to assist in creating fake discord objects for testing purposes.

```python
from disfake.core.cache import users
from disfake.core.snowflake import Snowflake
from disfake.http import user, guild


snowflake = Snowflake(worker=0, process=0)

u = user.generate(snowflake)
g = guild.generate(snowflake)

print(users.get(g["owner_id"]))
# {'id': '1036055620609900545', 'username': 'User 1036055620609900545', 'discriminator': '0545', 'avatar': None}

```