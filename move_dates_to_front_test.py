
from move_dates_to_front import make_new_name

# simple case: date goes from end to front
assert make_new_name("foo 1234-03-12.pdf") == "1234-03-12 foo.pdf"

# harder case: date goes from middle to front.  no extra spaces.
assert make_new_name('ADP Workforce Now dgoldstein Statements 2022-11-17 q4 rsus.pdf') == '2022-11-17 ADP Workforce Now dgoldstein Statements q4 rsus.pdf'

# nothing to do - notably, leave the " - " alone
assert make_new_name('2024-04-30 Pay Date 02 - perks.pdf') == '2024-04-30 Pay Date 02 - perks.pdf'

# rearrange but don't leave the underscore
assert make_new_name("eStmt_2024-01-17.pdf") == "2024-01-17 eStmt.pdf"
