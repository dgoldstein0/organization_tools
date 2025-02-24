import argparse
import re

from pathlib import Path

from config import get_config_for_folder, write_config_for_folder
from util import ask_question

CONFIG_SECTION = "files_without_extensions"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()

    print(f"Searching for filenames without an extension within {args.folder}")
    for dirpath, dirnames, filenames in args.folder.walk():

        config = get_config_for_folder(dirpath, CONFIG_SECTION) or {}
        rel_dirpath = dirpath.relative_to(args.folder)

        always_skip_files = []
        for fname in filenames:
            if config.get(fname, {}).get("skip", False):
                print(f"[{rel_dirpath}] skipping {fname} because it's been marked always_skip in this folder's .organizerc.json")
                continue

            ext = Path(fname).suffix
            if not ext or re.fullmatch(r"\d+", ext):
                rename = ask_question(f"[{rel_dirpath}] rename '{fname}' to '{fname}.pdf'?", default=True)

                if rename:
                    (dirpath / fname).rename(dirpath / (fname + ".pdf"))
                else:
                    always_skip = ask_question(f"[{rel_dirpath}] always skip renaming '{fname}'?", default=False)

                    if always_skip:
                        always_skip_files.append(fname)

        if always_skip_files:
            new_config = (config or {}).copy()
            for fname in always_skip_files:
                new_config[fname] = {"skip": True}

            write_config_for_folder(dirpath, CONFIG_SECTION, new_config)



if __name__ == "__main__":
    main()
