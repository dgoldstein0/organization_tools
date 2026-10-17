import argparse
import re

from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()

    find_dated_files_in_wrong_year_folder(args.folder)

def find_dated_files_in_wrong_year_folder(folder: Path) -> None:
    print(f"Searching for files with dates in the names within {folder}")

    for dirpath, dirnames, filenames in folder.walk():
        folder_year = None
        for p in reversed(dirpath.parts):
            if re.match(r"^(19|20)\d\d$", p):
                folder_year = int(p)

        if folder_year is not None:
            for fname in filenames:
                m = re.match(r"^(\d{4})-\d\d-\d\d\s", fname)
                if m is not None:
                    file_year = int(m.group(1))
                    if folder_year != file_year:
                        print(f"Found potentially misfiled file: {dirpath/fname}")


if __name__ == "__main__":
    main()
