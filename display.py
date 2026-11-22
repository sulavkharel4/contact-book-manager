"""Formatting and printing (FR3, FR8 output)."""
from validation import GROUPS


def format_table(contacts):
    header = f"{'ID':<5}{'Name':<22}{'Phone':<22}{'Email':<30}{'Group':<8}"
    lines = [header, "-" * len(header)]
    for c in contacts:
        email = c.email if c.email else "-"
        lines.append(f"{c.contact_id:<5}{c.name[:21]:<22}{c.phone[:21]:<22}"
                     f"{email[:29]:<30}{c.group:<8}")
    return "\n".join(lines)


def show_contacts(contacts, empty_message="No contacts to show."):
    if not contacts:
        print(empty_message)
    else:
        print(format_table(contacts))
        print(f"\n{len(contacts)} contact(s) listed.")


def print_summary(summary):
    print("\n===== SUMMARY REPORT =====")
    print(f"Total contacts          : {summary['total']}")
    print("Contacts per group:")
    for group in GROUPS:
        print(f"  {group:<10}: {summary['per_group'][group]}")
    print(f"Contacts without email  : {summary['without_email']}")
    print("==========================")
