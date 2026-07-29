import string
import secrets

def generate_password(length: int, use_digits: bool, use_capital: bool, use_symbols: bool, exclude_ambiguous: bool) -> str:
    elements = ""

    if use_capital:
        elements = string.ascii_letters
    else:
        elements = string.ascii_lowercase

    if use_digits:
        elements += string.digits

    if use_symbols:
        elements += string.punctuation

    if exclude_ambiguous:
        ambiguous = "0O1lI|"
        elements = "".join(e for e in elements if e not in ambiguous)

    return "".join(secrets.choice(elements) for _ in range(length))