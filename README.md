A few different organizational tools for keeping my files straight; each of these can be run with `uv run`

- find_duplicates.py: python script for finding duplicate files.
- find_misorganized_files.py - find files that are in the wrong place in the folder hierarchy, based on the dates in the filenames and folder hierarchy.  Currently does not try to rectify; most findings have been mislabeled files rather than files in the wrong folders.
- move_dates_to_front.py - renames files based on finding dates in their names and moving the date to the front of the filename.
- create_new_yearly_folders.py - finds folders with subfolders of last year or the year before, and offers to create a folder for the current year

The main entry point however is `uv run organize`, which looks at a the yaml config `~/.organizerc.yaml` and runs the operations specified there on the specified folders.

Config format:
```yaml
paths:
  folder1:
    - op1
    - op2
  folder2:
    - op3

```

# Dependencies

Developed with python 3.12.7 running under git-bash, and uv for package management (currently 0.13.0)

# Testing

`python move_dates_to_front_test.py` - if no output, the test passes.
