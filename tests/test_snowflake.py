from disfake.core.cache import snowflake


def test_generator():
    assert snowflake.hash(1234)
    assert snowflake.bool() in (True, False)
