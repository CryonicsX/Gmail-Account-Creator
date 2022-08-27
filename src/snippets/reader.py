import yaml

from os.path import exists

from typing import TypedDict, List
from typeguard import check_type


class ConfigSchema(TypedDict):
    browser_thread: int
    use_proxy: bool
    proxy_protocol: str
    account_count: int
    api_key: str


class Reader:
    def __init__(self):
        self.config = None

    def read(self):
        if not exists('./config/config.yaml'):
            return [False, "Can't find config folder."]

        try:
            with open("./config/config.yaml", "r") as stream:
                try:
                    self.config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError:
            return [False, "Can't find config.yaml"]

        try:
            check_type("data", self.config['settings'], ConfigSchema)
            self.config = self.config['settings']
        except:
            return [False, "Check your config file for values."]

        return [True, self.config]
