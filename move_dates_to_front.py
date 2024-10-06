import argparse
import re

from pathlib import Path

def make_new_name(filename: str) -> str:
    # if there are multiple dates in the filename, give up for now.  May revisit this case later, but often
    # we'll either need to ask the user which to use and both may be wrong for the current organization (e.g.
    # often these are a service period when I use the statement date in the filename)
    if len(list(re.finditer(r"\d\d\d\d-\d\d-\d\d", filename))) >= 2:
        return filename

    m = re.search(r"^(.*?)(\d\d\d\d-\d\d-\d\d)(.*?)((?:\.\S+)?)$", filename)
    if m:
        first, date, second, ext = m.groups(2)

        # smell test: most dates should be 19xx or 20xx, otherwise we didn't match a date.
        # TODO: we could also check the range of the months
        if date[:2] not in ("19", "20"):
            return filename

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

            try:
                new_name = make_new_name(fname)
            except Exception as e:
                raise ValueError(f"died on {dirpath/fname}") from e

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
