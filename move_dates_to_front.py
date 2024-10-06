import argparse
import re

from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()

    for f in args.folder.iterdir():
        m = re.search(r"^(.*?)(\d\d\d\d-\d\d-\d\d)(.*?)(\.\S+)?$", f.name)
        if m:
            first, date, second, ext = m.groups(2)
            new_name = re.sub(r"\s+", " ", f"{date} {first.strip()} {second.strip()}").strip() + ext

            if f.name != new_name:
                rename = False
                while (True):
                    confirm = input(f"Rename '{f.name}' to '{new_name}'? [Y/n]:")
                    if confirm in ("y", "Y", ""):
                        rename = True
                        break
                    elif confirm in ("n", "N"):
                        rename = False
                        break

                if rename:
                    f.rename(args.folder / new_name)



if __name__ == "__main__":
    main()
