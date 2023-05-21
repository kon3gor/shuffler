import datetime
import toml
from config import Config


def get_current_date():
    return datetime.datetime.now(tz=datetime.timezone.utc)


def get_config() -> Config:
    with open("config.toml", "r") as file:
        content = toml.load(file)

    return Config.from_dict(content)
