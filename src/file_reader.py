# file_reader.py

import yaml


def load_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def load_shader_tpl(shader_tpl):
    with open(shader_tpl, "r") as file:
        template = file.read()
    return template
