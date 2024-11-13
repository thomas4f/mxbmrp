# utils.py

import os
import sys
from pathlib import Path

import yaml


def get_config_path(default="config.yaml"):
    # Retrieve the configuration file.
    if len(sys.argv) > 1:
        print(f"Using custom config file {sys.argv[1]}")
        config_path = sys.argv[1]
    else:
        config_path = default

    return config_path


def load_config(config_file):
    # Load the configuration.
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def check_config(config):
    # Check the configuration.
    shader_dest_path = Path(config["shader_dest_path"])
    layer_src_path = Path(config["layer_src_path"])
    shader_src_path = Path(config["shader_src_path"])

    if not os.access(shader_dest_path, os.W_OK):
        print(f"shader_dest_path '{shader_dest_path}' does not exist/is not writable.")
        return False

    if not os.access(layer_src_path, os.R_OK):
        print(f"layer_src_path '{layer_src_path}' is not readable.")
        return False

    if not os.access(shader_src_path, os.R_OK):
        print(f"shader_src_path '{shader_src_path}' is not readable.")
        return False

    return True


def load_shader_tpl(shader_tpl):
    # Load the shader template.
    with open(shader_tpl, "r") as file:
        template = file.read()
    return template
