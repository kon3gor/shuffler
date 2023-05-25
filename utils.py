import datetime
import toml
from config import Config


__CONFIG = None


def get_current_date():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def get_config() -> Config:
    global __CONFIG

    if __CONFIG is None:
        with open("config.toml", "r") as file:
            content = toml.load(file)
        __CONFIG = Config.from_dict(content)

    return __CONFIG
