A few different organizational tools for keeping my files straight.

- find_duplicates.py: python script for finding duplicate files.
- find_misorganized_files.py - find files that are in the wrong place in the folder hierarchy, based on the dates in the filenames and folder hierarchy.  Currently does not try to rectify; most findings have been mislabeled files rather than files in the wrong folders.
- move_dates_to_front.py - renames files based on finding dates in their names and moving the date to the front of the filename.
- create_new_yearly_folders.py - finds folders with subfolders of last year or the year before, and offers to create a folder for the current year

# Dependencies

Developed with python 3.12.7 running under git-bash

# Testing

`python move_dates_to_front_test.py` - if no output, the test passes.
