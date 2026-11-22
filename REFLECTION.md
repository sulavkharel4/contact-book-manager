# Reflection - Contact Book Manager
Sulav Kharel (SM20252552)

**Program overview.** My program is a menu-driven Contact Book. It loads contacts from `data/contacts.csv`, lets the user add, view, search (by name, phone or email), update, delete and filter by group, detect duplicate phone numbers, and print a summary report (total, contacts per group, contacts without an email). Everything is saved back to the CSV on exit. Every prompt loops until the input is valid, so bad input does not crash it.

**Design choices.** I split the code by responsibility. `manager.py` holds the `ContactBook` class and never calls `input()` or `print()`, so I could test it directly. `validation.py` keeps pure checkers separate from prompt functions, `storage.py` handles the CSV, and `main.py` only runs the menu. The recursive function is `count_without_email` in `reports.py`. It splits the list in half, counts each half and adds the results, with base cases for an empty list and a single contact. I chose halving because its depth is about log2(n), so a large address book cannot hit Python's recursion limit. Totals use my own loops, as FR8 requires. Duplicate phones are compared by digits only, so "0412 345 678" and "0412345678" match.

**Testing results.** I wrote 29 unit tests covering normal, boundary and error cases, such as phones of 7, 8, 15 and 16 digits, malformed emails, unknown IDs, a missing CSV and corrupted CSV rows. All 29 pass (see `TEST_PLAN.md`). Testing exposed one real defect: formatted phone numbers were not detected as duplicates until I added digit-only comparison. I also tested the full program by hand, including closing input early, which saves and exits cleanly.

**Potential improvements.**
- Normalise international numbers (e.g. +61 and 0 prefixes) so they count as duplicates.
- Add sorting of contacts by name.
- Keep a backup copy of the CSV before saving.
- Add a graphical interface.
- Use GitHub Actions to run the tests on every commit.

**Personal reflection.**
The hardest part in this project for me was to setup git and github for the first time. After trying multiple times and searching it online I finally found out how to do it. Running the program made me realize how input validation matters.

**Acknowledgement of assistance.**  I used Claude (an AI assistant by Anthropic) to brainstorm ideas.
