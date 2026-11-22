"""Summary report (FR8) - totals are counted with our own loops, not len()/sum()."""
from validation import GROUPS


def count_without_email(contacts):
    """RECURSIVE (FR10): count contacts that have no email.

    Divide and conquer: split the list in half, count each half, add results.
    Base cases : empty list -> 0; single contact -> 1 if email is blank else 0.
    Recursive case: count(left half) + count(right half).
    Depth is about log2(n), so large lists do not hit Python's recursion limit.
    """
    size = len(contacts)
    if size == 0:
        return 0
    if size == 1:
        return 1 if contacts[0].email == "" else 0
    middle = size // 2
    return count_without_email(contacts[:middle]) + count_without_email(contacts[middle:])


def build_summary(contacts):
    """Return the report values: total, per group, and without email."""
    total = 0
    per_group = {group: 0 for group in GROUPS}
    for contact in contacts:
        total += 1
        per_group[contact.group] += 1
    return {"total": total,
            "per_group": per_group,
            "without_email": count_without_email(contacts)}
