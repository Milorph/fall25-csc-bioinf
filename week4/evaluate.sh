#!/usr/bin/env bash
set -e

# === Config ===
PY=python3
CODON=codon
DATA_DIR="data"
ALIGNER_CODON="aligners.codon"
ALIGNER_PY="aligners.py"
CHECKPOINT_FILE=".large_checkpoint"

# === Helper: run one test ===
run_test() {
  local lang=$1
  local method=$2
  local a=$3
  local b=$4
  local start end runtime result

  start=$(date +%s%3N)
  if [ "$lang" = "python" ]; then
    result=$($PY $ALIGNER_PY --method $method --a $a --b $b)
  else
    result=$($CODON run $ALIGNER_CODON -- --method $method --a $a --b $b)
  fi
  end=$(date +%s%3N)
  runtime=$((end - start))
  printf "  %-14s %-8s %-8s %6sms\n" "$method" "$lang" "$result" "$runtime"
}

echo
echo "========== SHORT SEQUENCES (q1-t1 through q5-t5) =========="
echo "Method          Lang     Score   Time"
echo "---------------------------------------"

for i in 1 2 3 4 5; do
  echo "--- q$i vs t$i ---"
  for method in global local semi-global affine-global; do
    run_test python $method $DATA_DIR/q$i.fa $DATA_DIR/t$i.fa
    run_test codon  $method $DATA_DIR/q$i.fa $DATA_DIR/t$i.fa
  done
  echo
done

echo "========== LONG SEQUENCES (MT-human vs MT-orang) =========="
echo "Running both Python and Codon full tests..."
echo

methods=("global" "local" "semi-global" "affine-global")

if [ -f "$CHECKPOINT_FILE" ]; then
  last_done=$(cat "$CHECKPOINT_FILE")
else
  last_done=""
fi

for method in "${methods[@]}"; do
  if [ "$last_done" = "$method" ]; then
    skip=1
  fi
  if [ -z "$skip" ]; then
    echo "--- $method ---"
    # Python
    start=$(date +%s%3N)
    py_res=$($PY $ALIGNER_PY --method $method --a $DATA_DIR/MT-human.fa --b $DATA_DIR/MT-orang.fa)
    end=$(date +%s%3N)
    runtime=$((end - start))
    printf "  %-14s %-8s %-8s %6sms\n" "$method" "python" "$py_res" "$runtime"

    # Codon
    start=$(date +%s%3N)
    result=$($CODON run $ALIGNER_CODON -- --method $method --a $DATA_DIR/MT-human.fa --b $DATA_DIR/MT-orang.fa)
    end=$(date +%s%3N)
    runtime=$((end - start))
    printf "  %-14s %-8s %-8s %6sms\n" "$method" "codon" "$result" "$runtime"

    echo "$method" > "$CHECKPOINT_FILE"
    echo
  fi
done

echo "✅ Finished all sequence alignment tests."
echo "========================================"
echo "All tests finished."
