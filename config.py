import json


DEFAULT_CONFIG_PATH = "config.json"


def read_config(config_file=DEFAULT_CONFIG_PATH):
    with open(config_file) as f:
        return json.loads(f.read())

