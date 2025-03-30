import argparse
import re

from pathlib import Path

from config import get_config_for_folder, write_config_for_folder
from util import ask_question

CONFIG_SECTION = "move_dates"

def make_new_name(filename: str) -> str:
    # if there are multiple dates in the filename, give up for now.  May revisit this case later, but often
    # we'll either need to ask the user which to use and both may be wrong for the current organization (e.g.
    # often these are a service period when I use the statement date in the filename)
    if len(list(re.finditer(r"\d\d\d\d-\d\d-\d\d", filename))) >= 2:
        return filename

    m = re.search(r"^(.*?)(\d\d\d\d-\d\d-\d\d)(.*?)((?:\.\S+)?)$", filename)
    if m:
        first, date, second, ext = m.groups()

        # smell test: most dates should be 19xx or 20xx, otherwise we didn't match a date.
        # TODO: we could also check the range of the months
        if date[:2] not in ("19", "20"):
            return filename

        # basic idea is to move the date to the front, keep the other parts, but strip out extra spaces
        # as well as - or _ on the boundaries of our parts - i.e. " -foo" should be " foo" but
        # " - foo" should be left as is
        return re.sub(r"\s+", " ", f"{date} {first.strip('-_ ')} {second.strip('-_ ')}").strip('-_ ') + ext

    # this is the format that Dropbox's "upload a new photo" uses for it's file naming.
    m = re.match(r"^IMG_(\d{4})(\d\d)(\d\d)_(\d{6}).jpg$", filename)
    if m:
        year, month, day, time = m.groups()

        # smell test: most dates should be 19xx or 20xx, otherwise we didn't match a date.
        # TODO: we could also check the range of the months
        if year[:2] not in ("19", "20"):
            return filename

        return f"{year}-{month}-{day} {time}.jpg"

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    short_months =  [m[:3] for m in months]
    all_months = months + short_months + [m.lower() for m in months] + [m.lower() for m in short_months] + [m.upper() for m in months] + [m.upper() for m in short_months]
    # TODO add case differences
    months_re = "|".join(all_months)
    m = re.search(rf"^(.*?)[-_ ]?({months_re})[-_ ]?(\d\d\d\d)(.*)$", filename)
    if m:
        first, month_str, year, second = m.groups()

        if re.match(r"^\d", second):
            return filename

        second = second.strip("-_ ")

        # smell test: most dates should be 19xx or 20xx, otherwise we didn't match a date.
        if year[:2] not in ("19", "20"):
            return filename
        month_num = (all_months.index(month_str) % 12) + 1

        return f"{year}-{month_num:>02} {first}{second}"

    return filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()

    print(f"Searching for files with dates in the names within {args.folder}")
    for dirpath, dirnames, filenames in args.folder.walk():

        config = get_config_for_folder(dirpath, CONFIG_SECTION) or {}
        rel_dirpath = dirpath.relative_to(args.folder)

        always_skip_files = []
        for fname in filenames:
            if config.get(fname, {}).get("skip", False):
                print(f"[{rel_dirpath}] skipping {fname} because it's been marked always_skip in this folder's .organizerc.json")
                continue

            try:
                new_name = make_new_name(fname)
            except Exception as e:
                raise ValueError(f"died on {dirpath/fname}") from e

            if fname != new_name:
                rename = ask_question(f"[{rel_dirpath}] rename '{fname}' to '{new_name}'?", default=True)

                if rename:
                    (dirpath / fname).rename(dirpath / new_name)
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
