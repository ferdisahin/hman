# Copy this file to your tap repo:
#   homebrew-tap/Formula/adam-asmaca.rb
#
# Replace ferdisahin and update sha256 after tagging v1.0.0:
#   curl -L https://github.com/ferdisahin/adam-asmaca/archive/refs/tags/v1.0.0.tar.gz | shasum -a 256

class AdamAsmaca < Formula
  desc "Terminal Hangman in English and Turkish"
  homepage "https://github.com/ferdisahin/adam-asmaca"
  url "https://github.com/ferdisahin/adam-asmaca/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "REPLACE_AFTER_RELEASE"
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
