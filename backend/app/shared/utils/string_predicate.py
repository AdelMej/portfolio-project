SPECIAL_CHARS = r"!@#$%^&*()_+\-=\[\]{};:,.?/"


def is_blank(value: str) -> bool:
    return not value.strip()


def has_text(value: str) -> bool:
    return not is_blank(value)


def contains_lowercase(value: str) -> bool:
    return any(c.islower() for c in value)


def contains_uppercase(value: str) -> bool:
    return any(c.isupper() for c in value)


def contains_digit(value: str) -> bool:
    return any(c.isdigit() for c in value)


def contains_special(value: str) -> bool:
    return any(c in SPECIAL_CHARS for c in value)
