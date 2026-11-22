"""Validation helpers and input prompts (FR11).

Pure checkers (is_valid_*, validate_contact) are separate from the prompt
functions (read_*) so the checkers can be unit-tested without typing input.
"""
import re

GROUPS = ("Family", "Friends", "Work")


# ---------- pure checkers ----------
def is_valid_name(value):
    value = value.strip()
    return 0 < len(value) <= 50 and any(ch.isalpha() for ch in value)


def is_valid_phone(value):
    """Digits, spaces, hyphens, optional leading '+'; 8-15 digits in total."""
    value = value.strip()
    if not re.fullmatch(r"\+?[0-9 \-]+", value):
        return False
    digits = sum(1 for ch in value if ch.isdigit())
    return 8 <= digits <= 15


def is_valid_email(value):
    """Blank is allowed (an email is optional); otherwise needs x@y.z form."""
    value = value.strip()
    if value == "":
        return True
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) is not None


def normalise_group(value):
    """Return 'Family'/'Friends'/'Work' for a name (any case) or 1-3, else None."""
    value = value.strip().lower()
    for group in GROUPS:
        if group.lower() == value:
            return group
    if value.isdigit() and 1 <= int(value) <= len(GROUPS):
        return GROUPS[int(value) - 1]
    return None


def validate_contact(name, phone, email, group):
    """Return an error message, or None if every field is valid."""
    if not is_valid_name(name):
        return "Name must be 1-50 characters and contain a letter."
    if not is_valid_phone(phone):
        return "Phone must have 8-15 digits (spaces, hyphens, leading + allowed)."
    if not is_valid_email(email):
        return "Email must look like name@example.com (or be blank)."
    if group not in GROUPS:
        return "Group must be Family, Friends or Work."
    return None


# ---------- prompts: loop until valid ----------
def read_name(prompt="Name: "):
    while True:
        value = input(prompt).strip()
        if is_valid_name(value):
            return value
        print("Invalid name: 1-50 characters, must contain a letter.")


def read_phone(prompt="Phone: "):
    while True:
        value = input(prompt).strip()
        if is_valid_phone(value):
            return value
        print("Invalid phone: use 8-15 digits (spaces, hyphens, leading + allowed).")


def read_email(prompt="Email (blank for none): "):
    while True:
        value = input(prompt).strip()
        if is_valid_email(value):
            return value
        print("Invalid email: use the form name@example.com or leave blank.")


def read_group(prompt="Group (1=Family, 2=Friends, 3=Work): "):
    while True:
        group = normalise_group(input(prompt))
        if group is not None:
            return group
        print("Invalid group: enter Family, Friends, Work or 1-3.")


def read_choice(prompt, low, high):
    """Read an integer between low and high (inclusive)."""
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if low <= number <= high:
            return number
        print(f"Please enter a number from {low} to {high}.")


def read_yes_no(prompt):
    while True:
        text = input(prompt).strip().lower()
        if text in ("y", "yes"):
            return True
        if text in ("n", "no"):
            return False
        print("Please answer Y or N.")


def read_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")
