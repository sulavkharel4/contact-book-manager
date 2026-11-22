"""The Contact record."""


def normalise_phone(phone):
    """Keep digits only, so '0412 345-678' and '0412345678' compare equal."""
    return "".join(ch for ch in phone if ch.isdigit())


class Contact:
    FIELDS = ["id", "name", "phone", "email", "group"]

    def __init__(self, contact_id, name, phone, email, group):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group

    def to_row(self):
        return {"id": self.contact_id, "name": self.name, "phone": self.phone,
                "email": self.email, "group": self.group}

    @classmethod
    def from_row(cls, row):
        """Build a Contact from a CSV row. Raises ValueError on bad data."""
        from validation import normalise_group
        try:
            contact_id = int(row["id"])
            group = normalise_group(row["group"])
            if contact_id < 1 or group is None:
                raise ValueError("bad id or group")
            return cls(contact_id, row["name"].strip(), row["phone"].strip(),
                       (row["email"] or "").strip(), group)
        except (KeyError, TypeError, AttributeError) as error:
            raise ValueError(f"malformed row: {error}")
