import secrets
import string


def generate_password(
    length: int,
    use_digits: bool,
    use_capital: bool,
    use_symbols: bool,
    exclude_ambiguous: bool,
    min_length: int = 8,
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length: Desired password length (must be >= min_length)
        use_digits: Include digits (0-9)
        use_capital: Include uppercase letters (A-Z)
        use_symbols: Include symbols (!@#$%^&*)
        exclude_ambiguous: Exclude easily confused characters
        min_length: Minimum allowed password length

    Returns:
        Generated password string

    Raises:
        ValueError: If length is too short
    """

    if length < min_length:
        raise ValueError(f"Password length must be at least {min_length} characters")

    char_set = []
    if use_capital:
        char_set.append(string.ascii_letters)
    else:
        char_set.append(string.ascii_lowercase)

    if use_digits:
        char_set.append(string.digits)

    if use_symbols:
        char_set.append("!@#$%&*()")

    elements = "".join(char_set)
    if exclude_ambiguous:
        ambiguous = "0O1lI|2Z5S"
        elements = "".join(c for c in elements if c not in ambiguous)

    return "".join(secrets.choice(elements) for _ in range(length))
