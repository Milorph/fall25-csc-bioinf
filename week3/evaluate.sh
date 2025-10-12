#!/usr/bin/env bash
# file: evaluate.sh
# Run Codon and Python tests (both already print runtime)

set -e
cd code

echo "🔧 Building Codon executable..."
codon build -release test_phylo.codon -o test_phylo_codon_exe

echo ""
echo "🚀 Running Phylo Tests"
echo "-----------------------------------"
printf "%-15s | %-12s\n" "Implementation" "Runtime"
echo "-----------------------------------"

printf "%-15s | " "Codon"
./test_phylo_codon_exe

printf "%-15s | " "Python"
python3 test_phylo.py

echo "-----------------------------------"
echo "✅ Evaluation complete."
