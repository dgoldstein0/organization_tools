import yaml
from pathlib import Path
from typing import Mapping, Protocol

from .move_dates_to_front import move_dates_to_front
from .find_duplicates import report_and_handle_duplicates
from .find_misorganized_files import find_dated_files_in_wrong_year_folder
from .find_files_with_no_extensions import find_files_with_no_extensions

# each of these functions takes a folder as an argument
class OrganizePass(Protocol):
    def __call__(folder: Path) -> None:
        ...

OPS: Mapping[str, OrganizePass] = {
    "move_dates_to_front": move_dates_to_front,
    # TODO: find duplicates can operate across multiple folders, but right now the config doesn't expose that ability
    "find_duplicates": lambda f: report_and_handle_duplicates([f], report_only=False),
    "find_dated_files_in_wrong_year_folder": find_dated_files_in_wrong_year_folder,
    "find_files_with_no_extensions": find_files_with_no_extensions,
}

def main() -> None:

    # TODO instead of a config in homedir, would it make sense to expect configs
    # within individual folders? we already support .organizerc.json for marking files as permanent skips in various passes
    config_file_path = Path("~/.organizerc.yaml").expanduser()
    with open(config_file_path, "r") as f:
        settings = yaml.safe_load(f)

    # validate config before doing any operations
    # TODO: maybe consider pydantic for this?
    for path, operations in settings["paths"].items():
        for operation in operations:
            if operation not in OPS:
                raise ValueError(f"Invalid Operation {operation} for path {path} specified in {config_file_path}")

    # do all the operations.
    for path, operations in settings["paths"].items():
        for operation in operations:
            OPS[operation](Path(path).expanduser())



if __name__ == "__main__":
    main()
