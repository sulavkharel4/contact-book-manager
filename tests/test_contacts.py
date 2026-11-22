"""Unit tests: normal, boundary and error cases. Run: python -m unittest discover -s tests -v"""
import os, sys, tempfile, unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import validation as v
from contact import Contact
from manager import ContactBook
from reports import build_summary, count_without_email
from storage import load_contacts, save_contacts
import main


def sample_book():
    book = ContactBook()
    book.add("Alice Nguyen", "0412 345 678", "alice@example.com", "Friends")
    book.add("Bob Smith", "0423 456 789", "", "Work")
    book.add("Carol Jones", "0412345678", "carol@example.com", "Family")
    return book


class TestValidation(unittest.TestCase):
    def test_names(self):
        self.assertTrue(v.is_valid_name("Al"))
        self.assertTrue(v.is_valid_name("A" * 50))
        for bad in ["", "   ", "12345", "A" * 51]:
            self.assertFalse(v.is_valid_name(bad), bad)

    def test_phones(self):
        for good in ["0412 345 678", "+61 490 123 456", "12345678", "1" * 15, "04-1234-5678"]:
            self.assertTrue(v.is_valid_phone(good), good)
        for bad in ["", "1234567", "1" * 16, "abc12345678", "04+12345678", "0412 345 67x", "-"]:
            self.assertFalse(v.is_valid_phone(bad), bad)

    def test_emails(self):
        for good in ["", "a@b.co", "alice.n@example.com"]:
            self.assertTrue(v.is_valid_email(good), good)
        for bad in ["alice", "alice@", "@example.com", "a@b", "a b@c.com", "a@@b.com"]:
            self.assertFalse(v.is_valid_email(bad), bad)

    def test_group(self):
        self.assertEqual(v.normalise_group("family"), "Family")
        self.assertEqual(v.normalise_group(" WORK "), "Work")
        self.assertEqual(v.normalise_group("2"), "Friends")
        for bad in ["", "0", "4", "-1", "colleagues"]:
            self.assertIsNone(v.normalise_group(bad), bad)


class TestPrompts(unittest.TestCase):
    def test_phone_reprompts_until_valid(self):
        with patch("builtins.input", side_effect=["", "abc", "123", "0412 345 678"]), patch("builtins.print"):
            self.assertEqual(v.read_phone(), "0412 345 678")

    def test_choice_rejects_text_and_out_of_range(self):
        with patch("builtins.input", side_effect=["x", "", "0", "10", "-3", "3"]), patch("builtins.print"):
            self.assertEqual(v.read_choice("? ", 1, 4), 3)

    def test_yes_no(self):
        with patch("builtins.input", side_effect=["maybe", "", "Y"]), patch("builtins.print"):
            self.assertTrue(v.read_yes_no("? "))
        with patch("builtins.input", side_effect=["no"]):
            self.assertFalse(v.read_yes_no("? "))

    def test_email_blank_allowed(self):
        with patch("builtins.input", side_effect=["bad", ""]), patch("builtins.print"):
            self.assertEqual(v.read_email(), "")

    def test_existing_id_loop(self):
        book = sample_book()
        with patch("builtins.input", side_effect=["abc", "-1", "99", "2"]), patch("builtins.print"):
            self.assertEqual(main.ask_for_existing_id(book).name, "Bob Smith")
        with patch("builtins.input", side_effect=[""]):
            self.assertIsNone(main.ask_for_existing_id(book))


class TestManager(unittest.TestCase):
    def test_add_assigns_unique_ids(self):
        book = sample_book()
        ids = [c.contact_id for c in book.contacts]
        self.assertEqual(ids, [1, 2, 3])
        book.delete(2)
        book.add("Dan Cole", "0499 999 999", "", "Work")
        ids = [c.contact_id for c in book.contacts]
        self.assertEqual(len(ids), len(set(ids)))

    def test_add_invalid_raises(self):
        book = ContactBook()
        with self.assertRaises(ValueError):
            book.add("", "0412345678", "", "Work")
        with self.assertRaises(ValueError):
            book.add("Zed", "123", "", "Work")
        with self.assertRaises(ValueError):
            book.add("Zed", "0412345678", "nope", "Work")
        with self.assertRaises(ValueError):
            book.add("Zed", "0412345678", "", "Colleagues")
        self.assertEqual(len(book.contacts), 0)

    def test_search_case_insensitive_and_multiple(self):
        book = sample_book()
        self.assertEqual(len(book.search("name", "ALICE")), 1)
        self.assertEqual(len(book.search("phone", "412")), 2)
        self.assertEqual(len(book.search("email", "@EXAMPLE")), 2)
        self.assertEqual(book.search("name", "zzz"), [])
        with self.assertRaises(ValueError):
            book.search("group", "Work")

    def test_update(self):
        book = sample_book()
        self.assertTrue(book.update(1, "phone", "0400 000 000"))
        self.assertEqual(book.find_by_id(1).phone, "0400 000 000")
        self.assertTrue(book.update(2, "group", "family"))
        self.assertEqual(book.find_by_id(2).group, "Family")
        self.assertTrue(book.update(1, "email", ""))
        self.assertEqual(book.find_by_id(1).email, "")

    def test_update_invalid_keeps_old_value(self):
        book = sample_book()
        with self.assertRaises(ValueError):
            book.update(1, "phone", "bad")
        self.assertEqual(book.find_by_id(1).phone, "0412 345 678")
        self.assertFalse(book.update(99, "name", "X Y"))

    def test_delete(self):
        book = sample_book()
        self.assertTrue(book.delete(1))
        self.assertIsNone(book.find_by_id(1))
        self.assertFalse(book.delete(99))

    def test_delete_confirmation_no_keeps_record(self):
        book = sample_book()
        with patch("builtins.input", side_effect=["1", "n"]), patch("builtins.print"):
            main.delete_contact(book)
        self.assertEqual(len(book.contacts), 3)
        with patch("builtins.input", side_effect=["1", "y"]), patch("builtins.print"):
            main.delete_contact(book)
        self.assertEqual(len(book.contacts), 2)

    def test_filter_group(self):
        book = sample_book()
        self.assertEqual(len(book.filter_by_group("Work")), 1)
        self.assertEqual(book.filter_by_group("Family")[0].name, "Carol Jones")

    def test_duplicates_ignore_formatting(self):
        dups = sample_book().find_duplicate_phones()
        self.assertEqual(list(dups.keys()), ["0412345678"])
        self.assertEqual(len(dups["0412345678"]), 2)
        self.assertEqual(ContactBook().find_duplicate_phones(), {})


