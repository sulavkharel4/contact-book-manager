"""ContactBook: all record operations, with no input()/print() inside."""
from contact import Contact, normalise_phone
from validation import GROUPS, normalise_group, validate_contact

SEARCH_FIELDS = ("name", "phone", "email")
EDIT_FIELDS = ("name", "phone", "email", "group")


class ContactBook:
    def __init__(self, contacts=None):
        self.contacts = list(contacts) if contacts else []

    def _next_id(self):
        highest = 0
        for contact in self.contacts:
            if contact.contact_id > highest:
                highest = contact.contact_id
        return highest + 1

    def add(self, name, phone, email, group):
        """FR2: validate, give a unique ID, store. Raises ValueError if invalid."""
        name, phone, email = name.strip(), phone.strip(), email.strip()
        group = normalise_group(group) or group
        error = validate_contact(name, phone, email, group)
        if error:
            raise ValueError(error)
        contact = Contact(self._next_id(), name, phone, email, group)
        self.contacts.append(contact)
        return contact

    def find_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.contact_id == contact_id:
                return contact
        return None

    def search(self, field, text):
        """FR4: case-insensitive partial match on name, phone or email."""
        if field not in SEARCH_FIELDS:
            raise ValueError("Cannot search by that field.")
        text = text.strip().lower()
        results = []
        for contact in self.contacts:
            if text in getattr(contact, field).lower():
                results.append(contact)
        return results

    def update(self, contact_id, field, value):
        """FR5: change one field, re-validating. Returns False if ID unknown."""
        contact = self.find_by_id(contact_id)
        if contact is None:
            return False
        if field not in EDIT_FIELDS:
            raise ValueError("Cannot edit that field.")
        fields = {"name": contact.name, "phone": contact.phone,
                  "email": contact.email, "group": contact.group}
        fields[field] = value.strip()
        fields["group"] = normalise_group(fields["group"]) or fields["group"]
        error = validate_contact(**fields)
        if error:
            raise ValueError(error)
        contact.name, contact.phone = fields["name"], fields["phone"]
        contact.email, contact.group = fields["email"], fields["group"]
        return True

    def delete(self, contact_id):
        """FR6 (the confirmation happens in the menu). False if ID unknown."""
        contact = self.find_by_id(contact_id)
        if contact is None:
            return False
        self.contacts.remove(contact)
        return True

    def filter_by_group(self, group):
        """FR7: contacts in one group."""
        return [c for c in self.contacts if c.group == group]

    def find_duplicate_phones(self):
        """FR7: {normalised number: [contacts]} for numbers used more than once."""
        by_number = {}
        for contact in self.contacts:
            key = normalise_phone(contact.phone)
            if key not in by_number:
                by_number[key] = []
            by_number[key].append(contact)
        duplicates = {}
        for key in by_number:
            if len(by_number[key]) > 1:
                duplicates[key] = by_number[key]
        return duplicates

    def phone_in_use(self, phone, ignore_id=None):
        key = normalise_phone(phone)
        for contact in self.contacts:
            if contact.contact_id != ignore_id and normalise_phone(contact.phone) == key:
                return True
        return False
