#!/usr/bin/env bash
set -euo pipefail

DATASETS=(data1 data2 data3 data4)

# helper: extract longest contig
longest_contig() {
python3 - "$1" <<'PY'
import sys
p=sys.argv[1]
hdr=None; seq=[]; best=(None,"")
with open(p) as f:
  for line in f:
    if line.startswith(">"):
      if hdr is not None:
        s="".join(seq)
        if len(s)>len(best[1]): best=(hdr,s)
      hdr=line.strip()[1:]; seq=[]
    else:
      seq.append(line.strip().upper())
if hdr is not None:
  s="".join(seq)
  if len(s)>len(best[1]): best=(hdr,s)
print(f">{best[0]}\n{best[1]}")
PY
}

for ds in "${DATASETS[@]}"; do
  contig="data/$ds/contig_codon.fasta"   # adjust if you only have contig.fasta
  longest="/tmp/${ds}_longest.fasta"
  result="data/$ds/blast_top_hits.tsv"

  echo "[${ds}] extracting longest contig..."
  longest_contig "$contig" > "$longest"

  echo "[${ds}] running BLAST remotely..."
  blastn -task megablast -query "$longest" -db nt -remote \
    -max_target_seqs 5 -max_hsps 1 \
    -outfmt "6 qseqid saccver ssciname pident length evalue bitscore stitle" \
    > "$result"

  echo "[${ds}] results saved to $result"
  sleep 2   # be kind to NCBI servers
done
