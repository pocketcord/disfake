HTTP
===============

.. module:: disfake.http

.. function:: user.generate(snowflake: Snowflake = cache.snowflake, **kwargs: Dict[str, Any])

    Generates a user object.

    :param snowflake: Snowflake Generator to use.
    :param kwargs: Additional keyword arguments to pass to the user object.
    :return: The generated user object.


.. function:: guild.generate(snowflake: Snowflake = cache.snowflake, member_count: int = 0, emoji_count: int = 0, role_count: int = 0, **kwargs: Dict[str, Any])

    Generates a guild object.

    .. warning:: The guild object will not contain members. See :func:`~disfake.gateway.promotors.promote_guild` for more information.

    :param snowflake: Snowflake generator to use. Defaults to the global snowflake generator. See :attr:`~disfake.core.cache.snowflake` for more information.
    :param member_count: Number of members to generate.
    :param emoji_count: Number of emojis to generate.
    :param role_count: Number of roles to generate.
    :param kwargs: Additional keyword arguments to pass to the guild object.
    :return: The generated guild object.
