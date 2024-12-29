import argparse
import hashlib

from collections import defaultdict
from pathlib import Path


def find_duplicates(folder: Path):
    paths_by_size = defaultdict(list)

    for dirpath, dirnames, filenames in folder.walk():
        for fname in filenames:
            fpath = dirpath / fname
            paths_by_size[fpath.stat().st_size].append(fpath)


    paths_by_hash = defaultdict(list)
    for paths in paths_by_size.values():
        if len(paths) > 1:
            for fpath in paths:
                with open(fpath, "rb") as f:
                    digest = hashlib.file_digest(f, "sha256")
                paths_by_hash[digest.hexdigest()].append(fpath)

    for paths in paths_by_hash.values():
        if len(paths) > 1:
            print("Found duplicate files")
            for path in paths:
                print("- ", path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path)
    args = parser.parse_args()

    find_duplicates(args.folder)


if __name__ == "__main__":
    main()
