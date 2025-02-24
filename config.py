import json

from pathlib import Path
from typing import Optional, Any

def get_config_for_folder(folder: Path, section: str) -> Optional[dict[str, dict[str, Any]]]:
    config_path = folder / ".organizerc.json"

    if not config_path.exists():
        return None

    with open(config_path, 'r') as f:
        return json.load(f)[section]

def write_config_for_folder(folder: Path, section: str, updated_config: dict[str, dict[str, Any]]) -> None:
    config_path = folder / ".organizerc.json"

    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    config[section] = updated_config

    with open(config_path, 'w') as f:
        json.dump(config, f)
