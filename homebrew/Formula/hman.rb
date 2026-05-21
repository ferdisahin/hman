# Copy this file to your tap repo:
#   homebrew-tap/Formula/hman.rb
#
# Update sha256 after a new release tag:
#   curl -L https://github.com/ferdisahin/hman/archive/refs/tags/1.0.tar.gz | shasum -a 256

class Hman < Formula
  desc "Terminal Hangman in English and Turkish"
  homepage "https://github.com/ferdisahin/hman"
  url "https://github.com/ferdisahin/hman/archive/refs/tags/1.0.tar.gz"
  sha256 "b0090d6b1d8c0be32905550132b8b1c470b269c39e2b0f477e594498d27824d6"
  license "MIT"

  depends_on "python@3.12"

  def install
    # Game files live together so hangman.py finds words_en.txt / words_tr.txt
    libexec.install "hangman.py", "words_en.txt", "words_tr.txt", "LICENSE"

    # Terminal command: hman
    (bin/"hman").write <<~EOS
      #!/bin/bash
      exec "#{Formula["python@3.12"].opt_bin}/python3.12" "#{libexec}/hangman.py" "$@"
    EOS
  end

  test do
    assert_path_exists libexec/"hangman.py"
    assert_path_exists libexec/"words_en.txt"
    assert_path_exists libexec/"words_tr.txt"
    assert_predicate bin/"hman", :exist?
    system bin/"hman", "--version"
  end
end
