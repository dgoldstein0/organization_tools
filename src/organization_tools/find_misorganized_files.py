import argparse
import re

from datetime import datetime
from pathlib import Path

from .util import ask_question

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
                m = re.match(r"^((\d{4})-\d\d-\d\d)\s", fname)
                if m is not None:
                    file_year = int(m.group(2))
                    if folder_year != file_year:
                        print(f"Found potentially misfiled file: {dirpath/fname}")
                        file_date = datetime.strptime(m.group(1), "%Y-%m-%d")
                        now = datetime.now() # should we use the file mtime instead?
                        if file_date > now:
                            if file_date.year > now.year:
                                proposed_date = file_date.replace(year = now.year)
                                if proposed_date < now:
                                    new_name = fname.replace(file_date.strftime("%Y-%m-%d"), proposed_date.strftime("%Y-%m-%d"))
                                    if ask_question(f"File date is in a future year; was this year meant? If so rename to {new_name}?", default=False):
                                        (dirpath / fname) .rename(dirpath / new_name)



if __name__ == "__main__":
    main()
