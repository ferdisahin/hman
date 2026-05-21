#!/usr/bin/env python3
"""Terminal Hangman — stdlib only, Python 3.9+. English and Turkish."""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path

MAX_WRONG = 6
ROOT = Path(__file__).parent

EN_ALPHABET = frozenset("abcdefghijklmnopqrstuvwxyz")
TR_ALPHABET = frozenset("abcçdefgğhıijklmnoöprsştuüvyz")

HANGMAN_STAGES = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
""",
]


@dataclass(frozen=True)
class Locale:
    code: str
    words_file: Path
    alphabet: frozenset[str]
    strings: dict[str, str]


LOCALES: dict[str, Locale] = {
    "en": Locale(
        code="en",
        words_file=ROOT / "words_en.txt",
        alphabet=EN_ALPHABET,
        strings={
            "title": "=== Hangman ===",
            "choose_language": "Select language:",
            "lang_option_en": "  1) English",
            "lang_option_tr": "  2) Türkçe",
            "invalid_language": "Invalid choice. Enter 1, 2, en, or tr.",
            "loaded_words": "Loaded {count} words. You have {max_wrong} wrong guesses.",
            "press_enter": "Press Enter to start...",
            "wrong_guesses": "Wrong guesses: {wrong}/{max_wrong}",
            "word": "Word:",
            "guessed_letters": "Guessed letters: {letters}",
            "guess_prompt": "Guess a letter (or 'quit'):",
            "single_letter": "Please enter a single letter (a-z).",
            "already_tried": "You already tried '{letter}'.",
            "won": "You won! The word was: {word}",
            "lost": "Game over. The word was: {word}",
            "thanks": "Thanks for playing!",
            "not_in_word": "'{letter}' is not in the word.",
            "in_word": "Good — '{letter}' is in the word!",
            "score": "Score — Wins: {wins}  Losses: {losses}",
            "play_again": "Play again? [y/n]:",
            "goodbye": "Goodbye!",
            "error_missing_file": "Error: word list not found ({path})",
            "error_empty": "Error: word list is empty.",
        },
    ),
    "tr": Locale(
        code="tr",
        words_file=ROOT / "words_tr.txt",
        alphabet=TR_ALPHABET,
        strings={
            "title": "=== Adam Asmaca ===",
            "choose_language": "Dil seçin:",
            "lang_option_en": "  1) English",
            "lang_option_tr": "  2) Türkçe",
            "invalid_language": "Geçersiz seçim. 1, 2, en veya tr girin.",
            "loaded_words": "{count} kelime yüklendi. {max_wrong} yanlış hakkınız var.",
            "press_enter": "Başlamak için Enter'a basın...",
            "wrong_guesses": "Yanlış tahmin: {wrong}/{max_wrong}",
            "word": "Kelime:",
            "guessed_letters": "Denenen harfler: {letters}",
            "guess_prompt": "Bir harf tahmin edin ('çık' ile bitirin):",
            "single_letter": "Lütfen tek bir harf girin (a-z, ç, ğ, ı, ö, ş, ü).",
            "already_tried": "'{letter}' harfini zaten denediniz.",
            "won": "Kazandınız! Kelime: {word}",
            "lost": "Oyun bitti. Kelime: {word}",
            "thanks": "Oynadığınız için teşekkürler!",
            "not_in_word": "'{letter}' kelimede yok.",
            "in_word": "Güzel — '{letter}' kelimede var!",
            "score": "Skor — Galibiyet: {wins}  Mağlubiyet: {losses}",
            "play_again": "Tekrar oynamak ister misiniz? [e/h]:",
            "goodbye": "Güle güle!",
            "error_missing_file": "Hata: kelime listesi bulunamadı ({path})",
            "error_empty": "Hata: kelime listesi boş.",
        },
    ),
}

QUIT_WORDS = frozenset({"quit", "q", "exit", "çık", "cik", "çıkış", "cikis"})


def t(locale: Locale, key: str, **kwargs: object) -> str:
    return locale.strings[key].format(**kwargs)


def normalize_letter(char: str, locale: Locale) -> str:
    if locale.code == "tr":
        if char == "I":
            return "ı"
        if char == "İ":
            return "i"
    return char.lower()


def is_valid_word(word: str, locale: Locale) -> bool:
    return bool(word) and all(c in locale.alphabet for c in word)


def load_words(locale: Locale) -> list[str]:
    path = locale.words_file
    if not path.exists():
        print(t(locale, "error_missing_file", path=path), file=sys.stderr)
        sys.exit(1)

    words: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        word = normalize_letter(line.strip(), locale)
        if is_valid_word(word, locale):
            words.append(word)

    if not words:
        print(t(locale, "error_empty"), file=sys.stderr)
        sys.exit(1)
    return words


def choose_language() -> Locale:
    print("=== Hangman / Adam Asmaca ===\n")
    print("Select language / Dil seçin:")
    print("  1) English")
    print("  2) Türkçe")

    mapping = {
        "1": "en",
        "2": "tr",
        "en": "en",
        "english": "en",
        "ingilizce": "en",
        "tr": "tr",
        "turkish": "tr",
        "türkçe": "tr",
        "turkce": "tr",
    }

    while True:
        raw = input("\n> ").strip().lower()
        code = mapping.get(raw)
        if code in LOCALES:
            return LOCALES[code]
        print("Invalid choice / Geçersiz seçim. Enter 1, 2, en, or tr.")


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def display_state(locale: Locale, secret: str, guessed: set[str], wrong: int) -> None:
    clear_screen()
    print(HANGMAN_STAGES[wrong])
    print(t(locale, "wrong_guesses", wrong=wrong, max_wrong=MAX_WRONG) + "\n")

    display = " ".join(c if c in guessed else "_" for c in secret)
    print(f"{t(locale, 'word')}  {display}\n")

    letters = sorted(ch for ch in guessed if ch in locale.alphabet)
    if letters:
        print(t(locale, "guessed_letters", letters=", ".join(letters)))


def prompt_guess(locale: Locale, guessed: set[str]) -> str:
    while True:
        raw = input(f"\n{t(locale, 'guess_prompt')} ").strip()
        if raw.lower() in QUIT_WORDS:
            raise KeyboardInterrupt

        if len(raw) != 1:
            print(t(locale, "single_letter"))
            continue

        letter = normalize_letter(raw, locale)
        if letter not in locale.alphabet:
            print(t(locale, "single_letter"))
            continue
        if letter in guessed:
            print(t(locale, "already_tried", letter=letter))
            continue
        return letter


def play_round(locale: Locale, words: list[str]) -> bool | None:
    secret = random.choice(words)
    guessed: set[str] = set()
    wrong = 0

    while True:
        display_state(locale, secret, guessed, wrong)

        if all(c in guessed for c in secret):
            print("\n" + t(locale, "won", word=secret))
            return True

        if wrong >= MAX_WRONG:
            print("\n" + t(locale, "lost", word=secret))
            return False

        try:
            letter = prompt_guess(locale, guessed)
        except KeyboardInterrupt:
            print("\n\n" + t(locale, "thanks"))
            return None

        guessed.add(letter)
        if letter not in secret:
            wrong += 1
            print(t(locale, "not_in_word", letter=letter))
        else:
            print(t(locale, "in_word", letter=letter))


def wants_replay(locale: Locale, answer: str) -> bool:
    answer = answer.strip().lower()
    if locale.code == "tr":
        return answer in ("e", "evet", "y", "yes")
    return answer in ("y", "yes", "e", "evet")


def print_version() -> None:
    print("hman 1.1")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in ("--version", "-V"):
        print_version()
        return
    locale = choose_language()
    words = load_words(locale)

    print("\n" + t(locale, "title"))
    print(
        t(locale, "loaded_words", count=len(words), max_wrong=MAX_WRONG) + "\n"
    )
    input(t(locale, "press_enter"))

    wins = losses = 0
    while True:
        result = play_round(locale, words)
        if result is None:
            break
        if result:
            wins += 1
        else:
            losses += 1

        print("\n" + t(locale, "score", wins=wins, losses=losses))
        again = input("\n" + t(locale, "play_again"))
        if not wants_replay(locale, again):
            print(t(locale, "goodbye"))
            break


if __name__ == "__main__":
    main()
