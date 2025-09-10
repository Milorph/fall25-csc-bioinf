#!/usr/bin/env bash
set -euxo pipefail

# Datasets
DATASETS=("data1" "data2" "data3" "data4")

mkdir -p out quast_out

# Table header
echo -e "Dataset\tLanguage\tRuntime(s)\tGenomeFraction\tDuplicationRatio\tNGA50\tMissassemblies\tMismatches"

run_one () {
  local ds="$1"
  local lang="$2"
  local cmd="$3"
  local tag="$4"

  /usr/bin/time -f "%e" -o "out/${ds}_${tag}.time" ${cmd} > "out/${ds}_${tag}.log" 2>&1
  runtime=$(cat "out/${ds}_${tag}.time")

  metrics="NA\tNA\tNA\tNA\tNA"   # (will fill later with QUAST)
  echo -e "${ds}\t${lang}\t${runtime}\t${metrics}"
}

for ds in "${DATASETS[@]}"; do
  # NOTE: we pass week1/<dataset> so main.py sees the actual folder with FASTAs
  run_one "${ds}" "python" "python3 week1/code/main.py week1/${ds}" "python"

  # Codon row (uncomment when ready)
  # run_one "${ds}" "codon" "codon run -release week1/code/main.py week1/${ds}" "codon"
done
