import argparse
import hashlib

from collections import defaultdict
from pathlib import Path
from .util import ask_question


def find_duplicates(folders: list[Path]) -> list[list[Path]]:
    paths_by_size = defaultdict(list)

    for folder in folders:
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

    results: list[list[Path]] = []
    for paths in paths_by_hash.values():
        if len(paths) > 1:
            results.append(paths)

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", type=Path, nargs='+', required=True, help="Folders to scan")
    parser.add_argument("-i", default=False, action="store_true", help="Interactive delete mode")
    args = parser.parse_args()

    report_and_handle_duplicates(args.folder, report_only=not args.i)

def report_and_handle_duplicates(folders: list[Path], report_only: bool) -> None:
    missing_folder = False
    for folder in folders:
        if not folder.exists():
            print("Error:", folder, "does not exist")
            missing_folder = True

    if missing_folder:
        print("Not searching for duplicates.  Try again with folders that exist")
        return

    duplicates = find_duplicates(folders)
    paths_to_delete: list[Path] = []
    for paths in duplicates:
        print("Found duplicate files")
        for path in paths:
            print("- ", path)

        if not report_only:
            for path in paths:
                keep = ask_question(f"Keep {path}?", default=True)
                if not keep:
                    paths_to_delete.append(path)

    if paths_to_delete:
        print("Paths to be deleted")
        for path in sorted(paths_to_delete):
            print("-", path)

        delete = ask_question("Permanently delete?", default=False)
        if delete:
            for path in paths_to_delete:
                path.unlink()

if __name__ == "__main__":
    main()
