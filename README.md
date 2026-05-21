# hman — Terminal Hangman

A minimal, cross-platform Hangman game for the terminal. Written in **Python 3** using only the standard library — no dependencies, no build step.

**Languages:** English and Turkish (choose at startup).

## Requirements

- Python 3.9 or newer

## Quick start

```bash
git clone https://github.com/ferdisahin/hman.git
cd hman
python3 hangman.py
```

On launch you pick a language:

```
=== Hangman / Adam Asmaca ===

Select language:
  1) English
  2) Turkish

>
```

## How to play

1. Select **English** or **Turkish**.
2. A random word is chosen from the matching word list.
3. Guess one letter at a time.
4. You have **6** wrong guesses before the hangman is complete.
5. Type `quit` or `q` to exit mid-round (Turkish mode also accepts `çık`).

## Word lists

| File | Language |
|------|----------|
| `words_en.txt` | English (a–z) |
| `words_tr.txt` | Turkish (includes ç, ğ, ı, ö, ş, ü) |

One word per line. Words are normalized to lowercase at runtime.

## Install with Homebrew

After you publish a [Homebrew tap](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap), users install once:

```bash
brew install ferdisahin/tap/hman
```

Then open any terminal and run:

```bash
hman
```

Homebrew installs the `hman` command under `$(brew --prefix)/bin`, which is already on your `PATH` — no need to `cd` into the project folder.

### Tap setup (maintainer)

1. Tag a release: `git tag 1.1 && git push origin refs/tags/1.1` ([releases](https://github.com/ferdisahin/hman/releases))
2. Copy `homebrew/Formula/hman.rb` into your tap repo (`homebrew-tap/Formula/`)
3. Update `url` and `sha256` in the formula (from the release tarball)
4. Push the tap repo

Example formula snippet — the install exposes the **`hman`** command:

```ruby
(bin/"hman").write <<~EOS
  #!/bin/bash
  exec "#{Formula["python@3.12"].opt_bin}/python3.12" "#{libexec}/hangman.py" "$@"
EOS
```

Verify locally (the formula must live in a tap — copy `hman.rb` into `$(brew --repository ferdisahin/tap)/Formula/` first, or create a tap):

```bash
brew tap-new ferdisahin/tap --no-git  # skip if the tap already exists
cp homebrew/Formula/hman.rb "$(brew --repository ferdisahin/tap)/Formula/"
brew install ferdisahin/tap/hman
hman --version   # expect: hman 1.1
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
hman/
├── hangman.py                 # game logic and UI
├── words_en.txt               # English words
├── words_tr.txt               # Turkish words
├── homebrew/Formula/hman.rb   # copy to your tap repo
└── README.md
```

## License

MIT — see [LICENSE](LICENSE).
