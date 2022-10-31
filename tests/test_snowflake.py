from datetime import datetime

from freezegun import freeze_time

from disfake.core.cache import snowflake
from disfake.core.snowflake import to_datetime

now = datetime.now()

# snowflake -> unix timestamp
FLAKES = {
    1036758709298003968: 1667252938,
    1036759128728403969: 1667253038,
    1036759548158803970: 1667253138,
    1036759967589203971: 1667253238,
    1036760387019603972: 1667253338,
    1036760806450003973: 1667253438,
    1036761225880403974: 1667253538,
    1036761645310803975: 1667253638,
    1036762064741203976: 1667253738,
    1036762484171603977: 1667253838,
}


def test_generator() -> None:
    assert snowflake.hash(1234)
    assert snowflake.bool() in (True, False)


def test_snowflake() -> None:
    flake = snowflake.snowflake()
    assert flake, "Snowflake is empty"


def test_to_datetime() -> None:
    for flake, ts in FLAKES.items():
        assert int(to_datetime(flake).timestamp()) == ts


def test_snowflake_accurate() -> None:
    flake = snowflake.snowflake()
    assert int(to_datetime(flake).timestamp()) == int(
        now.timestamp()
    ), "Snowflake is not accurate. Make sure test_to_datetime passes"
