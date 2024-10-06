import argparse
import re

from pathlib import Path

def make_new_name(filename: str) -> str:
    m = re.search(r"^(.*?)(\d\d\d\d-\d\d-\d\d)(.*?)(\.\S+)?$", filename)
    if m:
        first, date, second, ext = m.groups(2)
        # basic idea is to move the date to the front, keep the other parts, but strip out extra spaces
        # as well as - or _ on the boundaries of our parts - i.e. " -foo" should be " foo" but
        # " - foo" should be left as is
        return re.sub(r"\s+", " ", f"{date} {first.strip('-_ ')} {second.strip('-_ ')}").strip('-_ ') + ext

    return filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()

    print(f"Searching for files with dates in the names within {args.folder}")
    for dirpath, dirnames, filenames in args.folder.walk():
        for fname in filenames:

            new_name = make_new_name(fname)
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
