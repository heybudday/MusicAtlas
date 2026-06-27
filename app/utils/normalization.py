import re


def normalize_name(name: str) -> str:
    """
    Normalize an artist or label name for exact matching.
    """

    if name is None:
        return ""

    name = name.casefold()
    name = name.strip()

    name = re.sub(r"\s+", " ", name)

    return name