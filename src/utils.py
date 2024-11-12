# utils.py

import sys

import yaml


def load_config(config_file):
    # Load the configuration
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def load_shader_tpl(shader_tpl):
    # Load the shader template
    with open(shader_tpl, "r") as file:
        template = file.read()
    return template


def get_config_path(default="config.yaml"):
    # Retrieve the configuration file
    if len(sys.argv) > 1:
        print(f"Using custom config file {sys.argv[1]}")
        config_path = sys.argv[1]
    else:
        config_path = default

    return config_path
