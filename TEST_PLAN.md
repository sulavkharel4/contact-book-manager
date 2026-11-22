# Test Plan and Results - Contact Book Manager
**Student:** Sulav Kharel (SM20252552)

Run all tests: `python -m unittest discover -s tests -v`
**Result: 29 tests run, 29 passed, 0 failed.**

| Area | Normal case | Boundary case | Error case | Result |
|---|---|---|---|---|
| Name (FR2, FR11) | "Al" accepted | 50 chars ok, 51 rejected | empty, spaces, digits only | Pass |
| Phone | "0412 345 678", "+61 490 123 456" | 8 digits ok, 7 rejected; 15 ok, 16 rejected | letters, "+" in middle, blank | Pass |
| Email | "a@b.co" | blank allowed | "alice", "a@b", "@x.com", "a@@b.com" | Pass |
| Group | "family", " WORK ", "2" | 1 and 3 accepted | 0, 4, -1, "colleagues" | Pass |
| Menu choice (FR1) | 9 exits | 1 and 9 limits | "", "abc", 0, 10 show message and re-show menu | Pass |
| Add (FR2) | IDs 1,2,3 assigned | ID stays unique after delete + add | invalid field raises, nothing stored | Pass |
| View (FR3) | aligned table | - | empty book shows message | Pass |
| Search (FR4) | name/phone/email, case-insensitive | partial text matches several records | no match gives message; blank text re-prompts | Pass |
| Update (FR5) | change phone, group, email | blank email removes it | invalid value rejected, old value kept; unknown ID | Pass |
| Delete (FR6) | Y removes | N keeps record | unknown / non-numeric ID re-prompts; blank cancels | Pass |
| Filter by group (FR7) | Work, Family | group with no members | - | Pass |
| Duplicates (FR7) | "0412 345 678" = "0412345678" | no duplicates gives message | - | Pass |
| Summary + recursion (FR8, FR10) | total, per group, no-email count | empty list, 1 item | recursive count equals loop count for sizes 0,1,2,3,7,50,5000 | Pass |
| CSV (FR9) | save then load round-trip | blank email and leading zero kept | missing file created; malformed, duplicate-ID and invalid rows skipped with warning | Pass |
| Exit (FR12) | saves, prints goodbye | - | Ctrl+C / end of input still saves and exits cleanly | Pass |

## Defects found and fixed during testing
1. The first version of the "input ends" test used an empty mock list, which raised `StopIteration`
   instead of `EOFError`. The test was wrong, not the program; it now raises `EOFError` as a real
   closed terminal would.
2. Phone numbers such as "0412 345 678" and "0412345678" were not treated as duplicates. Fixed by
   comparing digits only (`normalise_phone`).
