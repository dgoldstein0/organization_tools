A few different organizational tools for keeping my files straight.

- find_duplicates.ps1: powershell script for finding duplicate files.  Invoke via `powershell -executionpolicy bypass -File C:\Users\David\Dropbox\code\organization_tools\find_duplicates.ps1` in the folder to organize.  Recursive.
- move_dates_to_front.py - renames files based on finding dates in their names and moving the date to the front of the filename.

Probably should ditch powershell here.

# Dependencies

Developed with python 3.12.7 running under git-bash

# Testing

`python move_dates_to_front_test.py` - if no output, the test passes.
