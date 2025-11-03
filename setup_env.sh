#!/usr/bin/env bash
set -e

echo "🔧 Setting up local environment (Codon + Python + deps)..."

# --- 1️⃣ System setup ---
sudo apt-get update
sudo apt-get install -y curl tar bc build-essential python3 python3-pip

# --- 2️⃣ Install Codon and Seq plugins ---
mkdir -p "${HOME}/.codon"
curl -L https://github.com/exaloop/codon/releases/download/v0.19.3/codon-linux-x86_64.tar.gz \
  | tar zxvf - --strip-components=1 -C "${HOME}/.codon"
curl -L https://github.com/exaloop/seq/releases/download/v0.11.5/seq-linux-x86_64.tar.gz \
  | tar zxvf - -C "${HOME}/.codon/lib/codon/plugins"

# Add Codon to PATH permanently
if ! grep -q ".codon/bin" ~/.bashrc; then
  echo 'export PATH="$PATH:$HOME/.codon/bin"' >> ~/.bashrc
fi
export PATH="$PATH:$HOME/.codon/bin"

# --- 3️⃣ Python setup ---
python3 -m pip install --upgrade pip
python3 -m pip install find_libpython matplotlib numpy pytest distinctipy trviz biotite

# --- 4️⃣ Configure Codon bridge ---
CODON_PYTHON=$(python3 -c "import find_libpython; print(find_libpython.find_libpython())")
export CODON_PYTHON
echo "export CODON_PYTHON=${CODON_PYTHON}" >> ~/.bashrc

echo "✅ Codon installed at: $(command -v codon)"
codon --version
echo "✅ CODON_PYTHON set to: $CODON_PYTHON"

echo "🎉 Environment setup complete!"
