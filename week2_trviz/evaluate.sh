#!/usr/bin/env bash
set -euo pipefail

echo "▶ Running Codon tests in week2_trviz"

# Move into codon_impl/tests directory
cd "$(dirname "$0")/codon_impl/tests"

# Ensure outputs folder exists
mkdir -p ../outputs
mkdir -p ./outputs

# Run all *_test.codon files
for f in *_test.codon; do
  echo "▶ Running $f"
  codon run "$f"
done

# Optional: run pipeline & plotting
cd ..
if [ -f main.codon ]; then
  echo "▶ Running main.codon to generate alignment outputs"
  codon run main.codon || true
fi

# Go back to project root (week2_trviz)
cd ..

if [ -f pyviz/viz_trplot.py ]; then
  echo "▶ Generating plots from Codon outputs"
  python pyviz/viz_trplot.py outputs/VariantMotif2.aligned.txt outputs/VariantMotif2_motif_map.txt || true
fi

