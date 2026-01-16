import requests
from config import Config

LANGUAGE_VERSIONS = {
    "python": ("3.10.0", "py"),
    "c": ("10.2.0", "c"),
    "cpp": ("10.2.0", "cpp"),
    "java": ("15.0.2", "java"),
    "javascript": ("18.15.0", "js")
}


def execute_code(language, code, stdin):
    language = language.lower()

    if language not in LANGUAGE_VERSIONS:
        raise ValueError("Unsupported language")

    version, ext = LANGUAGE_VERSIONS[language]

    payload = {
        "language": language,
        "version": version,
        "files": [{
            "name": f"main.{ext}",
            "content": code
        }],
        "stdin": stdin
    }

    response = requests.post(
        Config.PISTON_API_URL,
        json=payload,
        timeout=10
    )
    response.raise_for_status()
    return response.json()
