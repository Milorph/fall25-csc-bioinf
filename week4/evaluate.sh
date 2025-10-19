#!/usr/bin/env bash
set -e

# =========================================================
# Week 4 – Sequence Alignment Evaluation
# Works both locally and on GitHub Actions.
# =========================================================

# Resolve directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PY_ALIGNER="${DIR}/aligners.py"
CODON_ALIGNER="${DIR}/aligners.codon"
DATA_DIR="${DIR}/data"

printf "========== Week 4 – Sequence Alignment Evaluation ==========\n"
printf "%-15s %-8s %-8s %-10s\n" "Method" "Lang" "Score" "Runtime"
printf "%0.s-" {1..47}; echo

METHODS=("global" "local" "semi-global" "affine-global")
PAIRS=("q1 t1" "q2 t2" "q3 t3" "q4 t4" "q5 t5")

echo
echo "========== SHORT SEQUENCES (q1-t1 through q5-t5) =========="
echo

for pair in "${PAIRS[@]}"; do
  set -- $pair
  q=$1
  t=$2
  echo "--- ${q} vs ${t} ---"

  for method in "${METHODS[@]}"; do
    # ----- Python -----
    start=$(date +%s%3N)
    py_score=$(python3 "$PY_ALIGNER" --method "$method" --a "$DATA_DIR/$q.fa" --b "$DATA_DIR/$t.fa" 2>/dev/null || echo "ERR")
    end=$(date +%s%3N)
    py_time=$((end - start))
    printf "  %-15s %-8s %-8s %sms\n" "$method" "python" "$py_score" "$py_time"

    # ----- Codon -----
    start=$(date +%s%3N)
    codon_score=$(codon run "$CODON_ALIGNER" --method "$method" --a "$DATA_DIR/$q.fa" --b "$DATA_DIR/$t.fa" 2>/dev/null || echo "ERR")
    end=$(date +%s%3N)
    codon_time=$((end - start))
    printf "  %-15s %-8s %-8s %sms\n" "$method" "codon" "$codon_score" "$codon_time"
  done
  echo
done

echo "========== LONG SEQUENCES (MT-human vs MT-orang) =========="
echo

for method in "${METHODS[@]}"; do
  echo "--- $method ---"

  start=$(date +%s%3N)
  py_score=$(python3 "$PY_ALIGNER" --method "$method" --a "$DATA_DIR/MT-human.fa" --b "$DATA_DIR/MT-orang.fa" 2>/dev/null || echo "ERR")
  end=$(date +%s%3N)
  py_time=$((end - start))
  printf "  %-15s %-8s %-8s %sms\n" "$method" "python" "$py_score" "$py_time"

  start=$(date +%s%3N)
  codon_score=$(codon run "$CODON_ALIGNER" --method "$method" --a "$DATA_DIR/MT-human.fa" --b "$DATA_DIR/MT-orang.fa" 2>/dev/null || echo "ERR")
  end=$(date +%s%3N)
  codon_time=$((end - start))
  printf "  %-15s %-8s %-8s %sms\n" "$method" "codon" "$codon_score" "$codon_time"
done

echo
echo "✅ Finished all alignment tests."
echo "========================================"
