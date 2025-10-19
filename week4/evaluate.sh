#!/usr/bin/env bash
set -e

echo "========== Week 4 – Sequence Alignment Evaluation =========="

PYTHON_ALIGNER="week4/aligners.py"
CODON_ALIGNER="week4/aligners.codon"
DATA_DIR="week4/data"

MT_HUMAN="$DATA_DIR/MT-human.fa"
MT_ORANG="$DATA_DIR/MT-orang.fa"

Q_FILES=($DATA_DIR/q1.fa $DATA_DIR/q2.fa $DATA_DIR/q3.fa $DATA_DIR/q4.fa $DATA_DIR/q5.fa)
T_FILES=($DATA_DIR/t1.fa $DATA_DIR/t2.fa $DATA_DIR/t3.fa $DATA_DIR/t4.fa $DATA_DIR/t5.fa)

METHODS=("global" "local" "semi-global" "affine-global")

printf "%-15s %-8s %-8s %-10s\n" "Method" "Lang" "Score" "Runtime"
echo "-----------------------------------------------"

run_and_time() {
    local cmd="$1"
    local start=$(date +%s%3N)
    local result
    result=$(eval "$cmd")
    local end=$(date +%s%3N)
    local runtime=$((end - start))
    echo "$result $runtime"
}

# === SHORT SEQUENCES ===
echo
echo "========== SHORT SEQUENCES (q1-t1 through q5-t5) =========="

for i in {0..4}; do
    Q=${Q_FILES[$i]}
    T=${T_FILES[$i]}
    echo
    echo "--- $(basename $Q .fa) vs $(basename $T .fa) ---"
    for M in "${METHODS[@]}"; do
        for L in "python" "codon"; do
            if [ "$L" = "python" ]; then
                CMD="python3 $PYTHON_ALIGNER --method $M --a $Q --b $T"
            else
                CMD="codon run $CODON_ALIGNER -- --method $M --a $Q --b $T"
            fi
            read -r SCORE RUNTIME <<<"$(run_and_time "$CMD")"
            printf "  %-15s %-8s %-8s %s\n" "$M" "$L" "$SCORE" "${RUNTIME}ms"
        done
    done
done

# === LONG SEQUENCES ===
echo
echo "========== LONG SEQUENCES (MT-human vs MT-orang) =========="

for M in "${METHODS[@]}"; do
    echo
    echo "--- $M ---"
    for L in "python" "codon"; do
        if [ "$L" = "python" ]; then
            CMD="python3 $PYTHON_ALIGNER --method $M --a $MT_HUMAN --b $MT_ORANG"
        else
            CMD="codon run $CODON_ALIGNER -- --method $M --a $MT_HUMAN --b $MT_ORANG"
        fi
        read -r SCORE RUNTIME <<<"$(run_and_time "$CMD")"
        printf "  %-15s %-8s %-8s %s\n" "$M" "$L" "$SCORE" "${RUNTIME}ms"
    done
done

echo
echo "✅ Finished all alignment tests."
echo "========================================"