class TestReports(unittest.TestCase):
    def test_summary_values(self):
        s = build_summary(sample_book().contacts)
        self.assertEqual(s["total"], 3)
        self.assertEqual(s["per_group"], {"Family": 1, "Friends": 1, "Work": 1})
        self.assertEqual(s["without_email"], 1)

    def test_summary_empty(self):
        s = build_summary([])
        self.assertEqual(s["total"], 0)
        self.assertEqual(s["without_email"], 0)

    def test_recursive_matches_loop(self):
        for size in [0, 1, 2, 3, 7, 50, 5000]:
            contacts = [Contact(i, "N", "12345678", "" if i % 3 == 0 else "a@b.co", "Work")
                        for i in range(1, size + 1)]
            expected = 0
            for c in contacts:
                if c.email == "":
                    expected += 1
            self.assertEqual(count_without_email(contacts), expected, size)


class TestStorage(unittest.TestCase):
    def test_missing_file_is_created(self):
        with tempfile.TemporaryDirectory() as d, patch("builtins.print"):
            path = os.path.join(d, "newdata", "c.csv")
            self.assertEqual(load_contacts(path), [])
            self.assertTrue(os.path.exists(path))

    def test_round_trip_keeps_blank_email_and_leading_zero(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "c.csv")
            save_contacts(path, sample_book().contacts)
            loaded = load_contacts(path)
            self.assertEqual(len(loaded), 3)
            self.assertEqual(loaded[1].email, "")
            self.assertEqual(loaded[0].phone, "0412 345 678")

    def test_bad_rows_skipped(self):
        with tempfile.TemporaryDirectory() as d, patch("builtins.print"):
            path = os.path.join(d, "c.csv")
            with open(path, "w") as f:
                f.write("id,name,phone,email,group\n"
                        "1,Good Person,0412345678,,Work\n"
                        "x,Bad Id,0412345678,,Work\n"
                        "2,Bad Group,0412345678,,Boss\n"
                        "1,Dup Id,0412345678,,Work\n"
                        "3,Bad Phone,12,,Work\n")
            self.assertEqual(len(load_contacts(path)), 1)

    def test_shipped_sample_has_at_least_8_records(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "contacts.csv")
        self.assertGreaterEqual(len(load_contacts(path)), 8)


class TestMenuLoop(unittest.TestCase):
    def run_main(self, inputs):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "c.csv")
            with patch.object(main, "DATA_FILE", path), patch("builtins.input", side_effect=inputs), \
                 patch("builtins.print") as printed:
                main.main()
            output = "\n".join(str(c.args[0]) if c.args else "" for c in printed.call_args_list)
            saved = load_contacts(path) if os.path.exists(path) else []
            return output, saved

    def test_invalid_menu_choices_then_exit(self):
        out, _ = self.run_main(["", "abc", "0", "10", "9"])
        self.assertEqual(out.count("Invalid choice"), 4)
        self.assertIn("Goodbye!", out)

    def test_add_then_exit_saves(self):
        _, saved = self.run_main(["1", "Zoe Park", "0411 222 333", "", "3", "9"])
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].group, "Work")

    def test_empty_view_message(self):
        out, _ = self.run_main(["2", "9"])
        self.assertIn("The contact book is empty.", out)

    def test_eof_exits_cleanly(self):
        out, _ = self.run_main(EOFError())
        self.assertIn("Goodbye!", out)


if __name__ == "__main__":
    unittest.main()
