# MIT License
#
# Copyright (c) 2022 Ignacio Vizzo, Tiziano Guadagnino, Benedikt Mersch, Cyrill
# Stachniss.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# NOTE: This module was contributed by Markus Pielmeier on PR #63
from __future__ import annotations

import importlib
import sys

from pathlib import Path
from typing import Any, Dict, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from mapmos.config.config import (
    DataConfig,
    OdometryConfig,
    MOSConfig,
    TrainingConfig,
)


class MapMOSConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="mapmos_")
    out_dir: str = "results"
    data: DataConfig = DataConfig()
    odometry: OdometryConfig = OdometryConfig()
    mos: MOSConfig = MOSConfig()
    training: TrainingConfig = TrainingConfig()


def _yaml_source(config_file: Optional[Path]) -> Dict[str, Any]:
    data = None
    if config_file is not None:
        try:
            yaml = importlib.import_module("yaml")
        except ModuleNotFoundError:
            print(
                "Custom configuration file specified but PyYAML is not installed on your system,"
                ' run `pip install "kiss-icp[all]"`. You can also modify the config.py if your '
                "system does not support PyYaml "
            )
            sys.exit(1)
        with open(config_file) as cfg_file:
            data = yaml.safe_load(cfg_file)
    return data or {}


def load_config(config_file: Optional[Path]) -> MapMOSConfig:
    """Load configuration from an Optional yaml file."""
    config = MapMOSConfig(**_yaml_source(config_file))
    return config


def write_config(config: MapMOSConfig, filename: str):
    with open(filename, "w") as outfile:
        try:
            yaml = importlib.import_module("yaml")
            yaml.dump(config.model_dump(), outfile, default_flow_style=False)
        except ModuleNotFoundError:
            outfile.write(str(config.model_dump()))
