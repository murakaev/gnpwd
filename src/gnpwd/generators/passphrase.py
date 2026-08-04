import secrets
import os
from pathlib import Path

DEFAULT_WORDLIST_PATH = "eff_wordlist.txt"


class PassphraseGenerator:
    def __init__(self, word_count: int = 6):
        """
        Initialize the passphrase generator.

        Args:
            word_count: Number of words to include in the passphrase (default: 6)
        """
        self.word_count = word_count
        self.wordlist_path = None
        self._load_wordlist()

    def _get_cache_dir(self) -> Path:
        """Get the cache direactory path."""
        return Path.home() / ".gnpwd" / "cache"

    def _load_wordlist(self) -> None:
        """Load or download the EFF wordlist if not already cached."""
        cache_dir = self._get_cache_dir()
        cache_dir.mkdir(parents=True, exist_ok=True)
        wordlist_path = cache_dir / DEFAULT_WORDLIST_PATH

        if wordlist_path.exists():
            self.wordlist_path = str(wordlist_path)
            return

        print("Downloading EFF wordlist...")
        try:
            import requests

            response = requests.get("https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt")
            response.raise_for_status()

            with open(wordlist_path, "w", encoding="utf-8") as f:
                for line in response.text.splitlines():
                    word = line.strip().lower()
                    if len(word) > 0 and not word.startswith("#"):
                        f.write(f"{word}\n")
            self.wordlist_path = str(wordlist_path)
        except Exception as e:
            raise RuntimeError(f"Failed to download the EFF wordlist: {e}")

    def generate_passphrase(self, separator: str = "-", max_attempts: int = 10) -> str:
        """
        Generate a cryptographically secure passphrase.

        Args:
            separator: Character(s) to separate words (default: hyphen)
            max_attempts: Maximum attempts to find unique words

        Returns:
            Generated passphrase string
        """
        if not self.wordlist_path:
            raise RuntimeError("Wordlist not loaded")

        with open(self.wordlist_path, 'r', encoding='utf-8') as f:
            words = [line.split()[1] for line in f]

        valid_words = [word for word in words if len(word) > 1]
        if len(valid_words) < self.word_count * max_attempts:
            raise RuntimeError("Not enough unique words available")

        passphrase_parts = set()
        attempts = 0

        while len(passphrase_parts) < self.word_count and attempts < max_attempts:
            word = secrets.choice(valid_words)
            if word not in passphrase_parts:
                passphrase_parts.add(word)
            attempts += 1

        return separator.join(sorted(passphrase_parts))

generator = PassphraseGenerator()
print(generator._get_cache_dir())