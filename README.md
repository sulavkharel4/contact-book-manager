# Contact Book Manager (Project F)
**Student:** Sulav Kharel (SM20252552)

A modular, menu-driven Python console application for managing contacts
(ID, name, phone, email, group). Records are loaded from `data/contacts.csv` at
start-up and saved on exit.

## Requirements
- Python 3.8 or newer (tested on 3.12)
- No third-party packages. There is nothing to install or build.

## How to run
1. Unzip the submission and open a terminal in the unzipped folder (the one containing `main.py`).
2. Start the program:
   ```
   python main.py
   ```
   (use `python3 main.py` if `python` is not found, e.g. on Linux/macOS).
3. Choose options 1-9 from the menu. Option 9 saves the data and exits.

The sample file `data/contacts.csv` has 10 records, so the program can be used immediately.
If the file is missing, the program creates a new empty one on first run.

## How to run the tests
```
python -m unittest discover -s tests -v
```
Expected: `Ran 29 tests ... OK`. Test cases and results are described in `TEST_PLAN.md` and `Report.docx`.

## Menu
| # | Option |
|---|---|
| 1 | Add a contact |
| 2 | View all contacts |
| 3 | Search (by name, phone or email; case-insensitive) |
| 4 | Update a contact |
| 5 | Delete a contact (asks Y/N) |
| 6 | Filter by group (Family / Friends / Work) |
| 7 | Detect duplicate phone numbers |
| 8 | Summary report |
| 9 | Exit (saves data) |

## Project structure
| File | Responsibility |
|---|---|
| main.py | Menu loop and menu handlers |
| validation.py | Field checkers and re-prompting input functions |
| contact.py | `Contact` record, phone normalisation |
| manager.py | `ContactBook`: add, find, search, update, delete, filter, duplicates (no input/print) |
| reports.py | Summary report and the recursive function `count_without_email` |
| storage.py | CSV load/save using the csv module |
| display.py | Table and report formatting |
| data/contacts.csv | Sample data (10 records) |
| tests/test_contacts.py | 29 unit tests |
| Report.docx | Report: design choices, test cases/results, screenshots, Git log |
| REFLECTION.md | Reflection (max 500 words) |
