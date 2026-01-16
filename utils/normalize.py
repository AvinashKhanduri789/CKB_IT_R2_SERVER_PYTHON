def normalize(value: str = "") -> str:
    return (
        value
        .replace("\\n", "\n")
        .replace("\r\n", "\n")
        .rstrip()
        .strip()
    )
