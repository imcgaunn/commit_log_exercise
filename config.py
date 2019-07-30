import json


DEFAULT_CONFIG_PATH = "config.json"


def read_config(config_file=DEFAULT_CONFIG_PATH):
    config_dict = json.loads(config_file)
    return config_dict

