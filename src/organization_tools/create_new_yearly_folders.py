import argparse

from datetime import datetime
from pathlib import Path

from util import ask_question

def create_new_yearly_folders(folder: Path) -> None:

    this_year = datetime.now().year
    last_year = this_year - 1
    two_years_ago = last_year - 1

    for dirpath, dirnames, filenames in folder.walk():
        if str(last_year) in dirnames or str(two_years_ago) in dirnames:
            if str(this_year) not in dirnames:
                proposed_folder = dirpath / str(this_year)
                create = ask_question(f"Create {proposed_folder}?", default=True)

                if create:
                    proposed_folder.mkdir()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)

    args = parser.parse_args()

    create_new_yearly_folders(args.folder)

if __name__ == "__main__":
    main()
