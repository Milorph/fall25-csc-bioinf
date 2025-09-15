#!/usr/bin/env bash
set -euo pipefail

# Paths
CODON_MAIN="code/main_codon.py"
PY_MAIN="code/main.py"
CODON_BIN="./assembler"
DATA_ROOT="data"
DATASETS=(data1 data2 data3 data4)

# Optional: pin Python hash seed for stable set order (doesn't change code)
export PYTHONHASHSEED=${PYTHONHASHSEED:-0}

echo "[build] codon build -release"
codon build -release -o "$CODON_BIN" "$CODON_MAIN"

# Inline N50 (ceil ≥50%)
n50_from_fasta() {
  python3 - "$1" <<'PYCODE'
import sys
p=sys.argv[1]
lens,cur=[],0
try:
  with open(p,'r',encoding='utf-8',errors='ignore') as f:
    for line in f:
      if line.startswith('>'):
        if cur: lens.append(cur); cur=0
      else:
        cur += len(line.strip())
  if cur: lens.append(cur)
except FileNotFoundError:
  print(0); sys.exit(0)
if not lens:
  print(0); sys.exit(0)
lens.sort(reverse=True)
total=sum(lens)
half=(total+1)//2  # ceil(50%)
s=0
for L in lens:
  s+=L
  if s>=half:
    print(L); break
PYCODE
}

echo
echo "Dataset   Impl        N50       Time(s)"
echo "--------  ----------  --------  -------"

for ds in "${DATASETS[@]}"; do
  dsdir="$DATA_ROOT/$ds"

  # --- Codon ---
  codon_out="$dsdir/contig_codon.fasta"
  start=$(date +%s.%N)
  ulimit -s 8192000
  "$CODON_BIN" "$dsdir" >/dev/null
  end=$(date +%s.%N)
  dt=$(echo "$end - $start" | bc)
  # rename to avoid being overwritten by Python
  if [[ -f "$dsdir/contig.fasta" ]]; then mv -f "$dsdir/contig.fasta" "$codon_out"; fi
  n50_c=$(n50_from_fasta "$codon_out")
  printf "%-8s  %-10s  %-8s  %7.3f\n" "$ds" "Codon" "$n50_c" "$dt"

  # --- Python ---
  py_out="$dsdir/contig_python.fasta"
  start=$(date +%s.%N)
  PYTHONHASHSEED=$PYTHONHASHSEED python3 "$PY_MAIN" "$dsdir" >/dev/null
  end=$(date +%s.%N)
  dt=$(echo "$end - $start" | bc)
  if [[ -f "$dsdir/contig.fasta" ]]; then mv -f "$dsdir/contig.fasta" "$py_out"; fi
  n50_p=$(n50_from_fasta "$py_out")
  printf "%-8s  %-10s  %-8s  %7.3f\n" "$ds" "Python" "$n50_p" "$dt"
done
