"""Contact Book Manager - menu-driven console application.
Author: Sulav Kharel (SM20252552)

Run with:  python main.py
"""
import os

from display import format_table, print_summary, show_contacts
from manager import ContactBook
from reports import build_summary
from storage import load_contacts, save_contacts
from validation import (read_choice, read_email, read_group, read_name,
                        read_phone, read_yes_no, read_nonempty)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "contacts.csv")

MENU = """
===== CONTACT BOOK MANAGER =====
1. Add a contact
2. View all contacts
3. Search contacts
4. Update a contact
5. Delete a contact
6. Filter by group
7. Detect duplicate phone numbers
8. Summary report
9. Exit"""


def ask_for_existing_id(book, prompt="Enter contact ID (blank to cancel): "):
    """Loop until the user gives an ID that exists; blank cancels (returns None)."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return None
        if not text.isdigit():
            print("ID must be a whole number.")
            continue
        contact = book.find_by_id(int(text))
        if contact is not None:
            return contact
        print(f"No contact with ID {text}.")


def add_contact(book):
    print("\n--- Add a contact ---")
    name = read_name()
    phone = read_phone()
    if book.phone_in_use(phone):
        print("Note: this phone number is already used by another contact.")
    email = read_email()
    group = read_group()
    contact = book.add(name, phone, email, group)
    print(f"Added '{contact.name}' with ID {contact.contact_id}.")


def view_contacts(book):
    print("\n--- All contacts ---")
    show_contacts(book.contacts, "The contact book is empty.")


def search_contacts(book):
    print("\n--- Search ---")
    print("1. By name\n2. By phone\n3. By email")
    field = ("name", "phone", "email")[read_choice("Search by (1-3): ", 1, 3) - 1]
    text = read_nonempty(f"Enter {field} text to find: ")
    show_contacts(book.search(field, text), "No matching contacts found.")


def update_contact(book):
    print("\n--- Update a contact ---")
    contact = ask_for_existing_id(book)
    if contact is None:
        print("Update cancelled.")
        return
    print("1. Name\n2. Phone\n3. Email\n4. Group")
    choice = read_choice("Field to change (1-4): ", 1, 4)
    if choice == 1:
        field, value = "name", read_name("New name: ")
    elif choice == 2:
        field, value = "phone", read_phone("New phone: ")
    elif choice == 3:
        field, value = "email", read_email("New email (blank to remove): ")
    else:
        field, value = "group", read_group("New group (1=Family, 2=Friends, 3=Work): ")
    book.update(contact.contact_id, field, value)
    print("Contact updated.")


def delete_contact(book):
    print("\n--- Delete a contact ---")
    contact = ask_for_existing_id(book)
    if contact is None:
        print("Delete cancelled.")
        return
    show_contacts([contact])
    if read_yes_no(f"Delete '{contact.name}'? (Y/N): "):
        book.delete(contact.contact_id)
        print("Contact deleted.")
    else:
        print("Delete cancelled - nothing was removed.")


def filter_by_group(book):
    print("\n--- Filter by group ---")
    group = read_group()
    show_contacts(book.filter_by_group(group), f"No contacts in the {group} group.")


def show_duplicates(book):
    print("\n--- Duplicate phone numbers ---")
    duplicates = book.find_duplicate_phones()
    if not duplicates:
        print("No duplicate phone numbers found.")
        return
    for number in duplicates:
        print(f"\nNumber {number} is used by {len(duplicates[number])} contacts:")
        print(format_table(duplicates[number]))


def show_summary(book):
    print_summary(build_summary(book.contacts))


ACTIONS = {"1": add_contact, "2": view_contacts, "3": search_contacts,
           "4": update_contact, "5": delete_contact, "6": filter_by_group,
           "7": show_duplicates, "8": show_summary}


def main():
    book = ContactBook(load_contacts(DATA_FILE))
    print(f"Loaded {len(book.contacts)} contact(s).")
    try:
        while True:
            print(MENU)
            choice = input("Enter your choice (1-9): ").strip()
            if choice == "9":
                break
            action = ACTIONS.get(choice)
            if action is None:
                print("Invalid choice. Please enter a number from 1 to 9.")
                continue
            action(book)
    except (KeyboardInterrupt, EOFError):
        print("\nInput ended - saving and exiting.")
    try:
        save_contacts(DATA_FILE, book.contacts)
        print("Contacts saved.")
    except OSError as error:
        print(f"Could not save the file: {error}")
    print("Goodbye!")


if __name__ == "__main__":
    main()
