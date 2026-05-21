# Hangman / Adam Asmaca (Terminal)

A minimal, cross-platform Hangman game for the terminal. Written in **Python 3** using only the standard library — no dependencies, no build step.

**Languages:** English and Turkish (choose at startup).

## Requirements

- Python 3.9 or newer

## Quick start

```bash
git clone https://github.com/ferdisahin/adam-asmaca.git
cd adam-asmaca
python3 hangman.py
```

On launch you pick a language:

```
=== Hangman / Adam Asmaca ===

Select language / Dil seçin:
  1) English
  2) Türkçe

>
```

## How to play

1. Select **English** or **Türkçe**.
2. A random word is chosen from the matching word list.
3. Guess one letter at a time.
4. You have **6** wrong guesses before the hangman is complete.
5. Type `quit` / `çık` (or `q`) to exit mid-round.

## Word lists

| File | Language |
|------|----------|
| `words_en.txt` | English (a–z) |
| `words_tr.txt` | Turkish (includes ç, ğ, ı, ö, ş, ü) |

One word per line. Words are normalized to lowercase at runtime.

## Install with Homebrew (`hman` command)

After you publish a [Homebrew tap](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap), users install once:

```bash
brew install ferdisahin/tap/adam-asmaca
```

Then open any terminal and run:

```bash
hman
```

Homebrew puts `hman` in `$(brew --prefix)/bin`, which is already on your `PATH` — no `cd` into the project folder.

### Tap setup (maintainer)

1. Tag a release in this repo: `git tag v1.0.0 && git push origin v1.0.0`
2. Copy `homebrew/Formula/adam-asmaca.rb` into your tap repo (`homebrew-tap/Formula/`)
3. Update `sha256` in the formula (from the release tarball)
4. Push the tap repo

Example formula snippet — the important part is the **`bin/"hman"`** name:

```ruby
(bin/"hman").write <<~EOS
  #!/bin/bash
  exec "#{Formula["python@3.12"].opt_bin}/python3.12" "#{libexec}/hangman.py" "$@"
EOS
```

Verify locally:

```bash
brew install --build-from-source ./homebrew/Formula/adam-asmaca.rb
hman
hman --version
```

### Test without Homebrew (dev)

```bash
ln -sf "$(pwd)/hangman.py" ~/bin/hman   # if ~/bin is on PATH
chmod +x hangman.py
hman
```

## Roadmap

- [x] Language selection (EN / TR)
- [ ] Difficulty levels (easy / medium / hard)

## Project layout

```
adam-asmaca/
├── hangman.py              # game logic and UI
├── words_en.txt            # English words
├── words_tr.txt            # Turkish words
├── homebrew/Formula/       # copy to your tap repo
└── README.md
```

## License

MIT — see [LICENSE](LICENSE).
