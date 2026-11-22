"""CSV persistence (FR9). Uses the csv module."""
import csv
import os

from contact import Contact
from validation import validate_contact


def save_contacts(path, contacts):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Contact.FIELDS)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact.to_row())


def load_contacts(path):
    """Load contacts. Creates an empty file if missing; skips bad rows."""
    if not os.path.exists(path):
        save_contacts(path, [])
        print(f"No data file found - created new file: {path}")
        return []

    contacts, seen_ids = [], set()
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                contact = Contact.from_row(row)
                error = validate_contact(contact.name, contact.phone,
                                         contact.email, contact.group)
                if error:
                    raise ValueError(error)
                if contact.contact_id in seen_ids:
                    raise ValueError("duplicate ID")
            except ValueError as problem:
                print(f"Warning: skipped line {line_no} of CSV ({problem})")
                continue
            seen_ids.add(contact.contact_id)
            contacts.append(contact)
    return contacts
