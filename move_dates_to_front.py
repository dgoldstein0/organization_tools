import argparse
import re

from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()

    print(f"Searching for files with dates in the names within {args.folder}")
    for dirpath, dirnames, filenames in args.folder.walk():
        for fname in filenames:
            m = re.search(r"^(.*?)(\d\d\d\d-\d\d-\d\d)(.*?)(\.\S+)?$", fname)
            if m:
                first, date, second, ext = m.groups(2)
                new_name = re.sub(r"\s+", " ", f"{date} {first.strip()} {second.strip()}").strip() + ext

                if fname != new_name:
                    rename = False
                    while (True):
                        confirm = input(f"[{dirpath.relative_to(args.folder)}] rename '{fname}' to '{new_name}'? [Y/n]:")
                        if confirm in ("y", "Y", ""):
                            rename = True
                            break
                        elif confirm in ("n", "N"):
                            rename = False
                            break

                    if rename:
                        (dirpath / fname).rename(dirpath / new_name)



if __name__ == "__main__":
    main()
