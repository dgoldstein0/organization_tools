
from move_dates_to_front import make_new_name

def check_name(input_name: str, expected_output_name: str) -> None:
    assert make_new_name(input_name) == expected_output_name, f"make_new_name('{input_name}') is '{make_new_name(input_name)}' not '{expected_output_name}'"

# simple case: date goes from end to front
assert make_new_name("foo 2034-03-12.pdf") == "2034-03-12 foo.pdf"

# harder case: date goes from middle to front.  no extra spaces.
assert make_new_name('ADP Workforce Now dgoldstein Statements 2022-11-17 q4 rsus.pdf') == '2022-11-17 ADP Workforce Now dgoldstein Statements q4 rsus.pdf'

# nothing to do - notably, leave the " - " alone
assert make_new_name('2024-04-30 Pay Date 02 - perks.pdf') == '2024-04-30 Pay Date 02 - perks.pdf'

# rearrange but don't leave the underscore
assert make_new_name("eStmt_2024-01-17.pdf") == "2024-01-17 eStmt.pdf"

# skip this case for now, definitely don't extract the wrong date
assert make_new_name("Superbill20221201-16-129h7n7.pdf") == "Superbill20221201-16-129h7n7.pdf"

# skip the multi-date case for now
assert make_new_name("2022-05-22-to-2022-06-21-comcast-mobile.pdf") == "2022-05-22-to-2022-06-21-comcast-mobile.pdf"

# doesn't die if there's no extension
assert make_new_name("2023-12-29 mytherapy donation Gmail - Your Google Play Order Receipt") == "2023-12-29 mytherapy donation Gmail - Your Google Play Order Receipt"

# handles Dropbox photo naming
assert make_new_name("IMG_20241225_000605.jpg") == "2024-12-25 000605.jpg"

# handles paypal naming
check_name("statement-Jan-2025.pdf", "2025-01 statement.pdf")
check_name("statement-Dec-2021.pdf", "2021-12 statement.pdf")

# handles old BoA naming
check_name("December2013_4422.csv", "2013-12 4422.csv")

# is idempotent
for input_name in [
    'foo 2034-03-12.pdf',
    'ADP Workforce Now dgoldstein Statements 2022-11-17 q4 rsus.pdf',
    '2024-04-30 Pay Date 02 - perks.pdf',
    "eStmt_2024-01-17.pdf",
    "Superbill20221201-16-129h7n7.pdf",
    "2022-05-22-to-2022-06-21-comcast-mobile.pdf",
    "2023-12-29 mytherapy donation Gmail - Your Google Play Order Receipt",
    "IMG_20241225_000605.jpg",
    "2025-01 statement.pdf",
]:
    assert make_new_name(make_new_name(input_name)) == make_new_name(input_name)
